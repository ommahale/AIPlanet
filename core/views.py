from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth.models import User

from drf_yasg.utils import swagger_auto_schema

from . import serializers
from .models import *
# Create your views here.


@api_view(["GET"])
def index(request):
    return Response({"message":"API View!"})

@swagger_auto_schema(request_body=serializers.UserSerializer,method="POST",responses={201:"Created",400:"Bad Request",500:"Internal Server Error"})
@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    if username is None or password is None or email is None:
        return Response({"error":"Please provide username, email and password"},status=status.HTTP_400_BAD_REQUEST)
    try:
        temp=User.objects.filter(username=username).first()
        if temp:
            return Response({"error":"Username already exists"},status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username,email=email,is_staff=True)
        user.set_password(password)
        user.save()
        return Response({"message":"User created successfully"},status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class CreateHackathonView(APIView):
    @swagger_auto_schema(request_body=serializers.SwaggerCreateHackathonSerializer,responses={201:"Created",400:"Bad Request",500:"Internal Server Error"})
    def post(self,request):
        try:
            user_email = request.data.get("user_email")
            user = User.objects.filter(email=user_email).first()
            if user is None:
                return Response({"error":"User not found"},status=status.HTTP_400_BAD_REQUEST)
            data = {
                "name":request.data.get("name"),
                "bg_image_url":request.data.get("bg_image_url"),
                "hackathon_image_url":request.data.get("hackathon_image_url"),
                "description":request.data.get("description"),
                "start_date":request.data.get("start_date"),
                "end_date":request.data.get("end_date"),
                "reward_prize":request.data.get("reward_prize"),
                "created_by":user.id
            }
            serializer=serializers.CreateHackathonSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Hackathon created successfully","data":serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
