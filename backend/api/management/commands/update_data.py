# myapp/management/commands/update_data.py

from django.core.management.base import BaseCommand
from ...models import BasicTickerData, FavoriteTickerData, DetailedTickerData, GeneralNews, HistoricalTickerData
from ...helpers.helper_functions import get_historical_data, is_most_recent_friday
from datetime import date, timedelta
import requests
import os

class Command(BaseCommand):
    help = 'Update stock data from external API'

    def handle(self, *args, **kwargs):
        # Entry point for the command
        self.update_general_news()
        self.update_basic_ticker_data()
        self.update_favorite_detailed_and_historical_data()

    def update_basic_ticker_data(self):
        # Update basic ticker data if it hasn't been updated today
        if BasicTickerData.objects.get(symbol="AAPL").updated_at == date.today():
            self.stdout.write("Basic ticker data updated successfully with no changes.")
        else:
            self.stdout.write("Updating basic ticker data...")
            
            try:
                # Fetch data from the external API
                response = requests.get(f"https://financialmodelingprep.com/api/v3/available-traded/list?apikey={os.environ.get('FMP_API_KEY')}")
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as e:
                # Handle request errors
                self.stderr.write(f"Failed to fetch basic ticker data: {e}")
                return

            # Iterate over the fetched data and update/create BasicTickerData objects
            for ticker in data:
                if all([
                    ticker["symbol"], ticker["exchange"], ticker["exchangeShortName"], 
                    ticker['exchangeShortName'] in ["NASDAQ", "NYSE"], 
                    ticker["name"], ticker["price"], ticker["type"]
                ]):
                    if BasicTickerData.objects.filter(symbol=ticker["symbol"]).exists():
                        # Update existing ticker data
                        BasicTickerData.objects.filter(symbol=ticker["symbol"]).update(**ticker)
                    else:
                        # Create new ticker data
                        BasicTickerData.objects.create(**ticker)
            
            self.stdout.write("Basic ticker data updated successfully.")

    def update_favorite_detailed_and_historical_data(self):
        # Update detailed and historical data for favorite tickers
        for ticker in FavoriteTickerData.objects.all():
            if DetailedTickerData.objects.filter(basic_data=ticker.basic_data).exists() and DetailedTickerData.objects.get(basic_data=ticker.basic_data).updated_at == date.today():
                continue  # Skip updating if data is already up-to-date
            else:
                self.stdout.write(f"Updating detailed ticker data for {ticker.basic_data.symbol}...")
                try:
                    # Fetch detailed data from the external API
                    response = requests.get(f"https://financialmodelingprep.com/api/v3/profile/{ticker.basic_data.symbol}?apikey={os.environ.get('FMP_API_KEY')}")
                    response.raise_for_status()
                    detailed_data = response.json()[0]
                except requests.RequestException as e:
                    # Handle request errors
                    self.stderr.write(f"Failed to fetch detailed ticker data for {ticker.basic_data.symbol}: {e}")
                    continue  # Move on to the next ticker if there is an error

                # Remove unnecessary fields
                for field in ["symbol", "price", "exchange", "exchangeShortName", "companyName"]:
                    detailed_data.pop(field, None)

                # Update or create DetailedTickerData objects
                if DetailedTickerData.objects.filter(basic_data=ticker.basic_data).exists():
                    DetailedTickerData.objects.filter(basic_data=ticker.basic_data).update(**detailed_data)
                else:
                    DetailedTickerData.objects.create(**detailed_data, basic_data=ticker.basic_data)
            
            # Update the HistoricalTickerData objects
            latest_entry = HistoricalTickerData.objects.filter(basic_data=ticker.basic_data).order_by('-date').first()

            # Check if the latest entry is up-to-date
            if latest_entry and latest_entry.date < date.today() and not is_most_recent_friday(latest_entry.date):
                get_historical_data(ticker.basic_data.symbol, end_date=latest_entry.date + timedelta(days=1))
            elif not latest_entry:
                get_historical_data(ticker.basic_data.symbol)

        self.stdout.write("Favorite detailed and historical ticker data updated successfully.")

    def update_general_news(self):
        # Update general news if it hasn't been updated today
        if GeneralNews.objects.all().count() > 0 and GeneralNews.objects.all()[0].updated_at == date.today():
            self.stdout.write("General news updated successfully with no changes.")
        else:
            self.stdout.write("Updating general news...")
            try:
                # Fetch news articles from the external API
                response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={os.environ.get('NEWS_API_KEY')}&category=business").json()["articles"]
                
                # Delete existing news articles
                GeneralNews.objects.all().delete()

                # Create new GeneralNews objects
                for article in response:
                    article.pop("source", None)
                    GeneralNews.objects.create(**article)

                self.stdout.write("General news updated successfully.")
            except requests.RequestException as e:
                # Handle request errors
                raise Exception(f"Failed to fetch general news: {e}")
