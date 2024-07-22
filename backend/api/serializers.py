from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import BasicTickerData, DetailedTickerData, HistoricalTickerData, FavoriteTickerData

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Password field, write-only and not required

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]  # Fields to be serialized

    def validate_username(self, value):
        # Check if a user with the given username already exists
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        # Check if a user with the given email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate_password(self, value):
        # Validate the password using Django's built-in validators
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # Extract the password from validated data
        user = User(**validated_data)  # Create a User instance with the remaining validated data
        if password:
            user.set_password(password)  # Set the password securely
        user.save()  # Save the user instance to the database
        return user

    def update(self, instance, validated_data):
        # Ensure password cannot be updated through this serializer
        if 'password' in validated_data:
            raise ValidationError("You cannot change your password through this serializer.")
        
        # Update the user instance with the provided validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  # Save the updated user instance
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)  # Field for the old password, required
    new_password = serializers.CharField(required=True)  # Field for the new password, required

    def validate_new_password(self, value):
        # Validate the new password using Django's built-in validators
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

class BasicTickerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicTickerData
        fields = ['id', 'symbol', 'exchange', 'exchangeShortName', 'name', 'price', 'type']

class DetailedTickerDataSerializer(serializers.ModelSerializer):
    basic_data = BasicTickerDataSerializer()

    class Meta:
        model = DetailedTickerData
        fields = [
            'id', 'basic_data', 'currency', 'changes', 'ipoDate', 'beta', 'volAvg', 'mktCap', 'lastDiv', 'range',
            'cik', 'cusip', 'industry', 'website', 'description', 'ceo', 'sector', 'country', 'fullTimeEmployees',
            'phone', 'address', 'city', 'state', 'zip', 'dcfDiff', 'dcf', 'image', 'defaultImage', 'isEtf',
            'isActivelyTrading', 'isAdr', 'isFund', 'isin'
        ]

class HistoricalTickerDataSerializer(serializers.ModelSerializer):
    basic_data = BasicTickerDataSerializer()
    detailed_data = DetailedTickerDataSerializer()

    class Meta:
        model = HistoricalTickerData
        fields = [
            'id', 'basic_data', 'detailed_data', 'date', 'open', 'high', 'low', 'close', 'adjClose', 'volume',
            'unadjustedVolume', 'change', 'changePercent', 'vwap', 'label', 'changeOverTime'
        ]

class FavoriteTickerDataSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    basic_data = BasicTickerDataSerializer()
    detailed_data = DetailedTickerDataSerializer()

    class Meta:
        model = FavoriteTickerData
        fields = ['id', 'user', 'basic_data', 'detailed_data', 'favorited_at']