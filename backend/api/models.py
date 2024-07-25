from django.db import models
from django.contrib.auth.models import User

# Load using Actively Traded List API
class BasicTickerData(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    exchange = models.CharField(max_length=255)
    exchangeShortName = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    updated_at = models.DateField(auto_now=True)
    # detailed_data will be able to be accessed on this model, if it is null, then it hasn't been loaded yet, must make API call

    def __str__(self):
        return f"{self.symbol} - {self.name}"

# Load using Company Information API
class DetailedTickerData(models.Model):
    # Basic and essential information
    basic_data = models.OneToOneField(BasicTickerData, on_delete=models.CASCADE, related_name='detailed_data')
    currency = models.CharField(max_length=255)
    changes = models.DecimalField(max_digits=20, decimal_places=8)
    ipoDate = models.DateField()
    beta = models.DecimalField(max_digits=12, decimal_places=10)  # Adjusted precision and scale
    volAvg = models.BigIntegerField()
    mktCap = models.BigIntegerField()

    # Optional financial information
    lastDiv = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)  # Adjusted precision and scale
    dcfDiff = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    dcf = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)

    # Optional identification and classification
    cik = models.CharField(max_length=255, blank=True, null=True)
    cusip = models.CharField(max_length=255, blank=True, null=True)
    isin = models.CharField(max_length=255, blank=True, null=True)
    isEtf = models.BooleanField(blank=True, null=True)
    isAdr = models.BooleanField(blank=True, null=True)
    isFund = models.BooleanField(blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)

    # Optional descriptive information
    range = models.CharField(max_length=255, blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ceo = models.CharField(max_length=255, blank=True, null=True)
    fullTimeEmployees = models.IntegerField(blank=True, null=True)
    isActivelyTrading = models.BooleanField(blank=True, null=True)

    # Optional contact information
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)

    # Optional media information
    image = models.TextField(blank=True, null=True)
    defaultImage = models.BooleanField(blank=True, null=True)

    # Updated at
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.basic_data.symbol} - Detailed Data"

# Load this from the News API once every single day along with the basic ticker data
class GeneralNews(models.Model):
    author = models.TextField(blank=True, null=True)
    title = models.TextField()
    url = models.TextField(unique=True)
    publishedAt = models.DateTimeField()
    urlToImage = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

# This is separate relational table that connects users with their favorite stocks
class FavoriteTickerData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_stocks')
    basic_data = models.ForeignKey(BasicTickerData, on_delete=models.CASCADE, related_name='favorited_by_users')
    favorited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'basic_data')

    def __str__(self):
        return f"{self.user.username} - {self.basic_data.symbol}"

# The goal is when a user clicks this stock for the first time (opens up detailed view) we will load the historical data for all date ranges from the current date (up to 5 years back according to API limitations),
# on future views of the details we will update the data using the API from the current date to the most recent date stored in our database for the particular stock, speeding up data loads. 
# for favorited stocks we will update this with new dates every single day.
class HistoricalTickerData(models.Model):
    basic_data = models.ForeignKey(BasicTickerData, on_delete=models.CASCADE, related_name='historical_data')
    detailed_data = models.ForeignKey(DetailedTickerData, on_delete=models.CASCADE, related_name='historical_data')
    date = models.DateField()
    open = models.DecimalField(max_digits=20, decimal_places=8)
    high = models.DecimalField(max_digits=20, decimal_places=8)
    low = models.DecimalField(max_digits=20, decimal_places=8)
    close = models.DecimalField(max_digits=20, decimal_places=8)
    adjClose = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.BigIntegerField()
    unadjustedVolume = models.BigIntegerField()
    change = models.DecimalField(max_digits=20, decimal_places=8)
    changePercent = models.DecimalField(max_digits=12, decimal_places=10)  # Adjusted precision and scale
    vwap = models.DecimalField(max_digits=20, decimal_places=8)
    label = models.CharField(max_length=255)
    changeOverTime = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"{self.basic_data.symbol} - {self.date}"