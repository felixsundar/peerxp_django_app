from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.

@login_required
def index(request):
    return render(request, 'home.html')

def loginView(request):
    if request.user.is_authenticated:
        return redirect('index')
    return LoginView.as_view(template_name='login.html')(request)


@login_required
def logoutView(request):
    return LogoutView.as_view()(request)


@login_required
def newticketView(request):
    pass


@login_required
def myticketsView(request):
    pass
