from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from itertools import chain
from submitform import *
from qpost.models import *
from django.contrib.auth.models import *

def index(request):
    quser = request.user.quser
    completed_quests = quser.completed_quests.all()
    current_quests = quser.completed_quests.all()
        
    manage_context = {
        'current_quests': current_quests,
        'completed_quests': completed_quests
    }

    return render(request, 'view.html', manage_context)

def current(request):
    quser = request.user.quser
    current_quests = quser.current_quests.all()
    return render(request, 'view.html', {
    	'quests': current_quests,
    })

def completed(request):
    quser = request.user.quser
    completed_quests = quser.completed_quests.all()
    return render(request, 'view.html', {
    	'quests': completed_quests,
    })

