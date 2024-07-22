from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer, ChangePasswordSerializer, BasicTickerDataSerializer, HistoricalTickerDataSerializer, DetailedTickerDataSerializer, FavoriteTickerDataSerializer
from .models import BasicTickerData, DetailedTickerData, HistoricalTickerData, FavoriteTickerData
from datetime import date

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

class CombinedTickerDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def get(self, request, symbol):
        try:
            # Get the BasicTickerData object from the database abd serialize it
            ticker_info = BasicTickerData.objects.get(symbol=symbol)
            basic_info = BasicTickerDataSerializer(ticker_info).data
        except BasicTickerData.DoesNotExist:
            return Response({"error": "Ticker not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if detailed_data exists, if it does then grab it from the database, if not then call FMP API to get detailed data AND historical data and store in the database
        if hasattr(ticker_info, 'detailed_data'):
            detailed_data = ticker_info.detailed_data
        else:
            # Placeholder for future code to fetch and store detailed data and historical data, 
            # no need to store historical data in RAM since it will be stored later in the function, but make sure to store detailed_data in RAM here
            pass  

        # Serialize data
        detailed_info = DetailedTickerDataSerializer(detailed_data).data
        
        # Get the latest historical data entry
        latest_entry = HistoricalTickerData.objects.filter(basic_data=ticker_info).order_by('-date').first()

        # Check if latest entry is up-to-date
        if latest_entry and latest_entry.date == date.today():
            # Serialize data and return
            historical_info = HistoricalTickerDataSerializer(
                HistoricalTickerData.objects.filter(basic_data=ticker_info).order_by('-date'), many=True
            ).data

            # Return combined response
            return Response({
                'basic_info': basic_info,
                'detailed_info': detailed_info,
                'historical_info': historical_info
            }, status=status.HTTP_200_OK)
        
        elif latest_entry and latest_entry.date < date.today():
            # Call the FMP API to fill the database with the data from today's date to latest_entry date, exclude the latest_entry date
            pass  # Placeholder for future code to update historical data
        else:
            # Call the FMP API to fill the database with historical data, straight from the FMP API, no need to include dates, this assumes latest_entry is null … 
            pass  # Placeholder for future code to fetch historical data
        
        # Return combined response
        historical_info = HistoricalTickerDataSerializer(
                HistoricalTickerData.objects.filter(basic_data=ticker_info).order_by('-date'), many=True
            ).data
        
        return Response({
            'basic_info': basic_info,
            'detailed_info': detailed_info,
            'historical_info': historical_info
        }, status=status.HTTP_200_OK)