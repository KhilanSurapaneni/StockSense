from .models import BasicTickerData, DetailedTickerData, HistoricalTickerData, FavoriteTickerData
from datetime import date, timedelta
import requests
import os

# Returning detailed ticker data for a specific ticker
def get_detailed_data(symbol):
    try:
        ticker = BasicTickerData.objects.get(symbol=symbol)
        response = requests.get(f"https://financialmodelingprep.com/api/v3/profile/{ticker.symbol}?apikey={os.environ.get('FMP_API_KEY')}")
        response.raise_for_status()
        detailed_data = response.json()[0]
    except BasicTickerData.DoesNotExist:
        raise Exception(f"Ticker {symbol} not found in the database.")
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch detailed ticker data for {ticker.symbol}: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

    # Remove unnecessary fields
    detailed_data.pop("symbol", None)
    detailed_data.pop("price", None)
    detailed_data.pop("exchange", None)
    detailed_data.pop("exchangeShortName", None)
    detailed_data.pop("companyName", None)

    # Create and return the DetailedTickerData object
    DetailedTickerData.objects.create(
        **detailed_data,
        basic_data=ticker,
    )

    return DetailedTickerData.objects.get(basic_data=ticker)

# Fetching historical ticker data for a specific ticker
def get_historical_data(symbol, end_date=None):
    start_date = date.today().strftime("%Y-%m-%d")
    try:
        
        basic_info = BasicTickerData.objects.get(symbol=symbol)
        detailed_info = DetailedTickerData.objects.get(basic_data=basic_info)
        if end_date is None:
            response = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={os.environ.get('FMP_API_KEY')}")
        else:
            end_date = str(end_date)
            response = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={os.environ.get('FMP_API_KEY')}&from={end_date}&to={start_date}")

        response.raise_for_status()
        historical_info = response.json()["historical"]
    except BasicTickerData.DoesNotExist:
        raise Exception(f"Ticker {symbol} not found in the database.")
    except DetailedTickerData.DoesNotExist:
        raise Exception(f"Detailed data for ticker {symbol} not found in the database.")
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch historical ticker data for {symbol}: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

    # Create HistoricalTickerData objects
    for data in historical_info:
        HistoricalTickerData.objects.create(
            **data,
            basic_data=basic_info,
            detailed_data=detailed_info
        )

# Checking if a given date is the most recent Friday
def is_most_recent_friday(given_date):
    today = date.today()
    # Calculate the most recent Friday from today's date
    most_recent_friday = today - timedelta(days=(today.weekday() + 3) % 7)
    return given_date == most_recent_friday
