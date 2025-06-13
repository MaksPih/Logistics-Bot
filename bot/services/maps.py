import aiohttp
from bot.config import GOOGLE_MAPS_API_KEY
from bs4 import BeautifulSoup
from datetime import datetime

# Розхід пального на 100 км
FUEL_CONSUMPTION = {
    "тент": 28,
    "рефрижератор": 35,
    "зерновоз/самоскид": 38,
    "трал/негабарит": 43,
    "контейнеровоз": 40,
    "автоцистерна": 37
}

def get_per_km_rate(distance_km: float, base_rate: float) -> float:
    if distance_km < 50:
        return base_rate * 1.9        # дуже короткий маршрут
    elif distance_km < 100:
        return base_rate * 1.6        # короткий
    elif distance_km < 300:
        return base_rate * 1.3        # середній
    elif distance_km < 600:
        return base_rate * 0.9        # далекий
    elif distance_km < 1000:
        return base_rate * 0.8        # дуже далекий
    else:
        return base_rate * 0.7        # наддалекий

def calculate_cost(distance_km: float, vehicle_type: str, fuel_price: float):
    fuel_l_per_100km = FUEL_CONSUMPTION.get(vehicle_type, 35)
    fuel_l = round((fuel_l_per_100km / 100) * distance_km, 2)
    fuel_cost = round(fuel_l * fuel_price, 2)

    base_rate = {
        "тент": 36,
        "рефрижератор": 41,
        "зерновоз/самоскид": 44,
        "трал/негабарит": 55,
        "контейнеровоз": 46,
        "автоцистерна": 43
    }.get(vehicle_type, 50)

    per_km = get_per_km_rate(distance_km, base_rate)
    base_cost = round(per_km * distance_km, 2)
    total = round(base_cost + fuel_cost, 2)

    return {
        "fuel_l": fuel_l,
        "fuel_price": fuel_price,
        "fuel_cost": fuel_cost,
        "per_km": round(per_km, 2),
        "base_cost": base_cost,
        "total": total
    }

async def get_route_data(origin: str, destination: str):
    async with aiohttp.ClientSession() as session:
        url = (
            "https://maps.googleapis.com/maps/api/directions/json"
            f"?origin={origin}&destination={destination}&key={GOOGLE_MAPS_API_KEY}&language=uk"
        )
        async with session.get(url) as resp:
            data = await resp.json()

    if not data["routes"]:
        return None

    route = data["routes"][0]
    leg = route["legs"][0]

    distance_km = leg["distance"]["value"] / 1000  # метри → км
    duration_raw = leg["duration"]["value"]  # у секундах
    duration_sec = int(duration_raw * 1.4)   # +40% затримки
    duration_h = duration_sec // 3600
    duration_m = (duration_sec % 3600) // 60
    duration_str = f"{duration_h} год {duration_m} хв"
    polyline = route["overview_polyline"]["points"]

    return {
        "distance_km": round(distance_km, 2),
        "duration_str": duration_str,
        "polyline": polyline
    }   

def build_static_map(origin: str, destination: str, polyline: str) -> str:
    return (
        "https://maps.googleapis.com/maps/api/staticmap?"
        f"size=600x400&language=uk"
        f"&path=enc:{polyline}"
        f"&markers=color:green|label:A|{origin}"
        f"&markers=color:red|label:B|{destination}"
        f"&key={GOOGLE_MAPS_API_KEY}"
    )

async def get_current_fuel_price():
    url = "https://index.minfin.com.ua/ua/fuel/"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "html.parser")
    block = soup.find("table", class_="index-table")
    if not block:
        return None, None

    rows = block.find_all("tr")
    for row in rows:
        if "ДП" in row.text:
            price_td = row.find_all("td")
            try:
                price = float(price_td[1].text.replace(",", "."))
                date_str = datetime.now().strftime("%d.%m.%Y")
                return round(price, 2), date_str
            except:
                return None, None

    return None, None