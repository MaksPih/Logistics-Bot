import pytest
from unittest.mock import AsyncMock, patch
from bot.services.maps import (get_per_km_rate, calculate_cost, build_static_map, get_route_data)

def test_get_per_km_rate():
    assert get_per_km_rate(30, 50) == 95.0     # < 50
    assert get_per_km_rate(70, 40) == 64.0     # < 100
    assert get_per_km_rate(200, 30) == 39.0    # < 300
    assert get_per_km_rate(500, 60) == 54.0    # < 600
    assert get_per_km_rate(800, 40) == 32.0    # < 1000
    assert get_per_km_rate(1500, 70) == 49.0   # > 1000

def test_calculate_cost():
    result = calculate_cost(250, "тент", 52.28)
    assert isinstance(result, dict)
    assert result["fuel_l"] > 0
    assert result["fuel_cost"] > 0
    assert result["total"] > 0
    assert round(result["fuel_price"], 2) == 52.28
    assert "per_km" in result and result["per_km"] > 0

def test_build_static_map():
    url = build_static_map("Київ", "Львів", "test_polyline")
    assert "maps.googleapis.com" in url
    assert "Київ" in url
    assert "Львів" in url
    assert "test_polyline" in url
    assert url.startswith("https://")

@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_get_route_data(mock_get):
    mock_response = AsyncMock()
    mock_response.json.return_value = {
        "routes": [{
            "legs": [{
                "distance": {"value": 150000},  # 150 км
                "duration": {"value": 14400},   # 4 години (у секундах)
            }],
            "overview_polyline": {"points": "abc123"}
        }]
    }
    mock_get.return_value.__aenter__.return_value = mock_response

    result = await get_route_data("Київ", "Львів")

    assert result is not None
    assert result["distance_km"] == 150.0
    assert "год" in result["duration_str"]
    assert result["polyline"] == "abc123"