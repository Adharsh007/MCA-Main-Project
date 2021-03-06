from django.shortcuts import render
from Manager.forms import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate,logout
from django.http import HttpResponse,HttpResponseRedirect
from Manager.models import *
from django.db import connection
from django.views.generic import ListView,DetailView
from Manager import config
import itertools
from Manager.utils import *
import datetime
from django.contrib import messages
import json
from django.http import JsonResponse
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse



# Create your views here.

#to display the first loading page
def index_view(request):
    return render(request,'manager/index.html')

#to display the new loading page
def load_view(request):
    return render(request,'manager/load.html')

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
        if user:
            config.userid = user.id
            user_obj = User.objects.get(id=config.userid)
            print("inside home view")
            print(config.userid)
            print(user_obj)
            request.session['loginid'] = user.id
            if user.is_superuser == 1 and user.is_staff ==1:
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

                # counting number of team registred for each tournment
                team_count_cursor = connection.cursor()
                team_count_cursor.execute("""select  Manager_addtournments.id,
		        Manager_addtournments.t_name,
		        count(Manager_tournmentregistration.tr_name_id) As count
                from  Manager_addtournments LEFT OUTER join Manager_tournmentregistration
                on (Manager_addtournments.id = Manager_tournmentregistration.tr_name_id)
                GROUP by Manager_addtournments.t_name""")
                team_list_new_dict = {}
                team_list_new_dict = dictfetchall(team_count_cursor)
                print("Team list is")
                print(team_list_new_dict)
                print("**** # Now u r time *****")
                #print(team_list_new_dict[t_name])
                label =[]
                for i in range(len(team_list_new_dict)):
                    label.append(team_list_new_dict[i]['t_name'])

                print(label)

                count = []
                for i in range(len(team_list_new_dict)):
                    count.append(team_list_new_dict[i]['count'])
                print(count)





                return render(request,'Manager/adminpage.html',{'tourlist_dict':tourlist_dict, 'team_list_new_dict':team_list_new_dict})
            elif user:
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

                # counting number of team registred for each tournment
                team_count_cursor = connection.cursor()
                team_count_cursor.execute("""select  Manager_addtournments.id,
		        Manager_addtournments.t_name,
		        count(Manager_tournmentregistration.tr_name_id) As count
                from  Manager_addtournments LEFT OUTER join Manager_tournmentregistration
                on (Manager_addtournments.id = Manager_tournmentregistration.tr_name_id)
                GROUP by Manager_addtournments.t_name""")
                team_list_new_dict = {}
                team_list_new_dict = dictfetchall(team_count_cursor)
                print("Team list is")
                print(team_list_new_dict)
                print("**** # Now u r time *****")
                #print(team_list_new_dict[t_name])
                label =[]
                for i in range(len(team_list_new_dict)):
                    label.append(team_list_new_dict[i]['t_name'])

                print(label)

                count = []
                for i in range(len(team_list_new_dict)):
                    count.append(team_list_new_dict[i]['count'])
                print(count)
                return render(request, 'Manager/home.html',{'tourlist_dict':tourlist_dict, 'team_list_new_dict':team_list_new_dict,'user_obj':user_obj})
            else:
                return HttpResponse('Invalid')

        else:
            # return HttpResponse('Invalid')
            messages.error(request, 'Invalid credentials !')
            return redirect('/login')

    return render(request, 'Manager/home.html')

#adding new team
def addteam_view(request):
    print("Inside Add Team")
    user_obj = User.objects.get(id=config.userid)
    x =config.userid
    print(user_obj)
    print(x)
    manager_count_cursor = connection.cursor()
    manager_count_cursor.execute("""
    select count(auth_user.username) as count,
	auth_user.username,
    Manager_addteam.team_name
	from Manager_addteam LEFT OUTER join auth_user
	on(auth_user.id=Manager_addteam.username_id)
	where auth_user.username='%s'
    """%(user_obj))
    manager_count_dict = {}
    manager_count_dict = dictfetchall(manager_count_cursor)
    print("check")
    print(manager_count_dict)
    print(manager_count_dict[0]['count'])
    c = manager_count_dict[0]['count']
    d = manager_count_dict[0]['team_name']
    if c>0 :
        # return HttpResponse('<h1> You have alreay registred your team </h1>')
        return render(request, 'Manager/addteam_error.html',{'user_obj':user_obj,'manager_count_dict':manager_count_dict,'d':d})
    else:

        manager_nm = User.objects.get(id=x)
        teamform = AddTeamForm()
        if request.method == 'POST':
            teamform = AddTeamForm(request.POST, request.FILES)
            if teamform.is_valid():
                team=teamform.save(commit=False)
                team.username=manager_nm
                team.save()
                return redirect('/home')
        return render(request,'Manager/addteam.html',{'teamform':teamform,'user_obj':user_obj})


#Adding a player
def addplayer_view(request):
    print("Inside Add player")

    print(config.userid)
    x=config.userid
    team = AddTeam.objects.get(username=x)
    print("Team")
    print(team)
    user_obj = User.objects.get(id=config.userid)
    print(user_obj)
    player= AddPlayerForm()
    if request.method == 'POST':
        player = AddPlayerForm(request.POST,request.FILES)
        if player.is_valid():
            pp= player.save(commit=False)
            pp.team_name= team
            pp.save()
            return redirect('/myteam')
    return render(request,'Manager/addplayer.html',{'player':player,'user_obj':user_obj})


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
    user_obj = User.objects.get(id=config.userid)
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
    # return render(request, 'manager/myteam.html', context)
    return render(request, 'manager/myteam.html', {'dict': dict, 'user_obj':user_obj})

#To delete Player from list
def  delete_view(request,id):
    player_id = AddPlayer.objects.get(id=id)
    player_id.delete()
    return redirect('/myteam')

def  update_view(request,id):
    player_id = AddPlayer.objects.get(id=id)
    if request.method == 'POST':
        form = AddPlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/myteam')
    return render(request,'Manager/updateplayer.html',{'player_id':player_id})

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

