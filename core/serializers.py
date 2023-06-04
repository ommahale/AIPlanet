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

class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email"]

class ListHackathonSerializer(serializers.ModelSerializer):
    created_by = UserViewSerializer()
    class Meta:
        model = Hackathon
        depth = 2
        fields = [
            "id",
            "name",
            "bg_image_url",
            "hackathon_image_url",
            "description",
            "start_date",
            "end_date",
            "reward_prize",
            "created_by"
        ]

class CreateMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ["name","email"]

class CreateTeamSerializer(serializers.ModelSerializer):
    team_captain = CreateMemberSerializer()
    team_members = CreateMemberSerializer(many=True,required=False)
    class Meta:
        model = HackathonTeam
        fields = ["hackathon","team_name","team_captain","team_members"]

class GetMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ["name","email","id"]

class ListTeamSerializer(serializers.ModelSerializer):
    team_captain = GetMemberSerializer()
    team_members = GetMemberSerializer(many=True)
    class Meta:
        model = HackathonTeam
        fields = ["id","team_name","team_captain","team_members"]

class CreateSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonSubmission
        fields = ["hackathon","team","summary","submission_url"]

class ListSubmissionSerializer(serializers.ModelSerializer):
    team = ListTeamSerializer()
    class Meta:
        model = HackathonSubmission
        fields = ["id","team","summary","submission_url"]