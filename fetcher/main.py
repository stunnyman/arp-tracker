from requests import request as http_request, RequestException
from time import sleep
from datetime import datetime
from config import EXCHANGES, USDT, BINANCE, API_URL
from database import get_session, setup_database
from models import ARPValue


def save_to_db(exchange_name, token, arp_value):
    with get_session() as session:

        arp_value_record = ARPValue(
            exchange_name=exchange_name,
            token=token,
            arp_value=arp_value,
            timestamp=datetime.now()
        )

        session.add(arp_value_record)
        session.commit()

def fetch_arp(exchange_key, token):
    exchange = EXCHANGES.get(exchange_key)
    if exchange:
        url = exchange[API_URL].format(token)
        try:
            response = http_request('GET', url)
            response.raise_for_status()
            data = response.json()

            arp_value = round(float(data['data']['savingFlexibleProduct'][0]['apy']) * 100, 2)
            return arp_value
        except (RequestException, KeyError) as ex:
            print(f"Error fetching ARP : {ex} \n ")
            return None
    return None

def monitor():
    while True:
        arp_value = fetch_arp(BINANCE, USDT)
        if arp_value is not None:
            save_to_db(BINANCE, USDT, arp_value)
        sleep(6)

if __name__ == "__main__":
    setup_database()
    sleep(10)
    monitor()