#display the details of players
def playerdetail_view(request,id):
    if request.method == 'GET':
        print("inside Player profile")
        player = AddPlayer.objects.get(id=id)
        player_id = player.id
        #print(player.id)class="img-responsive" style="width: 100%; float: left; margin-right: 10px;"
        player_cursor = connection.cursor()
        player_cursor.execute("""select Manager_addplayer.first_name || ' ' || Manager_addplayer.last_name As name,
	           Manager_addteam.team_name,
	           Manager_addplayer.age,
	           Manager_addplayer.contact_no,
	           Manager_addplayer.jersy_no,
	           Manager_addplayer.position,
	           Manager_addplayer.address,
	           Manager_addplayer.upload_photo
               from Manager_addteam
               left outer join Manager_addplayer
               on (Manager_addteam.id=Manager_addplayer.team_name_id)
               WHERE Manager_addplayer.id=%d """%(player_id))
        player_profile_dict ={}
        player_profile_dict = dictfetchall(player_cursor)
        print(player_profile_dict)
        return render(request,'Manager/player_profile.html',{'player_profile_dict':player_profile_dict})



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
        print("Insde tournmentregistration page")
        print(trnm_obj)
        return render(request,'Manager/tournmentregistration.html',{'registerform':registerform})
        # return render(request,'Manager/tournmentregistration.html',{'trnm_obj':trnm_obj })

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
    f_date=datetime.datetime.now()
    date=f_date.strftime('%Y-%m-%d')
    s=str(date)
    print(s)

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
       (SELECT tr_name_id from Manager_tournmentregistration WHERE team_name_id = %d)
		AND Manager_addtournments.s_date> '%s' """%(x,s))

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
    return render(request,'Manager/showtour.html', {'dict':dict, 'dict1':dict1, 'user_obj':user_obj} )

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
    return render(request,'Manager/admin_fixture_tour_list.html',{'tourlist_dict':tourlist_dict})

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
	SELECT Manager_addteam.id,
	       Manager_addteam.team_name
    from Manager_addteam
    LEFT OUTER JOIN Manager_tournmentregistration
    ON (Manager_addteam.id = Manager_tournmentregistration.team_name_id)
    WHERE Manager_tournmentregistration.tr_name_id=%d"""%(int(tour_id.id)))
    team_dict = {}
    team_dict= dictfetchall(team_cursor)
    print("Inside team names")
    print(team_dict)

    #only for winner and Looser
    team2_cursor = connection.cursor()
    team2_cursor.execute("""
	SELECT Manager_addteam.id,
	       Manager_addteam.team_name
    from Manager_addteam
    LEFT OUTER JOIN Manager_tournmentregistration
    ON (Manager_addteam.id = Manager_tournmentregistration.team_name_id)
    WHERE Manager_tournmentregistration.tr_name_id=%d"""%(int(tour_id.id)))
    team2_dict = {}
    team2_dict= dictfetchall(team2_cursor)
    print("Inside Winner and looser")
    print(team2_dict)

    return render(request,'Manager/addpoints.html',{'point_dict':point_dict , 'tour_id':tour_id , 'team_dict':team_dict , 'team2_dict':team2_dict})

#adding values  to point point_table
def point_table(request):
        if request.method == 'POST':
            result = request.POST.get('r_type')
            print(result)
            if result == 'Win':
                tour_name = request.POST.get('trname')
                tourn_name_id = AddTournments.objects.get(t_name=tour_name)
                m_name = request.POST.get('matchname')
                match_name = AddFixture_table.objects.get(match_name=m_name)
                team_one = request.POST.get('team1')
                team_two = request.POST.get('team2')
                team_1_goal = request.POST.get('t1goals')
                team_2_goal = request.POST.get('t2goals')
                winner=request.POST.get('t1point')
                looser=request.POST.get('t2point')
                print("inside point table")
                print(tour_name)
                print(tourn_name_id)
                print(m_name)
                print(team_one)
                print(team_two)
                print(team_1_goal)
                print(team_2_goal)

                ob= AddPoints.objects.create(tourn_name_id=tourn_name_id ,m_name=match_name ,team_one=team_one,
                team_two=team_two,team_1_goal=team_1_goal,team_2_goal=team_2_goal,winner=winner,looser=looser)
                ob.save()

                live_scr_del_cursor = connection.cursor()
                live_scr_del_cursor.execute("""delete from Manager_livescore""")
                return redirect("/point_tourlist")
            else:
                print("Print tie")
                tour_name = request.POST.get('trname')
                tourn_name_id = AddTournments.objects.get(t_name=tour_name)
                m_name = request.POST.get('matchname')
                match_name = AddFixture_table.objects.get(match_name=m_name)
                team_one = request.POST.get('team1')
                team_two = request.POST.get('team2')
                team_1_goal = request.POST.get('t1goals')
                team_2_goal = request.POST.get('t2goals')
                print(tour_name)
                print(tourn_name_id)
                print(m_name)
                print(match_name)
                print(team_one)
                print(team_two)
                print(team_1_goal)
                print(team_2_goal)

                obj= Tie.objects.create(tourn_name_id=tourn_name_id ,m_name=match_name ,team_one=team_one,
                team_two=team_two,team_1_goal=team_1_goal,team_2_goal=team_2_goal)
                obj.save()
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
# def standing_list(request,id):
#     tour_id = AddTournments.objects.get(id=id)
#     print("Name of the tournmet is")
#     print(type(tour_id))
#     print(tour_id)
#     #to find all the teams in clicked tournment
#     team_list=connection.cursor()
#     team_list.execute("""
#     SELECT Manager_addteam.id, Manager_addteam.team_name
#     FROM Manager_addteam
#     LEFT OUTER JOIN Manager_tournmentregistration
#     on (Manager_addteam.id= Manager_tournmentregistration.team_name_id)
#     where Manager_tournmentregistration.tr_name_id=%s"""%(int(tour_id.id)))
#     team_list_dict = {}
#     team_list_dict =dictfetchall(team_list)
#     print("Teams playing in the tournments")
#     print(type(team_list_dict))
#     print(team_list_dict)
#     # find the number of matches played by each team
#     temp_store=[]
#
#     for i in team_list_dict:
#         #print(i['team_name'])
#         s=str(i['team_name'])
#         teambycount = connection.cursor()
#         teambycount.execute(""" select (select count(*) as c from Manager_addpoints where team_one = '%s')
#         +
#         (select count(*) as c from Manager_addpoints where team_two = '%s'
#         and Manager_addpoints.tourn_name_id_id=%d) as "no_of_matches",
#         (select count(*) as c from Manager_addpoints where
#         Manager_addpoints.winner ='%s' and Manager_addpoints.tourn_name_id_id=%d)
#         as wincount,
#         (select count(*) as c from Manager_addpoints where
#         Manager_addpoints.looser ='%s' and Manager_addpoints.tourn_name_id_id=%d)
#         as losscount,
#         (select (select count(*) as c from Manager_tie where team_one = '%s')
#         +
#         (select count(*) as c from Manager_tie where team_two = '%s' and Manager_tie.tourn_name_id_id=30))
#         As tie,
#         (select count(*)*3 as d  from Manager_addpoints where
#         Manager_addpoints.winner ='%s' and Manager_addpoints.tourn_name_id_id=%d)
#         as point
#         """%(s, s, int(tour_id.id), s ,int(tour_id.id) , s , int(tour_id.id),s, s, s, int(tour_id.id)))
#
#
#
#         a=[]
#
#         a=dictfetchall(teambycount)
#
#
#         #print("****" + str(a[0]['totcount']))
#         samp = {
#         'team_name': s,
#         'Matches': int(a[0]['no_of_matches']),
#         'wins': int(a[0]['wincount']),
#         'loss': int(a[0]['losscount']),
#         'tie': int(a[0]['tie']),
#         'Points': int(a[0]['point']),
#
# }
#
#         temp_store.append(samp)
#
#
#
#
#     print("*** Welcome to the Point table ********")
#     print(type(temp_store))
#     print(temp_store)
#     return render(request,'Manager/team_standings.html',{'temp_store':temp_store,'tour_id':tour_id})

