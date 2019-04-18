from django import forms
from django.contrib.auth.models import User
from Manager.models import UserProfile,AddTeam,AddPlayer,AddTournments,AddNews
from django.contrib.auth.forms import UserCreationForm



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def save(self, commit=True):
        user=super().save(commit=False)

        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['Address','Contact']
        labels = {
        "Contact": "Contact Number"
        }

class AddTeamForm(forms.ModelForm):
    class Meta:
        model = AddTeam
        fields = ['team_name','username','address','contact_no','team_logo']

        labels = {
                    "team_name": "Team Name",
                    "username": "Manager Name",
                    "address": "Address",
                    "contact_no": "Contact Number",
                    "team_logo": "Team Logo"
         }


class AddPlayerForm(forms.ModelForm):
    class Meta:
        model = AddPlayer
        fields = ['first_name','last_name','team_name','age','contact_no','address','jersy_no','position','upload_photo']

        labels = {

                "first_name": "FirstName",
                "last_name": "LastName",
                "team_name": "TeamName",
                "age": "Age",
                "contact_no": "Contact Number",
                "address": "Address",
                "jersy_no": "jersy Number",
                "position": "Playing Position",
                "upload_photo" : "Upload Photo"

}

class AddTournmentsForm(forms.ModelForm):
    class Meta:
        model = AddTournments
        fields = ['t_name','t_venue','s_date','e_date','r_fee','is_registred']
        labels = {

            "t_name": "Tournment Name",
            "t_venue": "Tournment Venue",
            "s_date": "Start Date",
            "e_date": "End Date",
            "r_fee": "Registration Fee",
            "is_registred": "Registred?"
        }

class AddNewsForm(forms.ModelForm):
    class Meta:
        model = AddNews
        fields= ['news_image','news_head','body']
        labels = {

            "news_image": "Upload Image",
            "news_head": "Headline",
            "body": "News Body",

        }
