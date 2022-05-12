from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('newticket', views.newticketView, name='newticket'),
    path('mytickets', views.myticketsView, name='mytickets')
]