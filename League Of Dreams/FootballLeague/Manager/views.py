from django.shortcuts import render
from Manager.forms import SignUpForm,UserProfileForm,AddTeamForm,AddPlayerForm,AddTournmentsForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from Manager.models import AddTournments

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

#to check login
""" def login_check(request):
    un = request.POST['uname']
    pw = request.POST['pwd']
    user = authenticate(request, username=un, password=pw)
    if user:
        return render(request,'Manager/home.html') """

#to check login and  display home page
def home_view(request):
    if request.method=='POST':
        un = request.POST.get('uname')
        pw = request.POST.get('pwd')
        user = authenticate(request, username=un, password=pw)
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


def show_tournments_view(request):
    tournment = AddTournments.objects.all()
    return render(request,'Manager/showtour.html',{'tournment':tournment})
