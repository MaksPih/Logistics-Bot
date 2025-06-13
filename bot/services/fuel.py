import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime

async def get_current_fuel_price():
    url = "https://index.minfin.com.ua/ua/fuel/"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "html.parser")
    block = soup.find("table", class_="line")
    if not block:
        return None, None

    rows = block.find_all("tr")
    for row in rows:
        if "Дизельне паливо" in row.text:
            price_td = row.find_all("td")
            try:
                price = float(price_td[2].text.replace(",", "."))
                date_str = datetime.now().strftime("%d.%m.%Y")
                return round(price, 2), date_str
            except:
                return None, None

    return None, None