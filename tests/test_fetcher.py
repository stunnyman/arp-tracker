import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from fetcher import save_to_db, BINANCE, USDT

@pytest.mark.asyncio
@patch('fetcher.main.get_session')
async def test_save_to_db(mock_get_session):
    mock_session = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_session

    await save_to_db(BINANCE, USDT, 1.23)

    mock_session.add.assert_called_once()
    record = mock_session.add.call_args[0][0]
    assert record.exchange_name == BINANCE
    assert record.token == USDT
    assert record.arp_value == 1.23
    assert isinstance(record.timestamp, datetime)

    mock_session.commit.assert_called_once()


# @pytest.mark.asyncio
# @patch('fetcher.app.main.http_request')
# async def test_fetch_arp_success(mock_http_request):
#     mock_response = MagicMock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {
#         'data': {
#             'savingFlexibleProduct': [{'apy': '0.0123'}]
#         }
#     }
#     mock_http_request.return_value = mock_response
#
#     arp_value = await app.fetch_arp(app.BINANCE, app.USDT)
#     assert arp_value == 1.23
#
#
# @pytest.mark.asyncio
# @patch('fetcher.app.main.http_request')
# async def test_fetch_arp_invalid_data(mock_http_request):
#     mock_response = MagicMock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {}
#     mock_http_request.return_value = mock_response
#
#     arp_value = await app.fetch_arp(app.BINANCE, app.USDT)
#     assert arp_value is None
