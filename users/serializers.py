from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    # Ensures password is only used for writing and not returned
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            # This ensures password is not returned in API responses.
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_instance = CustomUser(**validated_data)
        user_instance.set_password(password)
        user_instance.save()
        return user_instance
