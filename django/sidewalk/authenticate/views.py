from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.template import RequestContext
from authform import *
from models import *
from qpost.qpostform import *
import re
# from django.views.generic.base import TemplateView

def get_recent_comments(quser):
    completed_quests = quser.completed_set.all()
    comments = completed_quests[0].comment_set.all()
    for completed_quest in completed_quests:
        comments = comments | completed_quest.comment_set.all()
    ordered_comments = comments.order_by('date_posted').reverse()[:10]
    return ordered_comments

def comments(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            recent_comments = get_recent_comments(request.user.quser)
            return render(request, 'comments_table.html', { 'comments': recent_comments })
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseRedirect('../home')

# Create your views here.
def index(request):
    return HttpResponseRedirect('home/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('../home/')

def home(request):
    if not request.user.is_authenticated():
        login_form = LoginForm(prefix='login')
        reg_form = RegistrationForm(prefix='registration')
        home_context = {
            'login_form': login_form,
            'reg_form': reg_form
        }
        return render(request, 'home.html', home_context) 
    else:
        return HttpResponseRedirect('../dash/')

def login_view(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            if 'login' in request.POST:
                login_form = LoginForm(request.POST, prefix='login')
                if login_form.is_valid():
                    #...Handle login
                    username = login_form.cleaned_data['username']
                    password = login_form.cleaned_data['password']
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            return HttpResponse("success")
                        else:
                            return HttpResponse("old_user")
                            #return displayHomeWithContext(request, expired_acc=username)
                    else:
                        return HttpResponse("bad_login")
                else:
                    login_response_context = { login_form }
                    if not request.POST['login-username'] or not request.POST['login-password']:
                        return HttpResponse('bad_login')
                    return render(request, 'login_alerts.html', login_response_context)
            else:
                return HttpResponseNotFound();
        else:
            return HttpResponseNotFound();
    else:
        return HttpResponseRedirect("../dash")

def register(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            if 'registration' in request.POST: 
                reg_form = RegistrationForm(request.POST, prefix = 'registration')
                if reg_form.is_valid():
                    #...Handle registration
                    first_name = reg_form.cleaned_data['first_name']
                    last_name = reg_form.cleaned_data['last_name']
                    username = reg_form.cleaned_data['username']
                    password = reg_form.cleaned_data['password']
                    ver_password = reg_form.cleaned_data['verify_password']
                    email = reg_form.cleaned_data['email']
                    ver_email = reg_form.cleaned_data['verify_email']
                    location = reg_form.cleaned_data['location']
                    agreement = (request.POST.get('agree', 'whe') == "on")
        

                    response_string = ''
                    existing_users = User.objects.filter(username__exact=username)
                    existing_email = User.objects.filter(email__exact=email)
                    if (len(existing_users) > 0):
                        response_string += 'user_exists'
                    if (len(existing_email) > 0):
                        response_string += '&email_exists'
                    else:
                        response_string += '&'
                    if not (password == ver_password):
                        response_string += '&verify_password_fail'
                    else:
                        response_string += '&'
                    if not (email == ver_email):
                        response_string += '&verify_email_fail'
                    else:
                        response_string += '&'
                    if not agreement:
                        response_string += '&not_agree'
                    else:
                        response_string += '&'
                    if not (re.match('^[a-zA-Z0-9]+$', username)):
                        response_string += '&invalid_user'
                    if len(response_string) > 4:
                        return HttpResponse(response_string)

                    user = User.objects.create_user(username=username, email=email, password = password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    quser = QUser(user=user, location=location, 
                    stats = "0, 0, 0, 0, 0, 0, 0, 0, 0")
                    quser.save()
                    path = "staticfiles/images/default_icon.png"
                    f = File(open(path, 'rb'))
                    quser.icon.save('default_icon.png', f)

                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return HttpResponse('success')
                else:
                    register_context = {'reg_form': reg_form}
                    return render(request, 'register_alerts.html', register_context)
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseRedirect("../dash")

def get_allies_quests(quser):
    allies = quser.allies.all()
    ally_quests = []
    for ally in allies:
        quests = ally.questing_set.all()
        ally_quests.extend(quests)
    date_sorted_ally_quests = sorted(ally_quests, key=lambda quest: quest.date_taken, reverse=True)
    #date_sorted_ally_quests = [rel_quest.current_quest for rel_quest in date_sorted_ally_quests]
    return date_sorted_ally_quests

def dash(request):
    if request.user.is_authenticated():
        quser = request.user.quser
        current_quests = quser.questing_set.order_by('date_taken').reverse()[:10]
        current_quests = [questing.current_quest for questing in current_quests]
        #all_quests_db = Quest.objects.reverse()[:10]
        ally_quests = get_allies_quests(quser)[:10]
        city_filter = Quest.objects.filter(city=quser.location)
        daily_quest = (Quest.objects.order_by('rating').reverse() & city_filter)[0]
        dash_context = {
            'current_quests': current_quests,
            'ally_quests': ally_quests,
            'daily_quest': daily_quest, 
        }
        return render(request, 'dash.html', dash_context) 
    else:
        return HttpResponseRedirect('../home/')

def dash_next_current_page(request):
    if request.method == 'GET':
        current_page = int(request.GET['page'])
        quser = request.user.quser
        current_quests = quser.questing_set.order_by('date_taken').reverse()[10*current_page:10*(current_page + 1)]
        current_quests = [questing.current_quest for questing in current_quests]
        next_current_page_context = {
            'current_quests': current_quests
        }
        return render(request, 'current_quests_table.html', next_current_page_context)
    else:
        return HttpResponseRedirect('../dash/')

def dash_next_allied_page(request):
    if request.method == 'GET':
        current_page = int(request.GET['page'])
        quser = request.user.quser
        ally_quests = get_allies_quests(quser)[10*current_page:10*(current_page + 1)]
        next_ally_page_context = {
            'ally_quests': ally_quests
        }
        return render(request, 'ally_quests_table.html', next_ally_page_context)
    else:
        return HttpResponseRedirect('../dash/')

def complete_challenges_form(request):
    if request.method == 'GET':
        quest_id = int(request.GET['quest_id'])
        user_posted_name = request.GET['user_posted_name']
        quest = Quest.objects.get(id = quest_id)
        challenges = quest.challenge_set.all()
        return render(request, 'quest_complete_form.html', {
            'challenges': challenges,
            'quest': quest
        })
    else:
        return HttpResponseRedirect('../dash/')

def completion(request):
    def addStatsToUser(user, qstats):
        quser = user.quser
        quest_stats = eval(qstats)
        quser_stats = eval(quser.stats)
        stats_string = ''
        for index in range(len(quest_stats)):
            new_stat = (quest_stats[index] + quser_stats[index])
            stats_string += str(new_stat)
            if not index == (len(quest_stats) - 1):
                stats_string += ','
        quser.stats = stats_string
        quser.save()
    
    if request.user.is_authenticated():
        if request.method == "POST":
            quest_id = int(request.POST.get('quest_id'))
            poster_name = request.POST['user_posted_name']
            try:
                quser = request.user.quser
                quest = Quest.objects.get(id=quest_id, 
                    user_posted_name=poster_name)
            except (KeyError, Quest.DoesNotExist):
                return HttpResponseNotFound()
            else:
                complete_context = {}
                if request.method == 'POST':
                    error = False
                    challenge_certs = []
                    challenges = quest.challenge_set.all()
                    if ('rating' not in request.POST):
                        complete_context['no_rating'] = True
                        error = True
                    else:
                        rating = float(request.POST['rating'])
                    for i in range(1, len(challenges) + 1):
                        submitting_user = request.user.username
                        photo_tag = 'verify-image-' + str(i)
                        notes_tag = 'verify-notes-' + str(i)
                        if photo_tag not in request.FILES:
                            complete_context['no_photo'] = True
                            error = True
                            ver_photo = None
                        else:
                            ver_photo = request.FILES[photo_tag]
                        ver_notes = request.POST[notes_tag]
                        challenge_cert = ChallengeCertificate(user_submitted_name=submitting_user, challenge=challenges[i - 1], ver_photo=ver_photo, ver_notes=ver_notes)
                        challenge_certs.append(challenge_cert)
                    if error:
                        return render(request, 'completion_errors.html', complete_context)
                    for challenge_cert in challenge_certs:
                        challenge_cert.save()
                    addStatsToUser(request.user, quest.stats)
                    quest.rating = ((quest.rating * quest.number_completed_users + rating) / (quest.number_completed_users + 1))
                    quest.number_completed_users += 1
                    completion_relation = Completed(completed_user = request.user.quser, completed_quest = quest)
                    completion_relation.save()
                    questing_relation = Questing.objects.all().filter(current_user=request.user.quser).filter(current_quest=quest)[0]
                    questing_relation.delete()
                    quest.save()
                    return HttpResponse("success") 
                else:
                    return HttpResponseRedirect('../')
        else:
            return HttpResponse(html)
    else:
        return HttpResponseRedirect('../../../../home')

def forfeit(request):
    if request.user.is_authenticated():
        # return render(request, 'quest_success.html', {})
        if request.method == "POST":
            quest_id = int(request.POST.get('quest_id'))
            poster_name = request.POST['user_posted_name']

            try:
                quser = request.user.quser
                quest = Quest.objects.get(id=quest_id, user_posted_name=poster_name)
            except (KeyError, Quest.DoesNotExist):
                return HttpResponseNotFound()
            else:
                if quest in quser.current_quests.all():
                    questing_relation = quser.questing_set.get(current_quest = quest)
                    questing_relation.delete()
                    return HttpResponse("success")
                else:
                    html = "<html><body> you are not allowed to perform this action </body></html>"
                    return HttpResponse("already-forfeited")
        else:
            return HttpResponseRedirect('../../')
    else:
        return HttpResponseRedirect('../../../home')

def profile(request, username):
    def getRandomAllies(user):
        quser = user.quser
        allies = quser.allies.all()
        if (len(allies) > 50):
            allies = random.sample(allies, 50)
        return allies

    if (request.user.is_authenticated()):
        try:
            user = User.objects.get(username = username)
        except (KeyError, User.DoesNotExist):
            return render(request, 'profile.html', {
                'error_message': 'This user does not exist',
            })
        else:
            timeline = False
            quest_id = False
            if request.method == "POST":
                if 'timeline' in request.POST:
                    if request.POST['timeline'] == 'timeline':
                        timeline = True
                if 'quest-id' in request.POST:
                    quest_id = request.POST['quest-id']

            original_quser = request.user.quser
            quser = user.quser
            username = user.username
            current_quests = quser.current_quests.all()
            completed_quests = quser.completed_quests.all()
            posted_quests = quser.posted_quests.all()
            in_allies = (len(original_quser.allies.filter(user__username__exact=username)) > 0)
            
            if request.user.username == username:
                original = True
            else:
                original = False

            if (in_allies):
                ally = True
            else:
                ally = False

            if len(current_quests) == 0:
                inactive_current_rows = 0
            else:
                inactive_current_rows = (len(current_quests) - 1)/3

            if len(completed_quests) == 0:
                inactive_completed_rows = 0
            else:
                inactive_completed_rows = (len(completed_quests) - 1)/3

            if len(posted_quests) == 0:
                inactive_posted_rows = 0
            else:
                inactive_posted_rows = (len(posted_quests) - 1)/3

            stats = eval(quser.stats)
            numstats = len(stats)
            if numstats % 2 == 0:
                numrows = 2
                numcols = numstats / 2
                colwidth = 12 / numcols 
            else:
                numrows = 3
                numcols = numstats / 3
                colwidth = 12 / numcols
            rows = range(numrows)
            cols = range(numcols)

            profile_page = '../profile'
            allies = getRandomAllies(request.user)
            if not quest_id:
                quest_id = ""
            profile_context = {
                'original': original,
                'quser': quser,
                'username': username,
                'ally': ally,
                'current_quests': current_quests,
                'completed_quests': completed_quests,
                'posted_quests': posted_quests,
                'numrows': numrows,
                'stats': stats,
                'stat_list': stat_list,
                'stat_flavor': stat_flavor,
                'profile_page': profile_page,
                'numcols': numcols,
                'colwidth': colwidth,
                'rows': rows,
                'cols': cols,
                'inactive_current_rows': inactive_current_rows,
                'inactive_completed_rows': inactive_completed_rows,
                'inactive_posted_rows': inactive_posted_rows,
                'timeline': timeline,
                'quest_id': quest_id,
                'allies': allies
            }
            return render(request, 'profile.html', profile_context)
    else:
        return HttpResponseRedirect('../../home/')

def make_ally(request, username):
    if (request.user.is_authenticated()):
        try:
            ally_user = User.objects.get(username = username)
        except (KeyError, User.DoesNotExist):
            return render(request, 'profile.html', {
                'error_message': 'This user does not exist',
            })
        else:
            if request.method == "POST":
                ally = ally_user.quser
                original = request.user.quser
                if ally not in original.allies.all():
                    original.allies.add(ally)
                    return HttpResponse("success")
                else:
                    return HttpResponse("already-allies")
            else:
                return HttpResponseRedirect('../')
    else:
        return HttpResponseRedirect('../../../home')

def remove_ally(request, username):
    if (request.user.is_authenticated()):
        try:
            ally_user = User.objects.get(username = username)
        except (KeyError, User.DoesNotExist):
            return render(request, 'profile.html', {
                'error_message': 'This user does not exist',
            })
        else:
            if request.method == "POST":
                ally = ally_user.quser
                original = request.user.quser
                if ally in original.allies.all():
                    original.allies.remove(ally)
                    return HttpResponse("success")
                else:
                    return HttpResponse("already-not-allies")
            else:
                return HttpResponseRedirect('../')
    else:
        return HttpResponseRedirect('../../../home')


def timeline(request, username):
    if request.user.is_authenticated():
        user = User.objects.get(username = username)
        quser = user.quser #PERSON WHO PROFILE YOU'RE VIEWING
        quser_original = request.user.quser #PERSON YOU ARE MOFO
        in_allies = (len(quser_original.allies.filter(user__username__exact=username)) > 0)
        original = (quser_original.user.username == username)
        if (in_allies or original):
            completed_relations_sorted = []
            completed_quests = quser.completed_quests.all()
            completed_quests_sorted = completed_quests.order_by(
                "completed__date_completed")
            for quest in completed_quests_sorted:
                relation = Completed.objects.get(completed_user = quser,
                    completed_quest = quest)
                completed_relations_sorted.append(relation)
            quest_first = completed_quests[0]
            relation_first = Completed.objects.get(completed_user = quser,
                completed_quest = quest_first)
            comments_first = Comment.objects.filter(quest = relation_first)
            comments_sorted_first = comments_first.order_by("date_posted")

            completed_relations_sorted = completed_relations_sorted[::-1]
            completed_quests_sorted = completed_quests_sorted[::-1]

            time_differences = []
            for i in range(len(completed_relations_sorted) - 1):
                diff = completed_relations_sorted[i + 1].date_completed - \
                    completed_relations_sorted[i].date_completed
                time_differences.append(diff.total_seconds())
            
            first_time = completed_relations_sorted[0].date_completed
            last_time = completed_relations_sorted[-1].date_completed
            first_last_diff = (last_time - first_time).total_seconds()

            comment_scroll = False
            if (request.method == 'POST'):
                comment_scroll = True
                comment_id = int(request.POST['comment_id'])
                comment_div_id = "" #fix this later
                return render(request, 'timeline.html', {
                    'completed_quests_sorted': completed_quests_sorted,
                    'comments_sorted_first': comments_sorted_first,
                    'quest_first': quest_first,
                    'comment_div_id': comment_div_id,
                    'comment_scroll': comment_scroll,
                    'completed_relations_sorted': completed_relations_sorted,
                    'time_differences': time_differences,
                    'first_last_diff': first_last_diff
                })
            else:
                return render(request, 'timeline.html', {
                    'completed_quests_sorted': completed_quests_sorted,
                    'comments_sorted_first': comments_sorted_first,
                    'quest_first': quest_first,
                    'comment_scroll': comment_scroll,
                    'completed_relations_sorted': completed_relations_sorted,
                    'time_differences': time_differences,
                    'first_last_diff': first_last_diff
                })

        else:
            return HttpResponseRedirect('../')
    else:
        return HttpResponseRedirect('../../home/')

def timeline_quest(request, username):
    if (request.method == "GET"):
        quest_id = int(request.GET['quest_id'])
        #user_posted_name = int(request.GET['quest_id'])
        try:
            user = User.objects.get(username = username)
            quser = user.quser #ally
            quest = Quest.objects.get(id = quest_id)
        except (KeyError, User.DoesNotExist):
            return HttpResponseNotFound();
        else:
            relation = Completed.objects.get(completed_user = quser,
                completed_quest = quest)
            challenge_certificates = []
            for challenge in quest.challenge_set.all():
                challenge_certificates.append(challenge.challengecertificate_set.filter(user_submitted_name=user.username)[0])
            comments = Comment.objects.filter(quest = relation)
            comments_sorted = comments.order_by("date_posted")
            return render(request, 'timeline_quest.html', {
                'quest': quest,
                'comments_sorted': comments_sorted,
                'challenge_certificates': challenge_certificates,
                'username_ally': username
            })
    else:
        return HttpResponseRedirect('../../')

def comment(request, username):
    if (request.method == "POST"):
        quest_id = int(request.POST['quest_id'])
        try:
            user = User.objects.get(username = username)
            quser_ally = user.quser
            quest = Quest.objects.get(id = quest_id)
        except (KeyError, Quest.DoesNotExist):
            return HttpResponseNotFound();
        else:
            relation = Completed.objects.get(completed_user = quser_ally,
                completed_quest = quest)
            username_poster = request.POST['username_poster']
            poster_user = User.objects.get(username = username_poster)
            poster = poster_user.quser
            comment_text = request.POST['comment']
            comment = Comment(poster = poster, comment = comment_text,
                quest = relation)
            comment.save()
            return render(request, 'timeline_comment.html', {
                'comment': comment
            })
    else:
        return HttpResponseRedirect('../../')



def settings(request):
    if (request.user.is_authenticated()):
        return render(request, 'account_settings.html', { 'user':request.user})
    else:
        return HttpResponseRedirect('../home/')

def settings_submit(request):
    if (request.user.is_authenticated()):
        if (request.method == "POST"):
            first_name = request.POST['first-name'].strip()
            last_name = request.POST['last-name'].strip()
            description = request.POST['description'].strip()
            password = request.POST['password'].strip()
            email = request.POST['email'].strip()
            location = request.POST['location'].strip()
            if ('user-icon' in request.FILES):
                icon = request.FILES['user-icon']
                request.user.quser.icon = icon
                request.user.quser.save()

            settings_context = {}
            error = False
            if (not first_name) and (not last_name) and (not description) and (not password) and (not email) and (not location) and (not 'user-icon' in request.FILES):
                settings_context['all_empty'] = True
                error = True
                return render(request, 'settings_submission.html', settings_context)
    
            if (first_name and last_name):
                request.user.first_name = first_name
                request.user.last_name = last_name
            elif ((first_name and not last_name) or (last_name and not first_name)):
                settings_context['empty_name'] = True
                error = True

            if (description and not (re.match('^(\w|\s|.|\?|!|\')+', description))):
                settings_context['not_valid_uname'] = True
                error = True
            elif (description):
                request.user.quser.description = description
                request.user.quser.save()

            if (password):
                request.user.password = password
                
            if (email and not (re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))) :
                settings_context['not_valid_email'] = True
                error = True
            elif (email):
                request.user.email = email

            if (location):
                request.user.quser.location = location
                request.user.quser.save()

            if not error:
                settings_context['success'] = True
            request.user.save() 
            context = RequestContext(request, settings_context)
            return render(request, 'settings_submission.html', settings_context) 

        else:
            return HttpResponseNotFound()
    else:
        return HttpRedirectRequest("../../home")
def help(request):
    if (request.user.is_authenticated()):
        return render(request, 'help.html', {'user': request.user})
    else:
        return HttpResponseRedirect('../home')