#View for showing standing list
def standing_list(request,id):
    tour_id = AddTournments.objects.get(id=id)
    print("Name of the tournmet is")
    print(type(tour_id))
    print(tour_id)
    #to find all the teams in clicked tournment
    team_list=connection.cursor()
    team_list.execute("""
    SELECT Manager_addteam.id, Manager_addteam.team_name
    FROM Manager_addteam
    LEFT OUTER JOIN Manager_tournmentregistration
    on (Manager_addteam.id= Manager_tournmentregistration.team_name_id)
    where Manager_tournmentregistration.tr_name_id=%s"""%(int(tour_id.id)))
    team_list_dict = {}
    team_list_dict =dictfetchall(team_list)
    print("Teams playing in the tournments")
    print(type(team_list_dict))
    print(team_list_dict)
    # find the number of matches played by each team
    temp_store=[]

    for i in team_list_dict:
        #print(i['team_name'])
        s=str(i['team_name'])
        teambycount = connection.cursor()
        teambycount.execute(""" select (select count(*) as c from Manager_addpoints where team_one = '%s')
        +
        (select count(*) as c from Manager_addpoints where team_two = '%s'
        and Manager_addpoints.tourn_name_id_id=%d) as "no_of_matches",
        (select count(*) as c from Manager_addpoints where
        Manager_addpoints.winner ='%s' and Manager_addpoints.tourn_name_id_id=%d)
        as wincount,
        (select count(*) as c from Manager_addpoints where
        Manager_addpoints.looser ='%s' and Manager_addpoints.tourn_name_id_id=%d)
        as losscount,
        (select (select count(*) as c from Manager_tie where team_one = '%s')
        +
        (select count(*) as c from Manager_tie where team_two = '%s' and Manager_tie.tourn_name_id_id=%d))
        As tie,
        (select count(*)*3 as d  from Manager_addpoints where
        Manager_addpoints.winner ='%s' and Manager_addpoints.tourn_name_id_id=%d)
        as point,
        (select(select (select count(*) as c from Manager_tie where team_one = '%s')
        +
        (select count(*) as c from Manager_tie where team_two = '%s' and Manager_tie.tourn_name_id_id =%d))*1)
        as tie_point
        """%(s, s, int(tour_id.id), s ,int(tour_id.id) , s , int(tour_id.id),s, s,int(tour_id.id), s, int(tour_id.id), s, s, int(tour_id.id)))



        a=[]

        a=dictfetchall(teambycount)
        print("************************************************")
        print(a)


        #print("****" + str(a[0]['totcount']))
        samp = {
        'team_name': s,
        'Matches': int(a[0]['no_of_matches']+ a[0]['tie_point']),
        'wins': int(a[0]['wincount']),
        'loss': int(a[0]['losscount']),
        'tie': int(a[0]['tie']),
        'Points': int(a[0]['point'] + a[0]['tie_point'])


        }

        temp_store.append(samp)

    tie_count_cursor=connection.cursor()
    tie_count_cursor.execute("""
    select Manager_tie.team_one,
    count(Manager_tie.team_one) As count1
    from Manager_tie
    WHERE Manager_tie.team_one='%s'"""%(s))
    tie_list_dict = {}
    tie_list_dict =dictfetchall(tie_count_cursor)
    print("Inside tie")
    print(tie_list_dict )



    print("*** Welcome to the Point table ********")
    print(type(temp_store))
    print(temp_store)
    return render(request,'Manager/team_standings.html',{'temp_store':temp_store,'tour_id':tour_id})


