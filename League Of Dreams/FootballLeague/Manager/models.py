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
    username = models.ForeignKey(User,on_delete=models.CASCADE)
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
    team_name = models.ForeignKey(AddTeam,on_delete=models.CASCADE)
    age = models.IntegerField()
    contact_no = models.IntegerField()
    address = models.TextField()
    jersy_no = models.IntegerField()
    position = models.CharField(max_length=25,choices=POSITION_CHOICES)
    upload_photo = models.ImageField(upload_to='players/')

    def __str__(self):
        return str(self.id)



#model for adding news from admin
class AddNews(models.Model):
    news_image = models.ImageField(upload_to='news/')
    news_head = models.CharField(max_length=150)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.news_head

#model for adding tournment by admin
class AddTournments(models.Model):
    t_name =models.CharField(max_length=30)
    t_venue = models.CharField(max_length=30)
    s_date = models.DateTimeField(default=timezone.now)
    e_date = models.DateTimeField(default=timezone.now)
    r_fee = models.IntegerField()

    def __str__(self):
       return self.t_name

#model for tournment registration
class TournmentRegistration(models.Model):
    tr_name = models.ForeignKey(AddTournments,on_delete=models.CASCADE)
    team_name = models.ForeignKey(AddTeam, on_delete=models.CASCADE)
    is_registred = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

#model for adding fixture
class AddFixture_table(models.Model):
    tr_name = models.ForeignKey(AddTournments,on_delete=models.CASCADE)
    team_one = models.CharField(max_length=30)
    team_two = models.CharField(max_length=30)
    match_name = models.CharField(max_length=50)
    match_date = models.DateField()
    match_time = models.TimeField()
    venue = models.CharField(max_length=30)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.match_name

#model for adding point
class AddPoints(models.Model):
    tourn_name_id= models.ForeignKey(AddTournments,on_delete=models.CASCADE)
    m_name= models.ForeignKey(AddFixture_table,on_delete=models.CASCADE)
    team_one = models.CharField(max_length=20)
    team_two= models.CharField(max_length=20)
    team_1_goal = models.IntegerField()
    team_2_goal = models.IntegerField()
    winner = models.CharField(max_length=30)
    looser = models.CharField(max_length=30)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

#model for adding goals and assust
class AddGoalsandAssist(models.Model):
    tour_name= models.ForeignKey(AddTournments,on_delete=models.CASCADE)
    matchname = models.ForeignKey(AddFixture_table,on_delete=models.CASCADE)
    Scorer_name = models.CharField(max_length=20)
    assist_name = models.CharField(max_length=20, blank=True , null=True)
    team_name = models.ForeignKey(AddTeam,on_delete=models.CASCADE)
    g_time = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id)

#model for goal keeper saves
class AddGoalKeeperSaves(models.Model):
    tour_name= models.ForeignKey(AddTournments,on_delete=models.CASCADE)
    matchname = models.ForeignKey(AddFixture_table,on_delete=models.CASCADE)
    gk_names = models.CharField(max_length=20)
    saves = models.IntegerField()
    team_name = models.ForeignKey(AddTeam,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

#model for new goalkeeper
class NewKeeper(models.Model):
    tour_name= models.ForeignKey(AddTournments,on_delete=models.CASCADE)
    matchname = models.ForeignKey(AddFixture_table,on_delete=models.CASCADE)
    gk_name = models.ForeignKey(AddPlayer,on_delete=models.CASCADE)
    saves = models.IntegerField()
    team_name = models.ForeignKey(AddTeam,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

#model for live scorer
class LiveScore(models.Model):
    f_id = models.ForeignKey(AddFixture_table,on_delete=models.CASCADE)
    team_name = team_name = models.ForeignKey(AddTeam, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Tie(models.Model):
    tourn_name_id= models.ForeignKey(AddTournments,on_delete=models.CASCADE)
    m_name= models.ForeignKey(AddFixture_table,on_delete=models.CASCADE)
    team_one = models.CharField(max_length=20)
    team_two= models.CharField(max_length=20)
    team_1_goal = models.IntegerField()
    team_2_goal = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Tie(models.Model):
    tourn_name_id= models.ForeignKey(AddTournments,on_delete=models.CASCADE)
    m_name= models.ForeignKey(AddFixture_table,on_delete=models.CASCADE)
    team_one = models.CharField(max_length=20)
    team_two= models.CharField(max_length=20)
    team_1_goal = models.IntegerField()
    team_2_goal = models.IntegerField()

    def __str__(self):
        return str(self.id)
