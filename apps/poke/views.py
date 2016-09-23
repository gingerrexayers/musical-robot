from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from ..loginreg.models import User
from .models import Poke
# Create your views here.
def index(request):
    if not 'id' in request.session:
        return redirect(reverse('login:index'))
    currentUser = User.manager.get(id=request.session['id'])
    context = {
        'me': currentUser,
        'users': User.manager.all().exclude(id=request.session['id']),
        'pokes': Poke.manager.getPokeList(currentUser)
    }
    return render(request, 'poke/index.html', context)

def poke(request, id):
    poker = User.manager.get(id=request.session['id'])
    pokee = User.manager.get(id=id)
    Poke.manager.poke(poker, pokee)
    return redirect(reverse('pokes:index'))
