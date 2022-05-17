from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('tickets/new/', views.newticketView, name='newticket'),
    path('tickets/', views.manageticketsView, name='managetickets'),
    path('tickets/<str:ticketId>/delete/', views.deleteticketView, name='deleteticket'),
    path('tickets/<str:ticketId>/edit/', views.editticketView, name='editticket')
]