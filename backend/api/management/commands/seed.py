from django.core.management.base import BaseCommand
import requests
import os
from ...models import BasicTickerData, DetailedTickerData, HistoricalTickerData, FavoriteTickerData

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        BasicTickerData.objects.all().delete()
        DetailedTickerData.objects.all().delete()
        HistoricalTickerData.objects.all().delete()
        FavoriteTickerData.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Deleted all data from the database."))

        self.stdout.write('Seeding the database...')

        try:
            seed_basic_ticker_data()
            self.stdout.write(self.style.SUCCESS('Basic Ticker Data seeding completed.'))

            seed_detailed_ticker_data(num_tickers=20)
            self.stdout.write(self.style.SUCCESS('Detailed Ticker Data seeding completed.'))

            detailed_ticker_data = DetailedTickerData.objects.all()

            for ticker in detailed_ticker_data:
                seed_historical_ticker_data(ticker.basic_data.symbol)

            self.stdout.write(self.style.SUCCESS('Historical Ticker Data seeding completed.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))

        self.stdout.write(self.style.SUCCESS('Database seeding completed.'))


def seed_basic_ticker_data():
    try:
        response = requests.get(f"https://financialmodelingprep.com/api/v3/available-traded/list?apikey={os.environ.get('FMP_API_KEY')}")
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch basic ticker data: {e}")

    for ticker in data:
        if all([
            ticker["symbol"], ticker["exchange"], ticker["exchangeShortName"], 
            ticker['exchangeShortName'] in ["NASDAQ", "NYSE"], 
            ticker["name"], ticker["price"], ticker["type"]
        ]):
            BasicTickerData.objects.create(
                **ticker
            )


def seed_detailed_ticker_data(num_tickers=None):
    tickers = BasicTickerData.objects.all()

    if num_tickers is None:
        num_tickers = len(tickers)
    
    for ticker in tickers[:num_tickers]:
        try:
            response = requests.get(f"https://financialmodelingprep.com/api/v3/profile/{ticker.symbol}?apikey={os.environ.get('FMP_API_KEY')}")
            response.raise_for_status()
            detailed_data = response.json()[0]
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch detailed ticker data for {ticker.symbol}: {e}")

        detailed_data.pop("symbol", None)
        detailed_data.pop("price", None)
        detailed_data.pop("exchange", None)
        detailed_data.pop("exchangeShortName", None)
        detailed_data.pop("companyName", None)
        
        DetailedTickerData.objects.create(
            **detailed_data,
            basic_data=ticker,
        )


def seed_historical_ticker_data(symbol):
    try:
        basic_info = BasicTickerData.objects.get(symbol=symbol)
        detailed_info = DetailedTickerData.objects.get(basic_data=basic_info)

        response = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={os.environ.get('FMP_API_KEY')}")
        response.raise_for_status()
        historical_info = response.json()["historical"]
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch historical ticker data for {symbol}: {e}")

    for data in historical_info:
        HistoricalTickerData.objects.create(
            **data,
            basic_data=basic_info,
            detailed_data=detailed_info
        )