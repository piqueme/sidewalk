from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from qpost.models import *
from authenticate.models import QUser
from django.db.models import Q
from qpost.qpostform import *
import json
import random
from django.contrib.auth.models import User

def index(request):
    if (request.user.is_authenticated()):
        message = ""
        quest_example = Quest.objects.all()[:1].get()
        stats = eval(quest_example.stats)
        numstats = len(stats)
        if numstats % 2 == 0:
            numrows = 2
            numcols = numstats / 2
            colwidth = max(1, 12 / numcols) 
        else:
            numrows = 3
            numcols = numstats / 3
            colwidth = max(1, 12 / numcols)
        rows = range(numrows)
        cols = range(numcols)
        context_dict = {
            'numrows': numrows,
            'stat_list': stat_list,
            'numcols': numcols,
            'colwidth': colwidth,
            'rows': rows,
            'cols': cols
        }
      
        city_filter = Quest.objects.filter(city=request.user.quser.location)
        quests = city_filter & Quest.objects.order_by('date_posted').reverse()
        qusers = QUser.objects.all()
        qallies = request.user.quser.allies.all()
        if len(qallies) > 10:
            qallies = random.sample(qallies, 10)
        else:
            qallies = random.sample(qusers, 10)
        if len(quests) >= 10:
            quests = quests[:10] 
        context_dict['message'] = message
        context_dict['quests'] = quests
        context_dict['qallies'] = qallies
        return render(request, 'search.html', context_dict)
    else:
        return HttpResponseRedirect('../home')

def submit(request, page=1):
    if request.method == 'GET':
        if request.GET['model'].strip() == 'Adventurer':
            return user_submit(request, page)
        first = True
        message = ""
        quest_example = Quest.objects.all()[:1].get()
        stats = eval(quest_example.stats)
        numstats = len(stats)
        if numstats % 2 == 0:
            numrows = 2
            numcols = numstats / 2
            colwidth = max(1, 12 / numcols) 
        else:
            numrows = 3
            numcols = numstats / 3
            colwidth = max(1, 12 / numcols)
        rows = range(numrows)
        cols = range(numcols)
        context_dict = {
            'numrows': numrows,
            'stat_list': stat_list,
            'numcols': numcols,
            'colwidth': colwidth,
            'rows': rows,
            'cols': cols,
            'first': first
        }
        keywords_string = request.GET['keywords'].strip()
        filter_string = request.GET['filter'].strip()
        order_string = request.GET['order'].strip()
        if 'page' in request.GET:
            page = int(request.GET['page'])
            context_dict['first'] = False
        results = orderQuestKeywords(request.user.quser, keywords_string, filter_string, order_string, page)
        if (len(results) == 0):
            message = "No results found."
        context_dict['message'] = message
        context_dict['quests'] = results
      
        return render(request, 'search_submit.html', context_dict)
    else:
        return HttpResponseRedirect('../../search')

def user_submit(request, page=1):
    if request.method == 'GET':
        first = True
        message = ""
        quser = request.user.quser 
        stats = eval(quser.stats)
        numstats = len(stats)
        if numstats % 2 == 0:
            numrows = 2
            numcols = numstats / 2
            colwidth = max(1, 12 / numcols)
        else:
            numrows = 3
            numcols = numstats / 3
            colwidth = max(1, 12 / numcols)
        rows = range(numrows)
        cols = range(numcols)
        context_dict = {
            'numrows': numrows,
            'stat_list': stat_list,
            'numcols': numcols,
            'colwidth': colwidth,
            'rows': rows,
            'cols': cols,
            'first': first
        }
        keywords_string = request.GET['keywords'].strip()
        if 'page' in request.GET:
            page = int(request.GET['page'])
            context_dict['first'] = False
        results = orderUserKeywords(request.user.quser, keywords_string, page)
        if len(results) == 0:
            message = "No results found."
        context_dict['message'] = message
        context_dict['qusers'] = results
        return render(request, 'search_user_submit.html', context_dict)
    else:
        return HttpResponseRedirect('../../search')

