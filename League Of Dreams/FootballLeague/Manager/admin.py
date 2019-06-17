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
    list_display = ['t_name','t_venue','s_date','e_date','r_fee']
admin.site.register(AddTournments,AddTournmentsAdmin)

class TournmentRegistrationAdmin(admin.ModelAdmin):
    list_display=['tr_name','team_name','is_registred']
admin.site.register(TournmentRegistration,TournmentRegistrationAdmin)

class AddFixture_tableAdmin(admin.ModelAdmin):
    list_display=['tr_name','team_one','team_two','match_name','match_date','match_time','venue','status']
admin.site.register(AddFixture_table,AddFixture_tableAdmin)

class AddPointsAdmin(admin.ModelAdmin):
    list_display = ['tourn_name_id','m_name','team_one','team_two','team_1_goal','team_2_goal','winner','looser','status']
admin.site.register(AddPoints,AddPointsAdmin)

class AddGoalsandAssistAdmin(admin.ModelAdmin):
    list_display = ['tour_name','matchname','Scorer_name','assist_name','team_name','g_time']
admin.site.register(AddGoalsandAssist,AddGoalsandAssistAdmin)

class AddGoalKeeperSavesAdmin(admin.ModelAdmin):
    list_display = ['tour_name','matchname','gk_names','saves','team_name']
admin.site.register(AddGoalKeeperSaves,AddGoalKeeperSavesAdmin)

class NewKeeperAdmin(admin.ModelAdmin):
    list_display = ['tour_name','matchname','gk_name','saves','team_name']
admin.site.register(NewKeeper,NewKeeperAdmin)
