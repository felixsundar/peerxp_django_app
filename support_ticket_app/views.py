from datetime import datetime
import requests
from django.conf import settings
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.http import require_http_methods

from support_ticket_app.forms import NewTicketForm, EditTicketForm
from support_ticket_app.models import APIToken

# Create your views here.

class MyUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = self.loginUsingUsername(username, password)
        if user is None:
            user = self.loginUsingEmail(username, password)
        return user

    def loginUsingUsername(self, username, password):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                # add db check here to equal the timing login using username and email
                return user

    def loginUsingEmail(self, username, password):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # run password hash here to equal timing of existent and non-existent users
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

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
def manageticketsView(request):
    headers = getRequestHeader()
    context = {'fetched':False}
    if headers != False:
        r = requests.get(settings.ZOHO_TICKETS_API_URL, headers=headers)
        if r.status_code == requests.codes.ok:
            context['fetched'] = True
            context['data'] = r.json()['data']
    return render(request, 'mytickets.html', context=context)

@login_required
@require_http_methods(['POST'])
def deleteticketView(request, ticketId):
    if deleteTicket(ticketId):
        messages.success(request, 'Ticket number '+ticketId+' has been deleted successfully!')
    else:
        messages.error(request, 'Deleting ticket number '+ticketId+' failed!')
    return redirect('managetickets')

@login_required
def newticketView(request):
    if request.method == 'POST':
        form = NewTicketForm(request.user, request.POST)
        if form.is_valid() and addNewTicket(form.cleaned_data):
            messages.success(request, 'New Ticket has been added successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Adding new ticket failed!')
    else:
        form = NewTicketForm(request.user)
    context = { 'form': form }
    return render(request, 'newticket.html', context)

@login_required
def editticketView(request, ticketId):
    if request.method == 'POST':
        form = EditTicketForm(request.POST)
        if form.is_valid() and editTicket(ticketId, form.cleaned_data):
            messages.success(request, 'Ticket number '+ticketId+' has been updated successfully!')
            return redirect('managetickets')
        else:
            messages.error(request, 'Updating ticket failed!')
    else:
        ticket = getTicket(ticketId)
        form = False if not ticket else EditTicketForm(ticket)
    context = { 'form': form }
    return render(request, 'editticket.html', context)

def deleteTicket(ticketId):
    headers = getRequestHeader()
    if not headers:
        return False
    data = { 'ticketIds':[ticketId] }
    r = requests.post(settings.ZOHO_DELETE_TICKET_URL, json=data, headers=headers)
    if r.status_code == requests.codes.no_content:
        return True
    return False

def addNewTicket(data):
    data['contact']={
        'lastName':data.pop('lastName'), 
        'email':data.pop('email')
    }
    headers = getRequestHeader()
    if not headers:
        return False
    r = requests.post(settings.ZOHO_TICKETS_API_URL, json=data, headers=headers)
    if r.status_code == requests.codes.ok:
        return True
    return False

def getTicket(ticketId):
    headers = getRequestHeader()
    if not headers:
        return False
    r = requests.get(settings.ZOHO_TICKETS_API_URL + '/' + ticketId, headers=headers)
    if r.status_code != requests.codes.ok:
        return False
    return r.json()

def editTicket(ticketId, data):
    headers = getRequestHeader()
    if not headers:
        return False
    r = requests.patch(settings.ZOHO_TICKETS_API_URL + '/' + ticketId, json=data, headers=headers)
    if r.status_code == requests.codes.ok:
        return True
    return False

def getRequestHeader():
    try:
        token = APIToken.objects.get(tokenID=settings.ZOHO_API_TOKEN_ID)
    except APIToken.DoesNotExist:
        return False
    if not validateToken(token) and not renewToken(token):
        return False
    header = {
        'orgId':settings.ZOHO_API_ORGID,
        'Authorization':'Zoho-oauthtoken '+token.accessToken,
        'Content-Type':'application/json;charset=UTF-8'
    }
    return header
    
def validateToken(token):
    duration = datetime.now()-token.lastUpdatedTime
    if duration.seconds > token.expiresIn:
        return False
    return True

def renewToken(token):
    params = {
        'refresh_token':token.refreshToken,
        'client_id':token.clientID,
        'client_secret':token.clientSecret,
        'scope':token.scope,
        'grant_type':'refresh_token'
    }
    r = requests.post(settings.ZOHO_REFRESH_TOKEN_URL, params=params)
    if r.status_code != requests.codes.ok:
        return False
    response = r.json()
    token.accessToken = response['access_token']
    token.expiresIn = response['expires_in']
    token.lastUpdatedTime = datetime.now()
    token.save()
    return True
