from django.db import models
from django.contrib.auth.models import User
from qpost.models import *
from django.contrib.auth.models import User
import datetime

# Create your models here.
class QUser(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length = 60)
    icon = models.ImageField(upload_to = 'icons/user', 
    	blank = True, null = True)
    npc_rating = models.DecimalField(max_digits = 6, decimal_places = 3, 
		null=True, blank=True)
    description = models.TextField(blank = True, null = True, max_length=200)
    stats = models.CommaSeparatedIntegerField(max_length = 100)
    # completed_quests = models.ManyToManyField(Quest, 
    #        related_name = 'completed_quests', blank = True)
    # current_quests = models.ManyToManyField(Quest, 
    #        related_name = 'current_quests', blank = True)
    posted_quests = models.ManyToManyField(Quest, 
           related_name = 'posters', blank = True)
    completed_quests = models.ManyToManyField(Quest, through='Completed', 
           symmetrical=False, related_name='completers', blank=True)
    current_quests = models.ManyToManyField(Quest, through='Questing',
           symmetrical=False, related_name='questers', blank=True)
    allies = models.ManyToManyField('self', symmetrical=True)

    def __unicode__(self):
        return self.user.username

    def save(self):
        super(QUser, self).save()
        if self.icon:
            THUMBNAIL_SIZE = (256, 256)
            filename = str(self.icon.path)

            image = Image.open(filename)
            image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
            image.save(filename)
            
class Questing(models.Model):
    current_user = models.ForeignKey(QUser)
    current_quest = models.ForeignKey(Quest)
    date_taken = models.DateTimeField(auto_now_add = True)

class Completed(models.Model):
    completed_user = models.ForeignKey(QUser)
    completed_quest = models.ForeignKey(Quest)
    date_completed = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    poster = models.ForeignKey(QUser)
    comment = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    quest = models.ForeignKey(Completed)


    
