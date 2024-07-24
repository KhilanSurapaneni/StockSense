from django.contrib import admin
from .models import BasicTickerData, DetailedTickerData, HistoricalTickerData, FavoriteTickerData, GeneralNews

# Register your models here.
admin.register(BasicTickerData)
admin.register(DetailedTickerData)
admin.register(HistoricalTickerData)
admin.register(FavoriteTickerData)
admin.register(GeneralNews)