from django.urls import path
from .views import CreateUserView, UserProfileActions, ChangePasswordView, CombinedTickerDetailView, FavoriteTickersView, TickerSearchView, DashboardView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"), # allows a user to register
    path("token/", TokenObtainPairView.as_view(), name="login"), # allows a user to login
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"), # allows a user to refresh their JWT tokens, so they dont have to continuously login
    path("profile/", UserProfileActions.as_view(), name="profile-actions"), # allows a user to view, update, and delete their OWN profile only
    path("password/change/", ChangePasswordView.as_view(), name="password-change"), # allows a user to change their password
    path("ticker/favorites/", FavoriteTickersView.as_view(), name="favorite-tickers"), # allows a user to view which tickers they have favorited, and add/remove tickers from their favorites
    path("ticker/search/", TickerSearchView.as_view(), name="ticker-search"), # allows a user to search for tickers by symbol, it returns a list of tickers that match the search query
    path("ticker/dashboard/", DashboardView.as_view(), name="dashboard"), # allows a user to view basic + detailed ticker data for their favorite tickers or popular tickers if they are not logged in, top stories/news about business
    path("ticker/<str:symbol>/", CombinedTickerDetailView.as_view(), name="ticker-detail"), # allows a user to view ticker data for a specific stock, it combines the basic ticker data with the detailed ticker data and the latest historical data
]

# Home Page / Dashboard:
  # Logged in:
    # User can view basic + detailed ticker data for their favorite tickers
    # User can view top stories/news about business, store in db and update once per day
    # User can search for tickers
    
  # Not Logged in:
    # User can view a list of popular tickers along with detailed ticker data, for that popular ticker
    # User can view top stories/news about business, store in db and update once per day
    # User can search for tickers

# Profile Page:
  # Logged in:
    # User can view details about their profile, and update their profile
    # User can add/remove tickers from their favorites
    # User can change their password
  # Not Logged in:
    # No access to profile page

# Ticker Page:
  # Logged in:
    # User can view basic + detailed + historical ticker data for a specific ticker
    # User can add/remove ticker from their favorites
    # User can view news articles directly related to the ticker
  # Not Logged in:
    # User can view basic + detailed + historical ticker data for a specific ticker
    # User can view news articles directly related to the ticker
