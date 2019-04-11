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
    url(r'^$', views.index_view),
    url(r'^signup', views.signup_view),
    url(r'^login', views.login_view),
    url(r'^home', views.home_view),
    url(r'^addteam', views.addteam_view),
    url(r'^addplayer', views.addplayer_view),
    url(r'^admpg', views.load_admin_view),
    url(r'^tournmentadd', views.addtournment_view),
    url(r'^showtour', views.show_tournments_view),
    url(r'^myteam', views.view_team),
    url(r'^delete/(?P<id>\d+)/$', views.delete_view),
    url(r'^payment', views.makepayment_view),


]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
