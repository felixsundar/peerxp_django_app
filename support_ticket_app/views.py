from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from support_ticket_app.forms import NewTicketForm

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
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            messages.success(request, 'New Ticket has been added successfully.')
            return redirect('index')
    else:
        form = NewTicketForm()
    context = { 'form': form }
    return render(request, 'newticket.html', context)


@login_required
def myticketsView(request):
    pass
