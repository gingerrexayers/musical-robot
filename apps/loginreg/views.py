from django.shortcuts import render, redirect
from .models import User
from django.core.urlresolvers import reverse
import datetime
# Create your views here.

def index(request):
    if not 'errors' in request.session:
        request.session['errors'] = []
    context = {
        'today': str(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))
    }
    return render(request, 'loginreg/index.html', context)

def register(request):
    if request.method=='POST':
        result = User.manager.register(request.POST)

        if result[0]:
            request.session['id'] = result[1].id
            request.session.pop('errors')
            return redirect(reverse('login:success'))
        else:
            request.session['errors'] = result[1]
            return redirect(reverse('login:index'))

def login(request):
    if request.method=='POST':
        result = User.manager.login(request.POST)
        if result[0]:
            request.session['id'] = result[1].id
            request.session.pop('errors')
            return redirect(reverse('login:success'))

def logout(request):
    request.session.pop('id')
    return redirect(reverse('login:index'))

def success(request):
    return redirect(reverse('pokes:index'))
