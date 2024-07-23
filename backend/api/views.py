from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer, ChangePasswordSerializer, BasicTickerDataSerializer, HistoricalTickerDataSerializer, DetailedTickerDataSerializer, FavoriteTickerDataSerializer
from .models import BasicTickerData, DetailedTickerData, HistoricalTickerData, FavoriteTickerData
from datetime import date, timedelta
from .helper_functions import get_detailed_data, get_historical_data, is_most_recent_friday

# Registering a User
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()  # Queryset to retrieve all user objects
    serializer_class = UserSerializer  # Serializer class to handle user data
    permission_classes = [AllowAny]  # Allow any user to access this view (no authentication required)

# Finding and showing the logged-in User
class UserProfileActions(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer  # Serializer class to handle user data
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def get_object(self):
        # Return the current logged-in user
        return self.request.user

# Changing the User's Password
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)  # Initialize the serializer with request data
        if serializer.is_valid():
            user = request.user
            # Check if the old password is correct
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))  # Set the new password
                user.save()  # Save the user with the new password
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Returning information about a specific ticker for the detail view
class CombinedTickerDetailView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view (no authentication required)

    def get(self, request, symbol):
        try:
            # Get the BasicTickerData object from the database
            ticker_info = BasicTickerData.objects.get(symbol=symbol)
        except BasicTickerData.DoesNotExist:
            return Response({"error": "Ticker not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check if detailed_data exists, if it does then grab it from the database, if not then call FMP API to get detailed data and store in the database
        if DetailedTickerData.objects.filter(basic_data=ticker_info).exists():
            detailed_data = DetailedTickerData.objects.get(basic_data=ticker_info)
        else:
            try:
                detailed_data = get_detailed_data(ticker_info.symbol)
                get_historical_data(ticker_info.symbol)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Get the latest historical data entry
            latest_entry = HistoricalTickerData.objects.filter(basic_data=ticker_info).order_by('-date').first()

            # Check if latest entry is up-to-date
            if latest_entry and latest_entry.date < date.today() and not is_most_recent_friday(latest_entry.date):
                get_historical_data(ticker_info.symbol, end_date=latest_entry.date + timedelta(days=1))
            elif not latest_entry:
                get_historical_data(ticker_info.symbol)

            # Serialize the data
            historical_info = HistoricalTickerDataSerializer(
                HistoricalTickerData.objects.filter(basic_data=ticker_info).order_by('-date'), many=True
            ).data
            basic_info = BasicTickerDataSerializer(ticker_info).data
            detailed_info = DetailedTickerDataSerializer(detailed_data).data

            # Return combined response
            return Response({
                'basic_info': basic_info,
                'detailed_info': detailed_info,
                'historical_info': historical_info
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FavoriteTickersView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def get(self, request):
        try:
            # Get the current logged-in user
            user_id = self.request.user.id
            # Get all the favorite tickers for the current user
            favorite_tickers = FavoriteTickerData.objects.filter(user_id=user_id)
            # Serialize the favorite tickers
            serializer = FavoriteTickerDataSerializer(favorite_tickers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            # Get the current logged-in user
            user_id = self.request.user.id
            # Get the ticker symbol from the request body
            ticker_symbol = request.data.get('ticker_symbol')
            basic_ticker = BasicTickerData.objects.get(symbol=ticker_symbol)
            # Check if the ticker is already favorited by the user
            if FavoriteTickerData.objects.filter(user_id=user_id, basic_data=basic_ticker).exists():
                return Response({"error": "Ticker already favorited."}, status=status.HTTP_400_BAD_REQUEST)
            # Create a new FavoriteTickerData object
            FavoriteTickerData.objects.create(
                user_id=user_id,
                basic_data=basic_ticker
            )
            return Response({"message": "Ticker added to favorites."}, status=status.HTTP_200_OK)
        except BasicTickerData.DoesNotExist:
            return Response({"error": "Ticker not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            # Get the current logged-in user
            user_id = self.request.user.id
            # Get the ticker symbol from the request body
            ticker_symbol = request.data.get('ticker_symbol')
            basic_ticker = BasicTickerData.objects.get(symbol=ticker_symbol)
            # Check if the ticker is already favorited by the user
            if not FavoriteTickerData.objects.filter(user_id=user_id, basic_data=basic_ticker).exists():
                return Response({"error": "Ticker not favorited."}, status=status.HTTP_400_BAD_REQUEST)
            # Delete the FavoriteTickerData object
            FavoriteTickerData.objects.filter(user_id=user_id, basic_data=basic_ticker).delete()
            return Response({"message": "Ticker removed from favorites."}, status=status.HTTP_200_OK)
        except BasicTickerData.DoesNotExist:
            return Response({"error": "Ticker not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)