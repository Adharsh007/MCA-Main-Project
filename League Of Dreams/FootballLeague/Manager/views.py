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
from Manager.utils import *

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
	select DISTINCT ma1.team_name as "Team1", ma2.team_name as "Team2", mat.match_name, mat.match_date, mat.match_time,mat.id
	from Manager_addfixture_table mat
	left outer join Manager_addteam ma1 on ma1.team_name = mat.team_one
	left outer join Manager_addteam ma2 on ma2.team_name = mat.team_two
	where mat.tr_name_id = %d"""%(int(tour_id.id)))
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
    print(type(tour_id))
    print(tour_id)


    """"x = AddPoints.objects.values_list('team_one',flat=True)
    y = AddPoints.objects.values_list('team_two',flat=True)
    z=x.union(y) #this is (1)
    print("teams in  tournments are")
    print(z) """
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



    print("*** Welcome to the Point table ********")
    print(type(temp_store))
    print(temp_store)
    return render(request,'Manager/team_standings.html',{'temp_store':temp_store,'tour_id':tour_id})

#view shows list of available tournmets while click on fixture tab from index page
def fixture_tour_list(request):
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
    result_cursor =connection.cursor()
    result_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
    """)
    r_dict = {}
    r_dict =dictfetchall(result_cursor)
    print(r_dict)
    return render(request,'Manager/result_tour_list.html',{'r_dict':r_dict})

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
    select Manager_addgoalsandassist.Scorer_name as "Player",count(*) as "Goals" , Manager_addteam.team_name as "Team"
    from Manager_addgoalsandassist
    LEFT OUTER JOIN Manager_addteam
    on(Manager_addgoalsandassist.team_name_id=Manager_addteam.id)
    where Manager_addgoalsandassist.tour_name_id=%d
    GROUP by Manager_addgoalsandassist.Scorer_name
    ORDER By Goals DESC""" %(int(tour_id.id)))

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
    select Manager_addgoalkeepersaves.gk_names,sum(saves) as "Saves" , Manager_addteam.team_name
    from Manager_addgoalkeepersaves
	left OUTER JOIN Manager_addteam
	on(Manager_addgoalkeepersaves.team_name_id=Manager_addteam.id)
    where Manager_addgoalkeepersaves.tour_name_id=%d
    GROUP by Manager_addgoalkeepersaves.gk_names""" %(int(tour_id.id)))
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
    select Manager_addgoalsandassist.assist_name as "Player",count(*) as "Assists" , Manager_addteam.team_name as "Team"
    from Manager_addgoalsandassist
    LEFT OUTER JOIN Manager_addteam
    on(Manager_addgoalsandassist.team_name_id=Manager_addteam.id)
    where Manager_addgoalsandassist.tour_name_id=%d and Player is NOT 'NULL'
    GROUP by Manager_addgoalsandassist.assist_name
    ORDER By Assists DESC """ %(int(tour_id.id)))
    top_assist_dict = {}
    top_assist_dict = dictfetchall(assist_cursor)
    print(top_assist_dict)
    return render(request,'Manager/top_assist.html',{'top_assist_dict':top_assist_dict,'tour_id':tour_id})
