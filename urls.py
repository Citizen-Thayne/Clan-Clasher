from django.conf.urls import include, url
from django.contrib import admin
from ClanClasher import views
from ClanClasher.views import ChiefDetailView, ChiefListView, ClanDetailView


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^register$',views.register, name='register'),
    url(r'^login',views.login, name='login'),
    url(r'^logout',views.logout_view, name='logout'),
    url(r'^chief/detail/(?P<pk>\d+)$', ChiefDetailView.as_view(template_name='chief/detail.html'), name='chief_detail'),
    url(r'^chief/list/$', ChiefListView.as_view(template_name='chief/list.html'), name='chief_list'),
    url(r'^clan/detail/(?P<pk>\d+)$', ClanDetailView.as_view(template_name='clan/detail.html'), name='clan_detail'),

]