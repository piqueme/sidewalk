from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.models import User
from models import * 
from qpostform import *
from qpost.models import *
from authenticate.models import *
import random


def post(request):
    if (request.user.is_authenticated()):
        # Form stuff
        post_context = {
            'form' : QuestPostForm(stats=stat_list)
        }
        
        return render(request, 'qpost.html', post_context) 
    else:
        #return HttpResponseRedirect(home)
        return HttpResponseRedirect('../home') 

def submission(request):
    def extractStatsFromForm(form, clean=True):
        q_stat_list = []
        for stat in stat_list:
            if (clean):
                q_stat_list.append(form.cleaned_data[('stat_' + stat)])
            else:
                q_stat_list.append(request.POST[('stat_' + stat)])
        return q_stat_list
    
    def checkStatDistribution(stat_allowance, stats_arr):
        if (sum(stats_arr) <= stat_allowance):
            return True
        return False

    def checkEmptyChallenge(challenge, location):
        if (challenge == 'Description' or challenge == ''):
            return False
        if (location == 'Description' or location == ''):
            return False
        return True

    def checkEmptyQuestHeaders(qname, qdesc):
        if (qname == 'Quest Name' or qname == ''):
            return False
        if (qdesc == 'Description' or qdesc == ''):
            return False
        return True

    if (request.user.is_authenticated()):
        post_context = {}
        if request.method == 'POST':
            form = QuestPostForm(request.POST, request.FILES, stats=stat_list)
            post_context['form'] = form
            error = False
            if form.is_valid():
                quest_name = form.cleaned_data['quest_name']
                q_poster = request.user.username
                existing_quest = Quest.objects.filter(name__exact=quest_name).filter(user_posted_name__exact=q_poster)
                if (len(existing_quest) > 0):
                    post_context['quest_exists'] = True
                    error = True
                photo = request.FILES["quest_icon"]
                q_description = form.cleaned_data['description']
                if not checkEmptyQuestHeaders(qname=quest_name, qdesc=q_description):
                    post_context['quest_headers_empty'] = True
                    error = True
                q_stats = extractStatsFromForm(form) 
                q_challenge_set = []
                challenge_count = 1 
                stat_allowance = 0 
                
                quest = Quest(name=quest_name, user_posted_name=q_poster, icon=photo, description=q_description, stats=q_stats, number_completed_users=0)
                quest.city = request.user.quser.location
                quest.save()
                while ('challenge-' + str(challenge_count)) in request.POST:
                    # Challenges are not part of Django form
                    # Cleaning and validation necessary
                    ch_description = request.POST['challenge-' + str(challenge_count)]
                    ch_location = request.POST['location-' + str(challenge_count)]
                    if not checkEmptyChallenge(ch_description, ch_location):
                        post_context['challenges_empty'] = True
                        error = True
                    challenge = Challenge(quest=quest, description=ch_description, location=ch_location)
                    challenge.save()
                    q_challenge_set.append(challenge)
                    challenge_count += 1
                    stat_allowance += 5
                if not checkStatDistribution(stat_allowance=stat_allowance, stats_arr=q_stats):
                    post_context['bad_stats'] = True
                    error = True
                if (error):
                    quest.delete()
                    return render(request, 'qpost_errors.html', post_context)
                for challenge in q_challenge_set:
                    quest.challenge_set.add(challenge)
                quest.rating = 3
                quest.save()
                quser = request.user.quser
                quser.posted_quests.add(quest)
                return render(request, 'qpost_success.html', post_context)
            else:
                challenge_count = 0 
                stat_allowance = 0 
                while ('challenge-' + str(challenge_count)) in request.POST:
                    # Challenges are not part of Django form
                    # Cleaning and validation necessary
                    ch_description = request.POST['challenge-' + str(challenge_count)]
                    ch_location = request.POST['location-' + str(challenge_count)]
                    if not checkEmptyChallenge(ch_description, ch_location):
                        post_context['challenges_empty'] = True
                    challenge_count += 1
                    stat_allowance += 5
                q_stats = extractStatsFromForm(form) 
                if not checkStatDistribution(stat_allowance=stat_allowance, stats_arr=q_stats):
                    post_context['bad_stats'] = True
                return render(request, 'qpost_errors.html', post_context)
        else:
            return HttpResponseNotFound();
    else:
        return HttpResponseRedirect('../../home')