#view shows list of available tournmets while click on fixture tab from index page
def fixture_tour_list(request):
    print("inside fixture")
    f_date=datetime.datetime.now()
    date=f_date.strftime('%Y-%m-%d')
    print(date)
    s=str(date)
    print("string of date is")
    print(s)
    print(type(date))
    print(type(s))
    tourlist_cursor =connection.cursor()
    tourlist_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
    """)
    tourlist_dict = {}
    tourlist_dict =dictfetchall(tourlist_cursor)
    #print(tourlist_dict)

    today_fixture_cursor = connection.cursor()
    today_fixture_cursor.execute("""SELECT Manager_addfixture_table.id,
    Manager_addtournments.t_name,
	Manager_addfixture_table.match_date,
	Manager_addfixture_table.match_time,
	Manager_addfixture_table.team_one,
	Manager_addfixture_table.team_two,
	Manager_addfixture_table.venue
    from Manager_addtournments left OUTER join Manager_addfixture_table
    on(Manager_addtournments.id=Manager_addfixture_table.tr_name_id)
    WHERE Manager_addfixture_table.match_date='%s' """ %(str(s)))
    today_dict={}
    today_dict =dictfetchall(today_fixture_cursor)
    print(today_dict)


    return render(request,'Manager/fixture_tour_list.html',{'tourlist_dict':tourlist_dict, 'today_dict':today_dict})



#view shows fixtures respective to the tournments
def fixture_list(request,id):
    tour_id = AddTournments.objects.get(id=id)
    print("Name of the tournmet is")
    print(tour_id)
    f_cursor =connection.cursor()
    f_cursor.execute("""SELECT Manager_addfixture_table.match_date,
	                               Manager_addfixture_table.match_time,
	                               Manager_addfixture_table.team_one,
	                               Manager_addfixture_table.team_two,
	                               Manager_addfixture_table.match_name,
	                               Manager_addfixture_table.venue
	from Manager_addfixture_table
    where Manager_addfixture_table.tr_name_id=%d"""%(int(tour_id.id)))
    fixture_dict = {}
    fixture_dict =dictfetchall(f_cursor)
    print(fixture_dict)
    return render(request,'Manager/fixture_list.html',{'tour_id':tour_id, 'fixture_dict':fixture_dict})

#view shows list of available tournmets while click on Result tab from index page
def result_tour_list(request):
    f_date=datetime.datetime.now()
    date=f_date.strftime('%Y-%m-%d')

    s=str(date)


    result_cursor =connection.cursor()
    result_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
    """)
    r_dict = {}
    r_dict =dictfetchall(result_cursor)
    #print(r_dict)


    today_result_cursor = connection.cursor()
    today_result_cursor.execute("""SELECT Manager_addtournments.t_name,
	   Manager_addfixture_table.match_date,
	   Manager_addfixture_table.match_name,
	   Manager_addpoints.team_one,
	   Manager_addpoints.team_1_goal,
	   Manager_addpoints.team_two,
	   Manager_addpoints.team_2_goal,
	   Manager_addpoints.winner
       from Manager_addtournments left OUTER join Manager_addfixture_table
       on(Manager_addtournments.id=Manager_addfixture_table.tr_name_id)
       LEFT outer join Manager_addpoints
       on(Manager_addfixture_table.id=Manager_addpoints.m_name_id)
       WHERE Manager_addfixture_table.match_date='%s' """ %(str(s)))


    today_rdict={}
    today_rdict =dictfetchall(today_result_cursor)
    print(today_rdict)
    return render(request,'Manager/result_tour_list.html',{'r_dict':r_dict,'today_rdict':today_rdict})

#view shows fixtures respective to the tournments
def result_list(request,id):
    tour_id = AddTournments.objects.get(id=id)
    print("Name of the tournmet is")
    print(tour_id)
    r_cursor =connection.cursor()
    r_cursor.execute("""
    select Manager_addfixture_table.match_date,
	   Manager_addfixture_table.match_name,
	   Manager_addpoints.team_one,
	   Manager_addpoints.team_1_goal,
	   Manager_addpoints.team_two,
	   Manager_addpoints.team_2_goal,
	   Manager_addpoints.winner
    from Manager_addfixture_table
    LEFT OUTER JOIN Manager_addpoints
    on(Manager_addfixture_table.id=Manager_addpoints.m_name_id)
    WHERE Manager_addpoints.tourn_name_id_id=%d"""%(int(tour_id.id)))
    result_dict = {}
    result_dict =dictfetchall(r_cursor)
    print(result_dict)
    return render(request,'Manager/result.html',{'tour_id':tour_id, 'result_dict':result_dict})

#view for show About
def show_about(request):
    return render(request,'Manager/about.html')

def show_contact(request):
    return render(request,'Manager/contact.html')

def pdf_view(request):
    #return HttpResponse('Hi')
    tour = request.POST.get('tour_id')
    print("inside pdf")
    print("********* Inside Tournment is *******")
    print(tour)
    tour_id = AddTournments.objects.get(t_name=tour)
    print("DIsplay tournmentId ")
    print(tour_id)
    print(tour_id.id)


	#to find all the teams in clicked tournment
    team_list=connection.cursor()
    team_list.execute("""
    SELECT Manager_addteam.id, Manager_addteam.team_name
    FROM Manager_addteam
    LEFT OUTER JOIN Manager_tournmentregistration
    on (Manager_addteam.id= Manager_tournmentregistration.team_name_id)
    where Manager_tournmentregistration.tr_name_id=%s"""%(tour_id.id))
    team_list_dict = {}
    team_list_dict =dictfetchall(team_list)
    print("Teams playing in the tournments inside pdf is")
    #print(type(team_list_dict))
    print(team_list_dict)
    # find the number of matches played by each team
    temp_store=[]

    for i in team_list_dict:
        #print(i['team_name'])
        s=str(i['team_name'])
        teambycount = connection.cursor()
        teambycount.execute(""" select (select count(*) as c from Manager_addpoints where team_one = '%s')
        +
        (select count(*) as c from Manager_addpoints where team_two = '%s'
        and Manager_addpoints.tourn_name_id_id=%d) as "no_of_matches",
        (select count(*) as c from Manager_addpoints where
        Manager_addpoints.winner ='%s' and Manager_addpoints.tourn_name_id_id=%d)
        as wincount,
        (select count(*) as c from Manager_addpoints where
        Manager_addpoints.looser ='%s' and Manager_addpoints.tourn_name_id_id=%d)
        as losscount,
        (select count(*)*3 as d  from Manager_addpoints where
        Manager_addpoints.winner ='%s' and Manager_addpoints.tourn_name_id_id=%d)
        as point
        """%(s, s, int(tour_id.id), s ,int(tour_id.id) , s , int(tour_id.id), s, int(tour_id.id)))



        a=[]

        a=dictfetchall(teambycount)


        #print("****" + str(a[0]['totcount']))
        samp = {
        'team_name': s,
        'Matches': int(a[0]['no_of_matches']),
        'wins': int(a[0]['wincount']),
        'loss': int(a[0]['losscount']),
        'Points': int(a[0]['point'])
        }

        temp_store.append(samp)
    print("Final result in the pdf view is")
    print(temp_store)

    pdf = render_to_pdf('pdf/invoice.html', {'temp_store':temp_store})
    return HttpResponse(pdf, content_type='application/pdf')

