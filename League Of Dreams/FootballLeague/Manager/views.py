from django.shortcuts import render
from Manager.forms import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from Manager.models import *
from django.db import connection
from django.views.generic import ListView,DetailView
from Manager import config
import itertools

# Create your views here.

#to display the first loading page
def index_view(request):
    return render(request,'manager/index.html')

#to display data from the user table for signup
def signup_view(request):
    form = SignUpForm()
    profileform = UserProfileForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profileform = UserProfileForm(request.POST)

        if form.is_valid() and profileform.is_valid():
            user=form.save()
            profile = profileform.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/')
    return render(request,'Manager/signup.html',{'profileform':profileform, 'form':form})

#to display login page
def login_view(request):
    return render(request,'Manager/login.html')


#to check login and  display home page
def home_view(request):
    if request.method=='POST':
        un = request.POST.get('uname')
        pw = request.POST.get('pwd')
        user = authenticate(request, username=un, password=pw)
        config.userid = user.id
        user_obj = User.objects.get(id=config.userid)
        print("inside home view")
        print(config.userid)
        print(user_obj)
        request.session['loginid'] = user.id


        if user:
            if user.is_superuser == 1 and user.is_staff ==1:
                return render(request,'Manager/adminpage.html')
            elif user:
                #need
                #team_obj = AddTeam.objects.get(username=user_obj)
                #config.teamid = team_obj.id
                return render(request, 'Manager/home.html')
            else:
                return HttpResponse('Invalid')

        else:
            return HttpResponse('Invalid')

    return render(request, 'Manager/home.html')

#adding new team
def addteam_view(request):
    teamform = AddTeamForm()
    if request.method == 'POST':
        teamform = AddTeamForm(request.POST, request.FILES)
        if teamform.is_valid():
            teamform.save()
            return redirect('/home')
    return render(request,'Manager/addteam.html',{'teamform':teamform})

#Adding a player
def addplayer_view(request):
    player = AddPlayerForm()
    if request.method == 'POST':
        player = AddPlayerForm(request.POST,request.FILES)
        if player.is_valid():
            player.save()
            return redirect('/home')
    return render(request,'Manager/addplayer.html',{'player':player})


#load admin page
def load_admin_view(request):
    return render(request, 'Manager/adminpage.html')



#To add news from the admin side
def addnews_view(request):
    newsform = AddNewsForm()
    if request.method == 'POST':
        newsform = AddNewsForm(request.POST, request.FILES)
        if newsform.is_valid():
            newsform.save()
            return redirect('/admpg')
    return render(request,'Manager/addnews.html',{'newsform':newsform})

#list the news
class NewsList(ListView):
    model = AddNews
    context_object_name = 'AddNews_list'

#detail news list
class NewsDetail(DetailView):
    model= AddNews
    context_object_name = 'mynews'


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


#view team
def view_team(request):
    x = (request.session.get('loginid'))
    print(x)

    cursor = connection.cursor()
    cursor.execute("""
    SELECT
    Manager_addplayer.*
    FROM
    auth_user left outer join  Manager_addteam
    ON
    (auth_user.id=Manager_addteam.username_id)
    left outer JOIN Manager_addplayer
    on
    (Manager_addplayer.team_name_id = Manager_addteam.id)
    WHERE auth_user.id = %d"""%(x))

    dict = {}
    dict = dictfetchall(cursor)
    print(dict)
    context = {
        'dict': dict
    }
    return render(request, 'manager/myteam.html', context)

#To delete Player from list
def  delete_view(request,id):
    player_id = AddPlayer.objects.get(id=id)
    player_id.delete()
    return redirect('/myteam')

#to make payment for a tournment
def makepayment_view(request):
    return render(request,'Manager/payment.html')

#To display all the teams under club tab
class ClubListView(ListView):
    model = AddTeam
    template_name = 'Manager/listclubs.html'
    context_object_name = 'myclubs'

#display players belongs to each team
def playerlist_view(request, id):
    if request.method == "GET" :
        print("inside get")
        team_id = AddTeam.objects.get(id=id)
        print(team_id)
        print(team_id.id)
        playerlist = AddPlayer.objects.filter(team_name=team_id.id)
        print(playerlist)
        return render(request,'Manager/listplayers.html',{'playerlist':playerlist})

#Add tournmets from the admin home page
def addtournment_view(request):
    addtourform = AddTournmentsForm()
    if request.method=='POST':
        addtourform = AddTournmentsForm(request.POST)
        if addtourform.is_valid():
            addtourform.save()
            #TournmentRegistration.objects.create(tr_name=trnmnt, team_name= team_obj, is_registred= False)
            return redirect('/admpg')
    return render(request,'Manager/addtournment.html',{'addtourform':addtourform})

