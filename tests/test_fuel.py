import pytest
from unittest.mock import AsyncMock, patch
from bot.services.fuel import get_current_fuel_price

@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_get_current_fuel_price(mock_get):
    fake_html = """
        <html>
            <body>
                <table class="line">
                    <tr><td>А95</td><td>50.00</td><td>51.00</td></tr>
                    <tr><td>Дизельне паливо</td><td>52.50</td><td>53,30</td></tr>
                </table>
            </body>
        </html>
    """

    mock_response = AsyncMock()
    mock_response.text.return_value = fake_html
    mock_get.return_value.__aenter__.return_value = mock_response

    price, date_str = await get_current_fuel_price()

    assert price == 53.30
    assert isinstance(date_str, str)
    assert len(date_str) == 10  # формат: dd.mm.yyyy