#list available tournment list while click on goals and assist from admin side
def goals_assist_tour_list(request):
    goals_assist_cursor =connection.cursor()
    goals_assist_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
    """)
    goals_assist_dict = {}
    goals_assist_dict =dictfetchall(goals_assist_cursor)
    print(goals_assist_dict)
    return render(request,'Manager/g_and_a_tour_list.html',{'goals_assist_dict':goals_assist_dict})

#viwe for adding goals and assist from admin side
def add_goals_assists(request, id):
    tour_id = AddTournments.objects.get(id=id)
    print(tour_id)
    admin_ga = connection.cursor()
    admin_ga.execute("""
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
    admin_ga_dict = {}
    admin_ga_dict = dictfetchall(admin_ga)

    print(admin_ga_dict)

    point_cursor = connection.cursor()
    point_cursor.execute("""
    SELECT Manager_addfixture_table.match_name
    from Manager_addfixture_table
    where Manager_addfixture_table.tr_name_id=%d"""%(int(tour_id.id)))
    point_dict = {}
    point_dict= dictfetchall(point_cursor)
    print("Inside add points")
    print(point_dict)


    return render(request,'Manager/add_g_a.html',{'admin_ga_dict':admin_ga_dict,'tour_id':tour_id,'point_dict':point_dict})

# adding values into goals and assist table
def ganda_table(request):
    if request.method == 'POST':
        tour_name = request.POST.get('trname')
        tourn_name= AddTournments.objects.get(t_name=tour_name)
        mat_name = request.POST.get('matchname')
        match_name = AddFixture_table.objects.get(match_name=mat_name)
        g_name = request.POST.get('gname')
        a_name = request.POST.get('aname')
        t_name = request.POST.get('teamnm')
        team_name = AddTeam.objects.get(team_name=t_name)
        g_time = request.POST.get('gtime')
        print("Inside ganda table")
        print(tour_name)
        print(tourn_name.id)
        print(mat_name)
        print(g_name)
        print(a_name)
        x=len(a_name)
        if (x==0):
            print("Empty Spootted")
            a_name = 'NULL'
            print(a_name)
        print(t_name)
        print(g_time)
        ob =AddGoalsandAssist.objects.create(tour_name=tourn_name, matchname=match_name,
        Scorer_name=g_name,assist_name=a_name,team_name=team_name,g_time=g_time)
        ob.save()
        return redirect("/galist")

#list all the available tornmrnt while click on saves from admin adminpage
def save_tour_list(request):
    save_cursor =connection.cursor()
    save_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
    """)
    save_dict = {}
    save_dict =dictfetchall(save_cursor)
    print(save_dict)
    return render(request,'Manager/saves_tour_list.html',{'save_dict':save_dict})


#viwe for adding goals and assist from admin side
def saves_list(request, id):
    tour_id = AddTournments.objects.get(id=id)
    print(tour_id)
    save_cursor = connection.cursor()
    save_cursor.execute("""
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
    saves_dict = {}
    saves_dict = dictfetchall(save_cursor)

    print(saves_dict)

    point_cursor = connection.cursor()
    point_cursor.execute("""
    SELECT Manager_addfixture_table.match_name
    from Manager_addfixture_table
    where Manager_addfixture_table.tr_name_id=%d"""%(int(tour_id.id)))
    point_dict = {}
    point_dict= dictfetchall(point_cursor)
    print("Inside add points")
    print(point_dict)


    return render(request,'Manager/add_saves.html',{'saves_dict':saves_dict,'tour_id':tour_id,'point_dict':point_dict})


#Adding values to the saves table
def goalkeeper(request):
    if request.method == 'POST':
        tour_name = request.POST.get('trname')
        tourn_name= AddTournments.objects.get(t_name=tour_name)
        mat_name = request.POST.get('matchname')
        match_name = AddFixture_table.objects.get(match_name=mat_name)
        gkname = request.POST.get('gname')
        saves= request.POST.get('saves')
        t_name = request.POST.get('teamnm')
        team_name = AddTeam.objects.get(team_name=t_name)
        print(tourn_name)
        print(match_name)
        print(gkname)
        print(saves)
        print(team_name)
        ob =AddGoalKeeperSaves.objects.create(tour_name=tourn_name, matchname=match_name,
        gk_names=gkname,saves=saves,team_name=team_name)
        ob.save()
        return redirect("/s_tour_list")


# ****************** Listing Statics from Index Page ****************************

