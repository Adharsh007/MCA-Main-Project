from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
#model used to store additional features of manager other than from the user table
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    Address = models.TextField(blank = True)
    #Address2 = models.CharField(max_length = 30)
    #City = models.CharField(max_length = 30)
    Contact = models.IntegerField()

    def __str__(self):
        return self.user.username
#Model used to register team
class AddTeam(models.Model):
    team_name = models.CharField(max_length=40)
    username = models.ForeignKey(User)
    address = models.TextField()
    contact_no = models.IntegerField()
    team_logo = models.ImageField(upload_to='teams_logo/')

    def __str__(self):
        return self.team_name

#moder for add players
class AddPlayer(models.Model):
    POSITION_CHOICES = (('Striker','Striker'),('MidFielder','MidFielder'),('Defender','Defender'),('GoalKeeper','GoalKeeper'))
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    team_name = models.ForeignKey(AddTeam)
    age = models.IntegerField()
    contact_no = models.IntegerField()
    address = models.TextField()
    jersy_no = models.IntegerField()
    position = models.CharField(max_length=25,choices=POSITION_CHOICES)
    upload_photo = models.ImageField(upload_to='players/')

    def __str__(self):
        return self.first_name

#model for adding tournment by admin
class AddTournments(models.Model):
    t_name =models.CharField(max_length=30)
    t_venue = models.CharField(max_length=30)
    s_date = models.DateTimeField(default=timezone.now)
    e_date = models.DateTimeField(default=timezone.now)
    r_fee = models.IntegerField()

    def __str__(self):
        return self.t_name