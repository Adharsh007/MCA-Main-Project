"""FootballLeague URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from Manager import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$', views.index_view),
    url(r'^index', views.index_view),
    url(r'^$', views.load_view),
    url(r'^signup', views.signup_view),
    url(r'^login', views.login_view, name="login"),
    url(r'^home', views.home_view),
    url(r'^addteam', views.addteam_view),
    url(r'^addplayer', views.addplayer_view),
    url(r'^admpg', views.load_admin_view),
    url(r'^addnews', views.addnews_view),
    url(r'^listnews', views.NewsList.as_view()),
    url(r'^(?P<pk>\d+)/$', views.NewsDetail.as_view()),
    url(r'^myteam', views.view_team),
    url(r'^delete/(?P<id>\d+)/$', views.delete_view),
    url(r'^update/(?P<id>\d+)/$', views.update_view),
    url(r'^payment', views.makepayment_view),
    url(r'^listclub', views.ClubListView.as_view()),
    url(r'^player-list/(?P<id>\d+)/$', views.playerlist_view),
    url(r'^player_detail/(?P<id>\d+)/$',views.playerdetail_view),
    url(r'^tournmentadd', views.addtournment_view),
    url(r'^registertour/(?P<id>\d+)/$', views.tournmentreg),
    url(r'^showtour', views.show_tournments_view),
    url(r'^tourlist', views.fix_tour_list),
    url(r'^addfixture/(?P<id>\d+)/$', views.add_fixture_admin),
    url(r'^to_fix_table', views.fixture_table),
    url(r'^point_tourlist', views.point_tour_list),
    url(r'^addpoints/(?P<id>\d+)/$', views.add_points_admin),
    url(r'^to_point_table', views.point_table),
    url(r'^standings_tourlist', views.standing_tour_list),
    url(r'^standings/(?P<id>\d+)/$', views.standing_list),
    url(r'^fixture_tourlist', views.fixture_tour_list),
    url(r'^fixture/(?P<id>\d+)/$', views.fixture_list),
    url(r'^result_tourlist', views.result_tour_list),
    url(r'^result/(?P<id>\d+)/$', views.result_list),
    url(r'^about', views.show_about),
    url(r'^contact', views.show_contact),
    url(r'^pdf', views.pdf_view),
    url(r'^galist', views.goals_assist_tour_list),
    url(r'^add_ga/(?P<id>\d+)/$', views.add_goals_assists),
    url(r'^addganda', views.ganda_table),
    url(r'^s_tour_list', views.save_tour_list),
    url(r'^saves/(?P<id>\d+)/$', views.saves_list),
    url(r'^savestable', views.goalkeeper),
    url(r'^t_list_goals', views.tourlist_goals),
    url(r'^t_saves', views.t_saves_tourlist),
    url(r'^t_assist', views.t_assist_tourlist),
    #url(r'^t_gk', views.t_gk_tourlist),
    url(r'^top_goals/(?P<id>\d+)/$', views.top_goals_list),
    url(r'^top_sav/(?P<id>\d+)/$', views.top_gk_list),
    url(r'^top_assist/(?P<id>\d+)/$', views.top_assist_list),
    url(r'^ajaxx', views.aja_stand),
    url(r'^tournment_goals', views.aja_tour_goals),
    url(r'^admin_top_scorer', views.aja_top_goals),
    url(r'^admin_top_assist', views.aja_top_assist),
    url(r'^admin_top_gk', views.aja_top_gk),
    url(r'^data', views.get_data),
    url(r'^chartdata', views.ChartData.as_view()),
    url(r'^logout', views.user_logout),
    url(r'^add_live_score', views.live_score_admin),
    #url(r'^lis', views.live_score_form),
    url(r'^lis/(?P<id>\d+)/$', views.live_score_form_1, name='liv'),
    url(r'^s_live_score', views.see_live_score),
    url(r'^ajax/load-livescore', views.ajax_live_score, name= 'ajax_load_livescore'),
    










]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