def quest(request, quest_id, quest_poster):
    if (request.user.is_authenticated()):
        quser = request.user.quser
        poster = User.objects.get(username__exact=quest_poster)
        quest = Quest.objects.filter(id__exact=quest_id) \
            .filter(user_posted_name__exact=poster.username)[0] 
        if not quest or not poster:
            return HttpResponseNotFound("<html><body> The page doesn't exist! </body></html>")
        stats = eval(quest.stats)
        numstats = len(stats)

        photos = getRandomVerificationPhotos(quest, 18, 10)
        challenges = quest.challenge_set.all()

        button_status = ""
        if quest in quser.posted_quests.all():
            button_status = "posted"
        elif quest in quser.current_quests.all():
            button_status = "current"
        elif quest in quser.completed_quests.all():
            button_status = "completed"
        else:
            button_status = "none"

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
        profile_page = '../../profile'
        quest_context = {
            'quest': quest,
            'numrows': numrows,
            'stats': stats,
            'stat_list': stat_list,
            'stat_flavor': stat_flavor,
            'profile_page': profile_page,
            'numcols': numcols,
            'colwidth': colwidth,
            'poster': poster,
            'rows': rows,
            'cols': cols,
            'photos': photos,
            'challenges': challenges,
            'button_status': button_status
        }
        return render(request, 'quest_page.html', quest_context)
    else:
        return HttpResponseRedirect('../../home')

def completion(request, quest_id, quest_poster):
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
        try:
            quest = Quest.objects.get(id=quest_id, user_posted_name=quest_poster)
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
                completion_relation = Completed(completed_user=request.user.quser, completed_quest = quest)
                completion_relation.save()
                questing_relation = Questing.objects.all().filter(current_user=request.user.quser).filter(current_quest=quest)[0]
                questing_relation.delete()
                quest.save()
                return HttpResponse("success") 
            else:
                return HttpResponseRedirect('../')
    else:
        return HttpResponseRedirect('../../../../home')

def accept(request, quest_id, quest_poster):
    if request.user.is_authenticated():
        try:
            quser = request.user.quser
            quest = Quest.objects.get(id=quest_id, user_posted_name=quest_poster)
        except (KeyError, Quest.DoesNotExist):
            return HttpResponseNotFound()
        else:
            # if (quest not in quser.current_quests.all()) and \
            #     (quest not in quser.completed_quests.all()) and \
            #     (quest not in quser.posted_quests.all()):
            #     quser.current_quests.add(quest)
            #     return HttpResponse("success")
            # else:
            #     html = "<html><body> you are not allowed to perform this action </body></html>"
            #     return HttpResponse(html)
            if request.method == "POST":
                if (quest not in quser.current_quests.all()) and \
                    (quest not in quser.completed_quests.all()) and \
                    (quest not in quser.posted_quests.all()):
                    questing_relation = Questing(current_user = quser,
                        current_quest = quest)
                    questing_relation.save()
                    return HttpResponse("success")
                else:
                    return HttpResponse("already-accepted")
            else:
                return HttpResponseRedirect('../../')
    else:
        return HttpResponseRedirect('../../../home')

def forfeit(request, quest_id, quest_poster):
    if request.user.is_authenticated():
        # return render(request, 'quest_success.html', {})
        try:
            quser = request.user.quser
            quest = Quest.objects.get(id=quest_id, user_posted_name=quest_poster)
        except (KeyError, Quest.DoesNotExist):
            return HttpResponseNotFound()
        else:
            if request.method == "POST":
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

def remove(request, quest_id, quest_poster):
    if request.user.is_authenticated():
        try:
            quser = request.user.quser
            quest = Quest.objects.get(id=quest_id, user_posted_name=quest_poster)
        except (KeyError, Quest.DoesNotExist):
            return HttpResponseNotFound
        else:
            if request.method == "POST":
                if quest in quser.posted_quests.all():
                    quest.delete()
                    return HttpResponse("success")
                else:
                    html = "<html><body> you are not allowed to perform this action </body></html>"
                    return HttpResponse(html)
            else:
                return HttpResponseRedirect('../../')
    else:
        return HttpResponseRedirect('../../../home')
            # if request.POST['submit'] == True:
            #     if quest in quser.posted_quests.all():
            #         quest.delete()
            #         html = "<html><body> removed </body></html>"
            #         return HttpResponse(html)
            #     else:
            #         html = "<html><body> you are not allowed to perform this action </body></html>"
            #         return HttpResponse(html)
            # else:
            #     html = "<html><body> you are not allowed to perform this action </body></html>"
            #     return HttpResponse(html)


def getRandomVerificationPhotos(quest, amount, num_last_photos_checked_per_challenge):
    all_challenges = quest.challenge_set
    challenge_set = all_challenges.all()
    if (len(challenge_set) > 0):
        numPhotosPerChallenge = amount / all_challenges.count()
        photo_list = []
        for challenge in challenge_set:
            #last_photos = challenge.questverificationphoto_set.reverse()[:numPhotosPerChallenge]
            last_certificates = challenge.challengecertificate_set.reverse()[:numPhotosPerChallenge]
            last_photos = [last_certificates[i].ver_photo for i in range(len(last_certificates))]
            random_photos = random.sample(last_photos, min(len(last_photos), numPhotosPerChallenge))
            photo_list.extend(random_photos)
        return photo_list[:amount]
    else:
        return []
