from rest_framework import serializers

from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","password","email"]
        extra_kwargs = {
            "password":{"write_only":True}
        }

class SwaggerCreateHackathonSerializer(serializers.ModelSerializer):
    user_email=serializers.CharField()
    class Meta:
        model = Hackathon
        fields = [
            "name",
            "bg_image_url",
            "hackathon_image_url",
            "description",
            "start_date",
            "end_date",
            "reward_prize",
            "user_email"
        ]

class CreateHackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = [
            "name",
            "bg_image_url",
            "hackathon_image_url",
            "description",
            "start_date",
            "end_date",
            "reward_prize",
            "created_by"
        ]