#show tournment list when click on top goals from index page
def tourlist_goals(request):
    top_goal_cursor =connection.cursor()
    top_goal_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
    """)
    top_goal_dict = {}
    top_goal_dict =dictfetchall(top_goal_cursor)
    print(top_goal_dict)
    return render(request,'Manager/top_goals_tour_list.html',{'top_goal_dict':top_goal_dict})



# list top goal scores
def top_goals_list(request, id):
    tour_id = AddTournments.objects.get(id=id)
    print(tour_id)
    goal_cursor = connection.cursor()
    goal_cursor.execute("""
    select upper(Manager_addgoalsandassist.Scorer_name) as "Player",count(*) as "Goals" , Manager_addteam.team_name as "Team"
    from Manager_addgoalsandassist
    LEFT OUTER JOIN Manager_addteam
    on(Manager_addgoalsandassist.team_name_id=Manager_addteam.id)
    where Manager_addgoalsandassist.tour_name_id=%d
    GROUP by Player
    ORDER By Goals DESC
    """ %(int(tour_id.id)))

    top_goal_dict = {}
    top_goal_dict = dictfetchall(goal_cursor)
    print(top_goal_dict)
    return render(request,'Manager/top_goals.html',{'top_goal_dict':top_goal_dict,'tour_id':tour_id})


#show tournment list when click on top saves from index page
def t_saves_tourlist(request):
    top_save_cursor =connection.cursor()
    top_save_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
    """)
    top_save_dict = {}
    top_save_dict =dictfetchall(top_save_cursor)
    print(top_save_dict)
    return render(request,'Manager/top_saves_tour_list.html',{'top_save_dict':top_save_dict})

# list top saves
def top_gk_list(request, id):
    tour_id = AddTournments.objects.get(id=id)
    print(tour_id)
    gk_cursor = connection.cursor()
    gk_cursor.execute("""
    select upper(Manager_addgoalkeepersaves.gk_names) As Player,sum(saves) as "Saves" , Manager_addteam.team_name
    from Manager_addgoalkeepersaves
	left OUTER JOIN Manager_addteam
	on(Manager_addgoalkeepersaves.team_name_id=Manager_addteam.id)
    where Manager_addgoalkeepersaves.tour_name_id=%d
    GROUP by Player
    ORDER by saves DESC""" %(int(tour_id.id)))
    top_gk_dict = {}
    top_gk_dict = dictfetchall(gk_cursor)
    print(top_gk_dict)
    return render(request,'Manager/top_gk.html',{'top_gk_dict':top_gk_dict})




#show tournment list when click on top assist from index page
def t_assist_tourlist(request):
        top_assist_cursor =connection.cursor()
        top_assist_cursor.execute("""
        SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
    	LEFT OUTER JOIN Manager_addtournments
    	on
    	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
        """)
        top_assist_dict = {}
        top_assist_dict =dictfetchall(top_assist_cursor)
        print(top_assist_dict)
        return render(request,'Manager/top_assist_tour_list.html',{'top_assist_dict':top_assist_dict})

# list top assists
def top_assist_list(request, id):
    tour_id = AddTournments.objects.get(id=id)
    print(tour_id)
    assist_cursor = connection.cursor()
    assist_cursor.execute("""
    select upper(Manager_addgoalsandassist.assist_name) as "Player",count(*) as "Assists" , Manager_addteam.team_name as "Team"
    from Manager_addgoalsandassist
    LEFT OUTER JOIN Manager_addteam
    on(Manager_addgoalsandassist.team_name_id=Manager_addteam.id)
    where Manager_addgoalsandassist.tour_name_id=%d and Player is NOT 'NULL'
    GROUP by Player
    ORDER By Assists DESC """ %(int(tour_id.id)))
    top_assist_dict = {}
    top_assist_dict = dictfetchall(assist_cursor)
    print(top_assist_dict)
    return render(request,'Manager/top_assist.html',{'top_assist_dict':top_assist_dict,'tour_id':tour_id})

#using ajax in the standing ganda_table
def aja_stand(request):
    print("Ajax called")
    if request.is_ajax() and request.GET:
        tour_name= request.GET.get('name')
        tour_id= AddTournments.objects.get(t_name=tour_name)
        print(tour_name)
        print(tour_id.id)
        team_list=connection.cursor()
        team_list.execute("""
        SELECT Manager_addteam.id, Manager_addteam.team_name
        FROM Manager_addteam
        LEFT OUTER JOIN Manager_tournmentregistration
        on (Manager_addteam.id= Manager_tournmentregistration.team_name_id)
        where Manager_tournmentregistration.tr_name_id=%s"""%(int(tour_id.id)))

        res = team_list.fetchall()
        res_list = []
        print("Team list")
        for r in res:
            t ={}
            t['id']=r[0]
            t['team_name']= r[1]
            res_list.append(t)
        print(res_list)
        j=json.dumps(res_list)
        team_list.close()  #closing cursor
        return JsonResponse(res_list, safe=False)

def aja_tour_goals(request):
    #print("Inside tournment goals ajax")
    if request.is_ajax() and request.GET:
        tour_name= request.GET.get('name')
        tour_id= AddTournments.objects.get(t_name=tour_name)
        #print(tour_name)
        #print(tour_id)
        #print(tour_id.id)
        tour_goals_cursor = connection.cursor()
        tour_goals_cursor.execute("""
        SELECT Manager_addtournments.t_name,
	    count(Manager_addgoalsandassist.tour_name_id) As Goals
        from Manager_addtournments left outer join Manager_addgoalsandassist
        on(Manager_addtournments.id = Manager_addgoalsandassist.tour_name_id)
        WHERE Manager_addtournments.id=%d"""%(int(tour_id.id)))
        res =tour_goals_cursor.fetchall()
        res_list = []
        for r in res:
            t = {}
            t['t_name']=r[0]
            t['Goals'] = r[1]
            res_list.append(t)
        #print(res_list)
        j=json.dumps(res_list)
        tour_goals_cursor.close()
        return JsonResponse(res_list, safe=False)

