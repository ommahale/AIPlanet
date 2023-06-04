from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Members(BaseModel):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    def __str__(self):
        return self.name
class Hackathon(BaseModel):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bg_image_url = models.URLField()
    hackathon_image_url = models.URLField()
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    reward_prize = models.FloatField(max_length=100)
    def __str__(self):
        return self.name

class HackathonTeam(BaseModel):
    hackathon = models.ForeignKey(Hackathon,on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    team_captain = models.ForeignKey(Members,on_delete=models.CASCADE,related_name="team_captain")
    team_members = models.ManyToManyField(Members,related_name="team_members",blank=True)
    def __str__(self):
        return self.team_name

class HackathonSubmission(BaseModel):
    hackathon = models.ForeignKey(Hackathon,on_delete=models.CASCADE)
    team = models.ForeignKey(HackathonTeam,on_delete=models.CASCADE)
    summary = models.TextField(default="")
    submission_url = models.URLField()
    def __str__(self):
        return self.team.team_name
    class Meta:
        unique_together = ['hackathon','team']

