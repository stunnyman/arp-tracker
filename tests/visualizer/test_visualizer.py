import pytest
from httpx import AsyncClient, ASGITransport
from visualizer import app


@pytest.mark.asyncio
async def test_read_root_no_data(monkeypatch):
    async def mock_get_db_connection():
        class MockConnection:
            async def fetch(self, query):
                return []

            async def close(self):
                pass

        return MockConnection()

    monkeypatch.setattr("visualizer.main.get_db_connection", mock_get_db_connection)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.text == "No data found"


@pytest.mark.asyncio
async def test_read_root_with_data(monkeypatch):
    async def mock_get_db_connection():
        class MockConnection:
            async def fetch(self, query):
                return [
                    {"timestamp": "2024-1-1T12:00:00Z", "arp_value": 5}
                ]

            async def close(self):
                pass

        return MockConnection()

    monkeypatch.setattr("visualizer.main.get_db_connection", mock_get_db_connection)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "Binance x USDT" in response.text


@pytest.mark.asyncio
async def test_healthcheck():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
