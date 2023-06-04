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



'''

API to create a user (Sign Up)

'''
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
    

'''
API to create a hackathon
'''
class CreateHackathonView(APIView):
    @swagger_auto_schema(request_body=serializers.SwaggerCreateHackathonSerializer,responses={201:"Created",400:"Bad Request",500:"Internal Server Error"})
    def post(self,request):
        if request.user.is_anonymous:
            return Response({"error":"Please login to create hackathon"},status=status.HTTP_401_UNAUTHORIZED)
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


'''
API to list all hackathons
'''
class ListHackathonView(generics.ListAPIView):
    serializer_class = serializers.ListHackathonSerializer
    def list(self, request, *args, **kwargs):
        try:
            queryset = Hackathon.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response({"message":"Hackathon list","data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

'''
API to register a team for a hackathon
'''
class RegisterTeamAPIView(APIView):
    @swagger_auto_schema(request_body=serializers.CreateTeamSerializer,responses={201:"Created",400:"Bad Request",500:"Internal Server Error"})
    def post(self,request):
        serializer = serializers.CreateTeamSerializer(data=request.data)
        if serializer.is_valid():
            
                hackathon_id = request.data.get("hackathon")
                team_name = request.data.get("team_name")
                team_captain_name = request.data.get("team_captain")["name"]
                team_captain_email = request.data.get("team_captain")["email"]
                team_members = request.data.get("team_members")
                
                hackathon = Hackathon.objects.filter(id=hackathon_id).first()

                if hackathon is None:
                    return Response({"error":"Hackathon not found"},status=status.HTTP_400_BAD_REQUEST)
                team_captain = Members.objects.filter(name=team_captain_name,email=team_captain_email).first()
                
                if team_captain is None:
                    team_captain = Members.objects.create(name=team_captain_name,email=team_captain_email)
                temp = HackathonTeam.objects.filter(hackathon=hackathon,team_name=team_name,team_captain=team_captain).first()
                if temp:
                    return Response({"error":"Team already exists"},status=status.HTTP_400_BAD_REQUEST)
                team = HackathonTeam.objects.create(hackathon=hackathon,team_name=team_name,team_captain=team_captain)
                
                if team_members is not None:
                    for i in team_members:
                        member = Members.objects.filter(name=i["name"],email=i["email"]).first()
                        if member is None:
                            member = Members.objects.create(name=i["name"],email=i["email"])
                        team.team_members.add(member)
                
                team.save()
                return Response({"message":"Team registered successfully","team":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

'''
API to list all hackathons registered by a user
format : {
    "email":"team_captain_email",
    "name":"team_captain_name"
}
'''

@swagger_auto_schema(method="GET",responses={200:"OK",400:"Bad Request",500:"Internal Server Error"})
@api_view(["GET"])
def get_user_registrations(request):
    try:
        user_email = request.data.get("email")
        user_name = request.data.get("name")
    
        team=HackathonTeam.objects.filter(team_captain__name=user_name,team_captain__email=user_email)
        if team is None:
            return Response({"error":"Team not found"},status=status.HTTP_404_NOT_FOUND)
        data=serializers.ListTeamSerializer(team,many=True).data
        return Response({"message":"Team list","data":data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


'''
API to create submissions for a hackathon
'''
class CreateSubmissionAPIView(generics.CreateAPIView):
    serializer_class = serializers.CreateSubmissionSerializer
    @swagger_auto_schema(request_body=serializers.CreateSubmissionSerializer,responses={201:"Created",400:"Bad Request",500:"Internal Server Error"})
    def create(self, request, *args, **kwargs):
        try:
            hackathon_id = request.data.get("hackathon")
            team_id = request.data.get("team")
            summary = request.data.get("summary")
            submission_url = request.data.get("submission_url")
            hackathon = Hackathon.objects.filter(id=hackathon_id).first()
            team = HackathonTeam.objects.filter(id=team_id).first()
            if hackathon is None or team is None:
                return Response({"error":"Hackathon or Team not found"},status=status.HTTP_404_NOT_FOUND)
            temp = HackathonSubmission.objects.filter(hackathon=hackathon,team=team).first()
            if temp:
                return Response({"error":"Submission already exists"},status=status.HTTP_400_BAD_REQUEST)
            submission = HackathonSubmission.objects.create(hackathon=hackathon,team=team,summary=summary,submission_url=submission_url)
            submission.save()
            return Response({"message":"Submission created successfully","submission_id":submission.id},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def get_hackathon_submissions(request,team_id):
    try:
        team = HackathonTeam.objects.filter(id=team_id).first()
        if team is None:
            return Response({"error":"Team not found"},status=status.HTTP_404_NOT_FOUND)
        submissions = HackathonSubmission.objects.filter(team=team)
        data = serializers.ListSubmissionSerializer(submissions,many=True).data
        return Response({"message":"Submission list","data":data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)