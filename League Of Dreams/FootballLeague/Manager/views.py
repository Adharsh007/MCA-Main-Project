from django.shortcuts import render
from Manager.forms import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from Manager.models import *
from django.db import connection
from django.views.generic import ListView,DetailView
from Manager import config

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


#view for show tournmets from index page
def fixture_list_view(request):
    print(" *****************inside fixture list **************************")
    drop_cursor = connection.cursor()
    drop_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)

    """)
    drop_dict = {}
    drop_dict = dictfetchall(drop_cursor)
    print(drop_dict)
    #print(drop_dict[1])
    return render(request,'Manager/fixture_list.html', {'drop_dict':drop_dict} )



#view for display each tournment fixture
def tournment_fixture_view(request,id):

    y=config.userid
    print(y)
    t_id = AddTournments.objects.get(id=id)
    print(id)
    print(t_id.t_name)
    if y is None:
        #show fixtures to the end user
        print("Inside User fixture")
        user_fixture = connection.cursor()
        user_fixture.execute("""
        SELECT ma.id,ma.match_date, ma.match_time, ma_1.team_name AS "Team1", ma_2.team_name AS "Team2",ma.venue,ma.status,ma.tournment_id_id
        from Manager_addfixture ma
        left outer join Manager_addteam ma_1 on ma_1.id=ma.team_name_one
        left outer join Manager_addteam ma_2 on ma_2.id=ma.team_name_two
        WHERE ma.status=0 AND ma.tournment_id_id=%d """%(t_id.id))
        user_fixture_dict = {}
        user_fixture_dict = dictfetchall(user_fixture)
        print(user_fixture_dict)
        return render(request, 'Manager/tournment_fixture.html',{'user_fixture_dict':user_fixture_dict})


    elif y is not None:
        print("Inside admin fixture")
        admin_fixture = connection.cursor()
        admin_fixture.execute("""
        select DISTINCT Manager_tournmentregistration.team_name_id, Manager_addteam.team_name,
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
        Manager_tournmentregistration.tr_name_id= %d """%(int(t_id.id)))
        admin_fixture_dict = {}
        admin_fixture_dict = dictfetchall(admin_fixture)
        print(admin_fixture_dict)
        t_id = AddTournments.objects.get(id=id)
        return render(request,'Manager/add_fixture_admin.html',{'admin_fixture_dict':admin_fixture_dict, 't_id': t_id})

    else:
        return render(request,'Manager/tournment_fixture.html')




#view for adding fixture from admin side
def add_fixture_admin(request):
    print("****** inside fixture ******")
    if request.method=='POST':
        tour_name = request.POST.get('trname')
        tourn_name_id = AddTournments.objects.get(t_name=tour_name)
        m_name = request.POST.get('mname')
        t1=request.POST.get('team1')
        t2=request.POST.get('team2')
        fdate=request.POST.get('fdate')
        print(tour_name)
        print(t1)
        print(t2)
        print(fdate)
        ftime=request.POST.get('ftime')
        fvenue=request.POST.get('fvenue')
        ob=AddFixture.objects.create(tournment_id=tourn_name_id,match_name=m_name,team_name_one=t1 , team_name_two=t2, match_date=fdate ,match_time=ftime , venue = fvenue )
        ob.save()
        return redirect("/fixture")

#This view is to show list of tournments while clicking result tab from main index page
def result_tournment_list(request):
    result_cursor = connection.cursor()
    result_cursor.execute("""
    SELECT DISTINCT Manager_addtournments.id,Manager_addtournments.t_name from Manager_tournmentregistration
	LEFT OUTER JOIN Manager_addtournments
	on
	(Manager_tournmentregistration.tr_name_id=Manager_addtournments.id)
    """)
    result_dict = {}
    result_dict = dictfetchall(result_cursor)
    print(result_dict)
    return render(request,'Manager/user_result_list.html', {'result_dict':result_dict} )

#this view shows the result from a particular tournment name
def result_view(request, id):

    if request.method == 'POST':
        form_1 = ResulTdisplayForm_1(request.POST)
        form_2 = ResulTdisplayForm_2(request.POST)
        id = AddTournments.objects.get(id=id)
        print("Insude result view")
        print(id)
        
    else:
        form_1 = ResulTdisplayForm_1()
        form_2 = ResulTdisplayForm_2()
        id = AddTournments.objects.get(id=id)
        print("Insude result view")
        print(id)
    return render(request,'Manager/results.html',{'form_1':form_1, 'form_2': form_2})