def aja_top_goals(request):
    #print("Inside admin top scorer")
    if request.is_ajax() and request.GET:
        tour_name= request.GET.get('name')
        tour_id= AddTournments.objects.get(t_name=tour_name)
        #print(tour_name)
        #print(tour_id)
        #print(tour_id.id)
        top_scorer_cursor=connection.cursor()
        top_scorer_cursor.execute("""select Manager_addgoalsandassist.Scorer_name,
	    count(Scorer_name) As Goals
        from Manager_addgoalsandassist WHERE Manager_addgoalsandassist.tour_name_id=%d
        GROUP by Manager_addgoalsandassist.Scorer_name
        ORDER by Goals DESC"""%(int(tour_id.id)))
        res1 =top_scorer_cursor.fetchall()
        res_list1 = []
        for r in res1:
            t = {}
            t['Scorer_name']=r[0]
            t['Goals'] = r[1]
            res_list1.append(t)
        #print(res_list1)
        j=json.dumps(res_list1)
        top_scorer_cursor.close()
        return JsonResponse(res_list1, safe=False)

#display top assist in admin Page
def aja_top_assist(request):
    #print("inside ajax top assist")
    if request.is_ajax() and request.GET:
        tour_name= request.GET.get('name')
        tour_id= AddTournments.objects.get(t_name=tour_name)
        #print(tour_name)
        #print(tour_id)
        #print(tour_id.id)
        top_assist_cursor=connection.cursor()
        top_assist_cursor.execute("""select Manager_addgoalsandassist.assist_name,
	    count(assist_name) As Assist
        from Manager_addgoalsandassist
		WHERE Manager_addgoalsandassist.assist_name is NOT 'NULL' and Manager_addgoalsandassist.tour_name_id=%d
        GROUP by Manager_addgoalsandassist.assist_name
        ORDER by Assist DESC"""%(int(tour_id.id)))
        res1 =top_assist_cursor.fetchall()
        res_list1 = []
        for r in res1:
            t = {}
            t['assist_name']=r[0]
            t['Assist'] = r[1]
            res_list1.append(t)
        print(res_list1)
        j=json.dumps(res_list1)
        top_assist_cursor.close()
        return JsonResponse(res_list1, safe=False)

def aja_top_gk(request):
    print("inside ajax top goal GoalKeeper")
    if request.is_ajax() and request.GET:
        tour_name= request.GET.get('name')
        tour_id= AddTournments.objects.get(t_name=tour_name)
        print(tour_name)
        print(tour_id)
        print(tour_id.id)
        admin_gk_cursor = connection.cursor()
        admin_gk_cursor.execute("""select Manager_addgoalkeepersaves.gk_names,sum(saves) as "Saves" , Manager_addteam.team_name
        from Manager_addgoalkeepersaves
	    left OUTER JOIN Manager_addteam
	    on(Manager_addgoalkeepersaves.team_name_id=Manager_addteam.id)
        where Manager_addgoalkeepersaves.tour_name_id=%d
        GROUP by Manager_addgoalkeepersaves.gk_names
	    ORDER by Manager_addgoalkeepersaves.saves ASC""" %(int(tour_id.id)))

        res1 =admin_gk_cursor.fetchall()
        res_list1 = []
        for r in res1:
            t = {}
            t['gk_name']=r[0]
            t['Saves'] = r[1]
            res_list1.append(t)
        print(res_list1)
        j=json.dumps(res_list1)
        admin_gk_cursor.close()
        return JsonResponse(res_list1, safe=False)

#chart.js 1
def get_data(request):
    data = {
        "Tournment":'EPL',
        "Count": 10,
    }
    return JsonResponse(data)


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        team_count_cursor = connection.cursor()
        team_count_cursor.execute("""select  Manager_addtournments.id,
		Manager_addtournments.t_name,
		count(Manager_tournmentregistration.tr_name_id) As count
        from  Manager_addtournments LEFT OUTER join Manager_tournmentregistration
        on (Manager_addtournments.id = Manager_tournmentregistration.tr_name_id)
        GROUP by Manager_addtournments.t_name""")
        team_list_new_dict = {}
        team_list_new_dict = dictfetchall(team_count_cursor)
        print("Team list is")
        print(team_list_new_dict)
        label =[]
        for i in range(len(team_list_new_dict)):
            label.append(team_list_new_dict[i]['t_name'])

        print(label)

        count = []
        for i in range(len(team_list_new_dict)):
            count.append(team_list_new_dict[i]['count'])
        print(count)




        # labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        labels = label
        default_items = count
        data={
            "labels":labels,
            "default":default_items,
        }
        return Response(data)


def user_logout(request):
    if request.method == "GET":
        print("hi")
        logout(request)
        return HttpResponseRedirect(reverse('login'))

#adding live score from admin side
def live_score_admin(request):
    print("inside adding fixture from admin side")
    f_date=datetime.datetime.now()
    date=f_date.strftime('%Y-%m-%d')
    s=str(date)
    print(s)
    today_fixture_cursor = connection.cursor()
    today_fixture_cursor.execute("""SELECT Manager_addfixture_table.id,
    Manager_addtournments.t_name,
	Manager_addfixture_table.match_date,
	Manager_addfixture_table.match_time,
	Manager_addfixture_table.team_one,
	Manager_addfixture_table.team_two,
	Manager_addfixture_table.venue
    from Manager_addtournments left OUTER join Manager_addfixture_table
    on(Manager_addtournments.id=Manager_addfixture_table.tr_name_id)
    WHERE Manager_addfixture_table.match_date='%s' """ %(str(s)))
    today_dict={}
    today_dict =dictfetchall(today_fixture_cursor)
    print(today_dict)
    return render(request,'Manager/admin_live_score.html',{'today_dict':today_dict})



#live score form
# def live_score_form(request):
#     form = LiveScoreForm()
#     # if request.method=='POST':
#     #     form = LiveScoreForm(request.POST)
#     #     if form.is_valid():
#     #         form.save()
#             #TournmentRegistration.objects.create(tr_name=trnmnt, team_name= team_obj, is_registred= False)
#             #return redirect('/admpg')
#     return render(request,'Manager/show_live_score.html',{'form':form})



# def live_score_form(request):
#     form = LiveScoreForm()
#     if request.method == 'POST':
#         print("inside if")
#         form = LiveScoreForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/home')
#     return render(request,'Manager/show_live_score.html',{'form': form})