def orderUserKeywords(quser, keywords_string, page=1):
    keywords = keywords_string.split(" ")
    keyword_counts = {}
    for user in User.objects.all():
        keyword_counts[user] = 0

    for word in keywords:
        results = User.objects.filter(Q(username__icontains = word) | \
                    Q(first_name__icontains = word) | \
                    Q(last_name__icontains = word))
        for user in results: 
            keyword_counts[user] += 1
    for key in keyword_counts.keys():
        if keyword_counts[key] == 0:
            keyword_counts.pop(key)
    ordered_users = sorted(keyword_counts, key=keyword_counts.__getitem__, reverse=True)
    ordered_users = [user.quser for user in ordered_users]
    if page > 1:
        return ordered_users[(page - 1)*20: page*20]
    else:
        return ordered_users[:20]

def orderQuestKeywords(quser, keywords_string, filter_string="All", order_string = "Relevance", page=1):
    keywords = keywords_string.split(" ")
    keyword_counts = {}
    for quest in Quest.objects.all():
        keyword_counts[quest] = 0
 
    city_filter = Quest.objects.filter(city=quser.location)
    if filter_string == "Allies'":
        filter_query = Quest.objects.none()
        for ally in quser.allies.all(): 
            if not filter_query:
                filter_query = ally.current_quests.all()
            else:
                filter_query = filter_query | ally.current_quests.all() 
    elif filter_string == "Completed":
        filter_query = quser.completed_quests.all()
    elif filter_string == "Current":
        filter_query = quser.current_quests.all()
    else:
        filter_query = Quest.objects.all()
    filter_query = filter_query & city_filter

    for word in keywords:
        results = filter_query & (Quest.objects.filter(Q(name__icontains = word) | \
            Q(user_posted_name__icontains = word)))
        for quest in results:
            keyword_counts[quest] += 1
    for key in keyword_counts.keys():
        if keyword_counts[key] == 0:
            keyword_counts.pop(key)
    ordered_quests = sorted(keyword_counts, key = keyword_counts.__getitem__, reverse = True)[:100]
    if (order_string == "Recency"):
        ordered_quests = sorted(ordered_quests, key = lambda quest: quest.date_posted, reverse = True)
    elif (order_string == "Rating"):
        ordered_quests = sorted(ordered_quests, key = lambda quest: quest.rating, reverse = True)
    if page > 1: 
        return ordered_quests[(page - 1)*20: page*20]
    else:
        return ordered_quests[:20]

    return ordered_quests

def keywords(request, model="quest"):
    output = []
    city_filter = Quest.objects.filter(city=request.user.quser.location)
    city_user_filter = User.objects.filter(quser__location=request.user.quser.location)
    if (model == "quest"):
        for quest in city_filter:
            output.append(quest.name)
        for user in city_user_filter: 
            output.append(user.username)
    elif (model == "user"):
        for user in User.objects.all():
            output.append(user.username)
            output.append(user.first_name)
            output.append(user.last_name)
    elif (model == "current"):
        for quest in (request.user.quser.current_quests.all() & city_filter):
            output.append(quest.name)
            output.append(quest.user_posted_name)
    elif (model == "completed"):
        for quest in (request.user.quser.completed_quests.all() & city_filter):
            output.append(quest.name)
            output.append(quest.user_posted_name)
    elif (model == "allied"):
        for ally in request.user.quser.allies.all():
            for quest in (ally.current_quests.all() & city_filter):
                output.append(quest.name)
                output.append(quest.user_posted_name)
    return HttpResponse(json.dumps(output))

def search_errors(request):
    return HttpReponse("<html><body> hihi </body></html>")

def query(request, keyword):
    results = Quest.objects.filter(Q(name__icontains = keyword) | 
        Q(user_posted_name__icontains = keyword))
    challenges = Quest.challenges_set.all()

    if not results:
        return render(request, 'search.html', {
            'quests': results,
            'challenges' : challenges,
            'message' : "No results found."
        })

    else:
        return render(request, 'search.html', {
            'quests': results,
            'challenges' : challenges,
        })

# Create your views here.
