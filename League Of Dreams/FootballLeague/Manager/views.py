from django.shortcuts import render
from Manager.forms import SignUpForm,UserProfileForm,AddTeamForm,AddPlayerForm,AddTournmentsForm,AddNewsForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from Manager.models import AddTournments,AddPlayer,AddNews
from django.db import connection
from django.views.generic import ListView,DetailView

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
        request.session['loginid'] = user.id
        print(user)

        if user:
            if user.is_superuser == 1 and user.is_staff ==1:
                return render(request,'Manager/adminpage.html')
            elif user:
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

#Add tournmets from the admin home page
def addtournment_view(request):
    addtourform = AddTournmentsForm()
    if request.method=='POST':
        addtourform = AddTournmentsForm(request.POST)
        if addtourform.is_valid():
            addtourform.save()
            return redirect('/admpg')
    return render(request,'Manager/addtournment.html',{'addtourform':addtourform})

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




def show_tournments_view(request):
    tournment = AddTournments.objects.all()
    return render(request,'Manager/showtour.html',{'tournment':tournment})



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
