from django.db import models
from django.contrib.auth.models import User

# Load using Actively Traded List API

# The goal is to load this from the FMP API once every single day, it will return this data for EVERY ticker and only count as a singular API call, we will be filtering this to NYSE and NASDAQ only
# Additionally, we will only support actively traded stocks
class BasicTickerData(models.Model):
    symbol = models.CharField(max_length=10)
    exchange = models.CharField(max_length=50)
    exchangeShortName = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    # detailed_data will be able to be accessed on this model, if it is null, then it hasn't been loaded yet, must make API call
    # historical_data will also be able to be accessed, if it is null or the most recent date is not equal to the current date, you must make the API call to load the data

    def __str__(self):
        return f"{self.symbol} - {self.name}"


# Load using Company Information API

# The goal is to load this model once per day in two cases:
# Case 1: 
# If a user views this stock (opens up a detailed view, not a list view), this information will be loaded and stored in the db, so if they click it again then we can access the data without making an additional API call
# Case 2:
# If this stock is favorited by the user, then when we load the BasicTickerData we will also load this data, thus avoiding having to make an additional API call when the user clicks on their favorited stock
class DetailedTickerData(models.Model):
    basic_data = models.OneToOneField(BasicTickerData, on_delete=models.CASCADE, related_name='detailed_data')
    beta = models.DecimalField(max_digits=10, decimal_places=8)
    volAvg = models.BigIntegerField()
    mktCap = models.BigIntegerField()
    lastDiv = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    range = models.CharField(max_length=50)
    changes = models.DecimalField(max_digits=20, decimal_places=8)
    companyName = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)
    cik = models.CharField(max_length=20)
    isin = models.CharField(max_length=20)
    cusip = models.CharField(max_length=20, null=True, blank=True)
    industry = models.CharField(max_length=100)
    website = models.URLField(max_length=200)
    description = models.TextField()
    ceo = models.CharField(max_length=100)
    sector = models.CharField(max_length=50)
    country = models.CharField(max_length=2)
    fullTimeEmployees = models.IntegerField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=20)
    dcfDiff = models.DecimalField(max_digits=20, decimal_places=8)
    dcf = models.DecimalField(max_digits=20, decimal_places=8)
    image = models.URLField(max_length=200)
    ipoDate = models.DateField()
    defaultImage = models.BooleanField()
    isEtf = models.BooleanField()
    isActivelyTrading = models.BooleanField()
    isAdr = models.BooleanField()
    isFund = models.BooleanField()

    def __str__(self):
        return f"{self.basic_data.symbol} - Detailed Data"

# The goal is when a user clicks this stock for the first time (opens up detailed view) we will load the historical data for all date ranges from the current date (up to 5 years back according to API limitations),
# on future views of the details we will update the data using the API from the current date to the most recent date stored in our database for the particular stock, speeding up data loads. 
# for favorited stocks we will update this with new dates every single day.
class HistoricalData(models.Model):
    basic_data = models.ForeignKey(BasicTickerData, on_delete=models.CASCADE, related_name='historical_data')
    detailed_data = models.ForeignKey(DetailedTickerData, on_delete=models.CASCADE, related_name='historical_data')
    date = models.DateField()
    open_price = models.DecimalField(max_digits=20, decimal_places=8)
    high_price = models.DecimalField(max_digits=20, decimal_places=8)
    low_price = models.DecimalField(max_digits=20, decimal_places=8)
    close_price = models.DecimalField(max_digits=20, decimal_places=8)
    adj_close_price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.BigIntegerField()
    unadjusted_volume = models.BigIntegerField()
    change = models.DecimalField(max_digits=20, decimal_places=8)
    change_percent = models.DecimalField(max_digits=10, decimal_places=8)
    vwap = models.DecimalField(max_digits=20, decimal_places=8)
    label = models.CharField(max_length=50)
    change_over_time = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"{self.basic_data.symbol} - {self.date}"

# This is separate relational table that connects users with their favorite stocks
class FavoriteStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_stocks')
    basic_data = models.ForeignKey(BasicTickerData, on_delete=models.CASCADE, related_name='favorited_by_users')
    detailed_data = models.ForeignKey(DetailedTickerData, on_delete=models.CASCADE, related_name='favorited_by_users')
    favorited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.basic_data.symbol}"