#view for tournment registration
def tournmentreg(request, id):
    registerform = TournmentRegistrationForm()
    if request.method == 'POST':
        registerform = TournmentRegistrationForm(request.POST)
        if registerform.is_valid():
            registerform.save()

    else:
        user_obj = User.objects.get(id=config.userid)
        team_obj = AddTeam.objects.get(username=user_obj)
        trnm_obj = AddTournments.objects.get(id=id)
        TournmentRegistration.objects.create(is_registred = False, team_name = team_obj, tr_name = trnm_obj)
        print("Insde views.py")
        return render(request,'Manager/tournmentregistration.html',{'registerform':registerform})

def show_tournments_view(request):
    print("Inside show tournment")
    print("***********************************************")
    #user_obj = User.objects.get(id=config.userid)
    #team_obj = AddTeam.objects.get(username=user_obj)
    user_obj = User.objects.get(id=config.userid)
    team_obj = AddTeam.objects.get(username=user_obj)
    x= team_obj.id
    y= user_obj.id

    print(team_obj)

    cursor = connection.cursor()
    cursor1 = connection.cursor()

    cursor.execute("""select DISTINCT Manager_addtournments.id,
	   Manager_addtournments.t_name,
	   Manager_addtournments.t_venue,
	   Manager_addtournments.s_date,
	   Manager_addtournments.e_date,
	   Manager_addtournments.r_fee
       from  Manager_addtournments
       LEFT OUTER JOIN Manager_tournmentregistration
       ON (Manager_addtournments.id = Manager_tournmentregistration.tr_name_id)
       where Manager_addtournments.id not in
       (SELECT tr_name_id from Manager_tournmentregistration WHERE team_name_id = %d) """%(x))

    cursor1.execute("""
    select t_name,t_venue,s_date,e_date,r_fee from Manager_addtournments
    LEFT OUTER JOIN Manager_tournmentregistration
    on
    (Manager_addtournments.id = Manager_tournmentregistration.tr_name_id)
    LEFT OUTER JOIN Manager_addteam
    on
    (Manager_tournmentregistration.team_name_id=Manager_addteam.id)
    where Manager_addteam.username_id= %d """%(y))


    dict = {}
    dict1 = {}

    dict = dictfetchall(cursor)
    dict1 = dictfetchall(cursor1)

    print(dict)
    print("Nedumbally")
    print(dict1)
    return render(request,'Manager/showtour.html', {'dict':dict, 'dict1':dict1} )

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Second LIfe %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#view shows list of available tournmets while click on add fixture from admin side
def fix_tour_list(request):
    tourlist_cursor =connection.cursor()
    tourlist_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
    """)
    tourlist_dict = {}
    tourlist_dict =dictfetchall(tourlist_cursor)
    print(tourlist_dict)
    return render(request,'Manager/fixture_tour_list.html',{'tourlist_dict':tourlist_dict})

#view for adding fixture from admin side
def add_fixture_admin(request, id):
    tour_id = AddTournments.objects.get(id=id)
    print(tour_id)
    admin_fixture = connection.cursor()
    admin_fixture.execute("""
        select Manager_tournmentregistration.team_name_id, Manager_addteam.team_name,
        Manager_addtournments.id,Manager_addtournments.t_name
        from
        Manager_tournmentregistration
        LEFT OUTER JOIN Manager_addteam
        on
        (Manager_tournmentregistration.team_name_id = Manager_addteam.id)
        LEFT outer JOIN
        Manager_addtournments
        on (Manager_tournmentregistration.tr_name_id= Manager_addtournments.id)
        WHERE
        Manager_tournmentregistration.tr_name_id= %d """%(int(tour_id.id)))
    admin_fixture_dict = {}
    admin_fixture_dict = dictfetchall(admin_fixture)
    print("******************inside admin fixture**************")
    print(admin_fixture_dict)
    return render(request, 'Manager/addfixture.html',{'admin_fixture_dict':admin_fixture_dict, 'tour_id':tour_id })

#Adding value to the fixture table
def fixture_table(request):
    if request.method=='POST':
        tour_name = request.POST.get('trname')
        tourn_name_id = AddTournments.objects.get(t_name=tour_name)
        t1=request.POST.get('team1')
        t2=request.POST.get('team2')
        fdate=request.POST.get('fdate')
        ftime=request.POST.get('ftime')
        fvenue=request.POST.get('fvenue')
        matchname = request.POST.get('mname')
        print("Inside adding in to fixture table")
        print(tour_name)
        print(tourn_name_id)
        print(t1)
        print(t2)
        print(fdate)
        print(ftime)
        print(fvenue)
        print(matchname)
        ob= AddFixture_table.objects.create(tr_name=tourn_name_id,team_one=t1,team_two=t2,match_name=matchname,
        match_date=fdate,match_time=ftime,venue=fvenue)
        ob.save()
        return redirect("/tourlist")

# ***************************** Add POints *********************
#view shows list of available tournmets while click on add points from admin side
def point_tour_list(request):
    tourlist1_cursor =connection.cursor()
    tourlist1_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
    """)
    tourlist1_dict = {}
    tourlist1_dict =dictfetchall(tourlist1_cursor)
    print(tourlist1_dict)
    return render(request,'Manager/point_tour_list.html',{'tourlist1_dict':tourlist1_dict})

