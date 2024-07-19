from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')  # Extract the password
        user = User(**validated_data)  # Create user instance without saving to the database
        user.set_password(password)  # Set the password using set_password() to ensure it is hashed
        user.save()  # Save the user instance to the database
        return user
