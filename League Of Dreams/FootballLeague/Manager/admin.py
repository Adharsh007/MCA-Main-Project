from django.contrib import admin
from Manager.models import *

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['Address','Contact']
admin.site.register(UserProfile,UserProfileAdmin)

class AddTeamAdmin(admin.ModelAdmin):
    list_display = ['team_name','username','address','contact_no','team_logo']
admin.site.register(AddTeam,AddTeamAdmin)

class AddPlayerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','team_name','age','contact_no','address','jersy_no','position','upload_photo']
admin.site.register(AddPlayer,AddPlayerAdmin)

class AddNewsAdmin(admin.ModelAdmin):
    list_display = ['news_image','news_head','body','created','updated','active']
admin.site.register(AddNews,AddNewsAdmin)

class AddTournmentsAdmin(admin.ModelAdmin):
    list_display = ['t_name','t_venue','s_date','e_date']
admin.site.register(AddTournments,AddTournmentsAdmin)

class TournmentRegistrationAdmin(admin.ModelAdmin):
    list_display=['tr_name','team_name','is_registred']
admin.site.register(TournmentRegistration,TournmentRegistrationAdmin)

class AddFixtureAdmin(admin.ModelAdmin):
    list_display=['tournment_id','match_name','team_name_one','team_name_two','match_date','match_time','venue','status']
admin.site.register(AddFixture,AddFixtureAdmin)

class AddResultsAdmin(admin.ModelAdmin):
    list_display=['tournment_id','fixture_id','score_one','score_two']
