from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer, ChangePasswordSerializer, BasicTickerDataSerializer, HistoricalDataSerializer, DetailedTickerDataSerializer, FavoriteStockSerializer
from .models import BasicTickerData, DetailedTickerData, HistoricalData, FavoriteStock
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