def live_score_form_1(request, id):
    if request.method == 'POST':
        mtch_id = request.POST.get('matchname')
        tm_name = request.POST.get('teamname')
        score = request.POST.get('Score')

        print(mtch_id)
        print(tm_name)
        print(score)

        mtch_obj = AddFixture_table.objects.get(id=mtch_id)
        print(mtch_obj)
        print(type(mtch_obj))
        tm_obj = AddTeam.objects.get(team_name= tm_name)
        print(tm_obj)
        print(type(tm_obj))

        obj = LiveScore.objects.create(f_id = mtch_obj, team_name = tm_obj, score = score)
        obj.save()
        return redirect('/add_live_score')

    else:
        fix = AddFixture_table.objects.filter(id=id)
        print(fix)
        form={}
        return render(request,'Manager/show_live_score.html',{'fix': fix})


#see live score from index page
# def see_live_score(request):
#     if request.is_ajax() and request.method=='GET':
#         j=json.dumps('Hello')
#         print('helllolloo')
#         return JsonResponse(j, safe=False)
#         #return JsonResponse
#     else:
#         return render(request,'Manager/index_live_score.html')


def see_live_score(request):
    print("Inside ajaxsubjectlist")


    f_date=datetime.datetime.now()
    date=f_date.strftime('%Y-%m-%d')
    print(date)
    s=str(date)

    today_fixture_cursor = connection.cursor()
    today_fixture_cursor.execute("""SELECT Manager_addfixture_table.id,
        Manager_addtournments.t_name,
        Manager_addfixture_table.match_date,
        Manager_addfixture_table.match_time,
        Manager_addfixture_table.team_one,
        Manager_addfixture_table.team_two,
        Manager_addfixture_table.venue
        from Manager_addtournments left OUTER join Manager_addfixture_table
        on(Manager_addtournments.id=Manager_addfixture_table.tr_name_id)
        WHERE Manager_addfixture_table.match_date='%s' """ %(str(s)))

    today_dict={}
    today_dict =dictfetchall(today_fixture_cursor)

    if len(today_dict) > 0:
        team_one = str(today_dict[0]['team_one'])
        team_two = str(today_dict[0]['team_two'])

        team_one_obj =  AddTeam.objects.get(team_name= team_one)
        team_two_obj =  AddTeam.objects.get(team_name= team_two)

        team_one_id = int(team_one_obj.id)
        team_one_logo = str(team_one_obj.team_logo)
        team_two_id = int(team_two_obj.id)
        team_two_logo = str(team_two_obj.team_logo)

        team_one_cursor = connection.cursor()
        team_one_cursor.execute("""select count(*) as tot_count from Manager_livescore
                                where team_name_id = '%d'""" % (team_one_id))
        team_one_dict = {}
        team_one_dict = dictfetchall(team_one_cursor)
        team_one_count = team_one_dict[0]['tot_count']

        team_two_cursor = connection.cursor()
        team_two_cursor.execute("""select count(*) as tot_count from Manager_livescore
                                where team_name_id = '%d'""" % (team_two_id))
        team_two_dict = {}
        team_two_dict = dictfetchall(team_two_cursor)
        team_two_count = team_two_dict[0]['tot_count']
    else:
        team_one = ""
        team_two = ""
        team_one_count = 0
        team_two_count = 0

    return render(request,'Manager/index_live_score.html', {'team_one': team_one,
        'today_dict': today_dict,
        'team_two': team_two,
        'team_one_count': team_one_count,
        'team_two_count': team_two_count,
        'team_one_logo': team_one_logo,
        'team_two_logo': team_two_logo})

def ajax_live_score(request):
    print("inside livescore ajax")

    f_date=datetime.datetime.now()
    date=f_date.strftime('%Y-%m-%d')
    print(date)
    s=str(date)

    today_fixture_cursor = connection.cursor()
    today_fixture_cursor.execute("""SELECT Manager_addfixture_table.id,
        Manager_addtournments.t_name,
        Manager_addfixture_table.match_date,
        Manager_addfixture_table.match_time,
        Manager_addfixture_table.team_one,
        Manager_addfixture_table.team_two,
        Manager_addfixture_table.venue
        from Manager_addtournments left OUTER join Manager_addfixture_table
        on(Manager_addtournments.id=Manager_addfixture_table.tr_name_id)
        WHERE Manager_addfixture_table.match_date='%s' """ %(str(s)))

    today_dict={}
    today_dict =dictfetchall(today_fixture_cursor)

    if len(today_dict) > 0:
        team_one = str(today_dict[0]['team_one'])
        team_two = str(today_dict[0]['team_two'])

        team_one_obj =  AddTeam.objects.get(team_name= team_one)
        team_two_obj =  AddTeam.objects.get(team_name= team_two)

        team_one_id = int(team_one_obj.id)
        team_one_logo = str(team_one_obj.team_logo)
        team_two_id = int(team_two_obj.id)
        team_two_logo = str(team_two_obj.team_logo)

        team_one_cursor = connection.cursor()
        team_one_cursor.execute("""select count(*) as tot_count from Manager_livescore
                                where team_name_id = '%d'""" % (team_one_id))
        team_one_dict = {}
        team_one_dict = dictfetchall(team_one_cursor)
        team_one_count = team_one_dict[0]['tot_count']

        team_two_cursor = connection.cursor()
        team_two_cursor.execute("""select count(*) as tot_count from Manager_livescore
                                where team_name_id = '%d'""" % (team_two_id))
        team_two_dict = {}
        team_two_dict = dictfetchall(team_two_cursor)
        team_two_count = team_two_dict[0]['tot_count']
    else:
        team_one = ""
        team_two = ""
        team_one_count = 0
        team_two_count = 0

    return render(request, 'Manager/ajax_load_livscore.html', {'team_one': team_one,
        'today_dict': today_dict,
        'team_two': team_two,
        'team_one_count': team_one_count,
        'team_two_count': team_two_count,
        'team_one_logo': team_one_logo,
        'team_two_logo': team_two_logo})
