from django.template import Library
from qpost.models import *
from random import choice
from django.contrib.auth.models import User

register = Library()

@register.filter
def get_range( value ):
    return range( value )

@register.filter
def multiply( value, arg ):
    return value*arg

@register.filter
def getval( index, reflist ):
    if index < len(reflist):
    	return reflist[index]
    return None

@register.filter
def stradd(value, arg):
	return str(value) + "," + str(arg)

@register.filter
def trail_trim(value):
    return ('"' + str(value)[:15] + '..."')

@register.filter
def getquestval(args, qlist):
	arg_list = args.split(",")
	stat_index = int(arg_list[0])
	q_index = int(arg_list[1])
	stats = eval(qlist[q_index].stats)
	return stats[stat_index]

@register.filter
def getflowerquestval(args, qlist):
	arg_list = args.split(",")
	stat_index = int(arg_list[0])
	count = int(arg_list[1])
	upcount = int(arg_list[2])
	q_index = (upcount + 1)*3 + count
	stats = eval(qlist[q_index].stats)
	return stats[stat_index]

@register.filter
def getinactiveval(args, qlist):
	arg_list = args.split(",")
	count = int(arg_list[0])
	upcount = int(arg_list[1])
	q_index = (upcount + 1)*3 + count
	return qlist[q_index]

@register.filter
def getquestname(quest):
	return quest.name

@register.filter
def getquestid(quest):
	return quest.id

@register.filter
def getposterid(quest):
	poster_name = quest.user_posted_name
	poster = User.objects.get(username = poster_name)
	return poster.id

@register.filter
def getpostername(quest):
        poster_name = quest.user_posted_name
        return poster_name

@register.filter
def getqicon(quest):
	return quest.icon

@register.filter
def getqiconurl(quest):
	return quest.icon.url

@register.filter
def getqverification(quest, username):
	photos = []
	for challenge in quest.challenge_set.all():
		for photo in challenge.questverificationphoto_set.all():
			if photo.user_submitted_name == username:
				photos.append(photo)
	return choice(photos)

@register.filter
def getqverificationurl(quest, username):
	urls = []
	for challenge in quest.challenge_set.all():
		for photo in challenge.questverificationphoto_set.all():
			if photo.user_submitted_name == username:
				urls.append(photo.url)
	return choice(urls)

@register.filter
def prefix(text):
	textlist = text.split('_')
	return textlist[0]
