from requests import request as http_request, RequestException
from asyncio import sleep, run
from datetime import datetime
from fetcher.config import EXCHANGES, USDT, BINANCE, API_URL, SLEEP_TIME
from fetcher.database import get_session, setup_database
from fetcher.models import ARPValue


async def save_to_db(exchange_name, token, arp_value):
    with get_session() as session:

        arp_value_record = ARPValue(
            exchange_name=exchange_name,
            token=token,
            arp_value=arp_value,
            timestamp=datetime.now()
        )

        session.add(arp_value_record)
        session.commit()

async def fetch_arp(exchange_key, token):
    exchange = EXCHANGES.get(exchange_key)
    if exchange:
        url = exchange[API_URL].format(token)
        try:
            response = http_request('GET', url)
            response.raise_for_status()
            data = response.json()

            return round(float(data['data']['savingFlexibleProduct'][0]['apy']) * 100, 2)
        except (RequestException, KeyError) as ex:
            print(f"Error fetching ARP : {ex} \n ")
            return None
    return None

async def monitor():
    while True:
        arp_value = await fetch_arp(BINANCE, USDT)
        if arp_value is not None:
            await save_to_db(BINANCE, USDT, arp_value)
        await sleep(SLEEP_TIME)

if __name__ == "__main__":
    setup_database()
    run(monitor())