#view for adding points from admin Inside
def add_points_admin(request, id):
    tour_id = AddTournments.objects.get(id=id)
    print(tour_id)

    point_cursor = connection.cursor()
    point_cursor.execute("""
    SELECT Manager_addfixture_table.match_name
    from Manager_addfixture_table
    where Manager_addfixture_table.tr_name_id=%d"""%(int(tour_id.id)))
    point_dict = {}
    point_dict= dictfetchall(point_cursor)
    print("Inside add points")
    print(point_dict)

    team_cursor = connection.cursor()
    team_cursor.execute("""
	select DISTINCT ma1.team_name as "Team1", ma2.team_name as "Team2", mat.match_name, mat.match_date, mat.match_time,mat.id
	from Manager_addfixture_table mat
	left outer join Manager_addteam ma1 on ma1.team_name = mat.team_one
	left outer join Manager_addteam ma2 on ma2.team_name = mat.team_two
	where mat.tr_name_id = %d"""%(int(tour_id.id)))
    team_dict = {}
    team_dict= dictfetchall(team_cursor)
    print("Inside team names")
    print(team_dict)
    return render(request,'Manager/addpoints.html',{'point_dict':point_dict , 'tour_id':tour_id , 'team_dict':team_dict})

#adding values  to point point_table
def point_table(request):
        if request.method == 'POST':
            tour_name = request.POST.get('trname')
            tourn_name_id = AddTournments.objects.get(t_name=tour_name)
            m_name = request.POST.get('matchname')
            match_name = AddFixture_table.objects.get(match_name=m_name)
            team_one = request.POST.get('team1')
            team_two = request.POST.get('team2')
            team_1_goal = request.POST.get('t1goals')
            team_2_goal = request.POST.get('t2goals')
            team_1_point=request.POST.get('t1point')
            team_2_point=request.POST.get('t2point')
            print("inside point table")
            print(tour_name)
            print(tourn_name_id)
            print(m_name)
            print(team_one)
            print(team_two)
            print(team_1_goal)
            print(team_2_goal)
            print(team_1_point)
            print(team_2_point)
            ob= AddPoints.objects.create(tourn_name_id=tourn_name_id ,m_name=match_name ,team_one=team_one,
            team_two=team_two,team_1_goal=team_1_goal,team_2_goal=team_2_goal,team_1_point=team_1_point,team_2_point=team_2_point)
            ob.save()
            return redirect("/point_tourlist")


#view shows list of available tournmets while click on standings tab from index page
def standing_tour_list(request):
    tourlist_cursor =connection.cursor()
    tourlist_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
    """)
    tourlist_dict = {}
    tourlist_dict =dictfetchall(tourlist_cursor)
    print(tourlist_dict)
    return render(request,'Manager/standings_tour_list.html',{'tourlist_dict':tourlist_dict})

#View for showing standing list
def standing_list(request,id):
    tour_id = AddTournments.objects.get(id=id)
    print("Name of the tournmet is")
    print(tour_id)

    team_list=connection.cursor()
    team_list.execute("""
    SELECT Manager_addteam.id, Manager_addteam.team_name
    FROM Manager_addteam
    LEFT OUTER JOIN Manager_tournmentregistration
    on (Manager_addteam.id= Manager_tournmentregistration.team_name_id)
    where Manager_tournmentregistration.tr_name_id=%s"""%(int(tour_id.id)))
    team_list_dict = {}
    team_list_dict =dictfetchall(team_list)
    print(team_list_dict)
    t_count1_dict={}
    t_count2_dict={}
    t_count3_dict={}
    print("******** Team 1 list is ************")
    for i in team_list_dict:
        t_count1 = connection.cursor()
        t_count1.execute("""
        select Manager_addteam.id,Manager_addpoints.team_one,count(*) As count
        from Manager_addpoints
        LEFT OUTER JOIN Manager_addteam
        on(Manager_addteam.team_name=Manager_addpoints.team_one)
        where Manager_addteam.id=%d"""%(i['id']))
        t_count1_dict=dictfetchall(t_count1)
        print(t_count1_dict)
    print("******** Team 2 list is ************")
    for x in team_list_dict:
        t_count2 = connection.cursor()
        t_count2.execute("""
        select Manager_addteam.id,Manager_addpoints.team_two,count(*) As count
        from Manager_addpoints
        LEFT OUTER JOIN Manager_addteam
        on(Manager_addteam.team_name=Manager_addpoints.team_two)
        where Manager_addteam.id=%d"""%(x['id']))
        t_count2_dict=dictfetchall(t_count2)

        print(t_count2_dict)
