from django.urls import path
from .views import CreateUserView, UserProfileActions, ChangePasswordView, CombinedTickerDetailView, FavoriteTickersView, TickerSearchView, DashboardView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"), 
    path("profile/", UserProfileActions.as_view(), name="profile-actions"),
    path("password/change/", ChangePasswordView.as_view(), name="password-change"),
    path("ticker/favorites/", FavoriteTickersView.as_view(), name="favorite-tickers"), 
    path("ticker/search/", TickerSearchView.as_view(), name="ticker-search"), 
    path("ticker/dashboard/", DashboardView.as_view(), name="dashboard"), 
    path("ticker/<str:symbol>/", CombinedTickerDetailView.as_view(), name="ticker-detail"), 
]

# register/
 # POST - Creates a new user account, and registers it in the Django DB, body should be a JSON object with the following fields: username, email, password, first_name, last_name

# token/
 # POST - Allows a user to login, returns a JWT access token and referesh token, body should be a JSON object with the following fields: username, password

# token/refresh/
 # POST - Allows a user to refresh their JWT access token, given a valid refresh token, returns a new JWT access token 
  # body should be a JSON object with the following fields: refresh : the refresh token

# profile/, proteced routes must pass the JWT token in Bearer Token Authorization header
 # GET - Allows a user to view their username, first name, last name, email
 # PUT - Allows a user to update their username, first name, last name, email, body should be a JSON object with the following fields: username, first_name, last_name, email
 # DELETE - Allows a user to delete their account

# password/change/, protected routes must pass the JWT token in Bearer Token Authorization header
  # PUT - Allows a user to change their password, body should be a JSON object with the following fields: old_password, new_password, returns a message if the password was changed successfully

# ticker/favorites/, protected routes must pass the JWT token in Bearer Token Authorization header
  # GET - Returns a list of tickers that the user has favorited, each with the fields: id, user, basic_data, favorited_at
  # POST - Adds a ticker to the user's favorites, body should be a JSON object with the following fields: ticker_symbol : the ticker symbol to be favorited
  # DELETE - Removes a ticker from the user's favorites, body should be a JSON object with the following fields: ticker_symbol : the ticker symbol to be removed from the favorites, returns a message if the ticker was removed successfully
    
# ticker/search/, protected routes must pass the JWT token in Bearer Token Authorization header
  # GET - Searches for tickers by symbol, returns a list of tickers that match the search query, search query should be a symbol
    # Query Params: symbol(requierd), limit(optional) - number of results to return, default is 10

# ticker/dashboard/
 # GET:
   # Protected: Requires a valid JWT token in the Authorization header
     # Returns basic + detailed ticker data for the authenticated users's favorite tickers, as well as general news articles about business
   # Not Proteched:
     # Returns basic + detailed ticker data for AAPL, NVDA, TSLA, MSFT, AMZN, and the top stories/news about business

# ticker/<str:symbol>/
 # GET:
   # Returns basic, detailed, and historical ticker data for a specified ticker, as well as the latest news articles about the ticker
     
     