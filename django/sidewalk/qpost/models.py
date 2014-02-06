from django.db import models
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class Quest(models.Model):
    name = models.CharField(max_length = 200)
    user_posted_name = models.CharField(max_length = 60)
    description = models.TextField()
    city = models.CharField(max_length = 60)
    icon = models.ImageField(upload_to='icons/quest', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    stats = models.CommaSeparatedIntegerField(max_length = 200)
    average_npc = models.DecimalField(max_digits = 6, decimal_places = 3, 
        null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    number_completed_users = models.IntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return u"%s posted by %s" % (self.name, self.user_posted_name)
    def save(self):
        super(Quest, self).save()
        if self.icon:
            THUMBNAIL_SIZE = (256, 256)
            filename = str(self.icon.path)
            image = Image.open(filename)
            image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
            image.save(filename)

        # if miniature and self.photo:
  #           filepath = self.photo.path
  #           size = settings.PHOTO_SIZE # 200
  #           identifier = '_%d.' % size
  #           if filepath.find(identifier) == -1:
  #               image = Image.open(filepath)
  #               image.thumbnail([size, size], Image.ANTIALIAS)
  #               new_filepath = filepath.split('.')
  #               new_filepath = '.'.join(new_filepath[:-1]) + identifier + new_filepath[-1].lower()
  #               try:
  #                   image.save(new_filepath, image.format, quality=90, optimize=1)
  #               except:
  #                   image.save(new_filepath, image.format, quality=90)
  #               # use resized image for photo
  #               photo_name = self.photo.name.split('.')
  #               photo_name = '.'.join(photo_name[:-1]) + identifier + photo_name[-1].lower()
  #               self.photo = photo_name
  #               self.save(miniature=False)
  #               # remove old image
  #               os.remove(filepath) - See more at: http://nanvel.name/weblog/django-resize-image-save/#sthash.hSaTlIxU.dpuf

        # DJANGO_TYPE = self.icon.file.content_type
        # if DJANGO_TYPE == 'image/jpeg':
        #   PIL_TYPE = 'jpeg'
        #   FILE_EXTENSION = 'jpg'
        # elif DJANGO_TYPE == 'image/png':
        #   PIL_TYPE = 'png'
        #   FILE_EXTENSION = 'png'


class Challenge(models.Model):
    quest = models.ForeignKey(Quest)
    description = models.TextField()
    location = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.description

#class QuestVerificationPhoto(models.Model):
#    challenge = models.ForeignKey(Challenge)
#    user_submitted_name = models.CharField(max_length = 60)
#    photo = models.FileField(upload_to='verification_photos')
#    #photo_str = models.CharField(max_length = 60)
#
#    def __unicode__(self):
#       return u"Verification Photo for %s" % self.challenge.description

class ChallengeCertificate(models.Model):
    challenge = models.ForeignKey(Challenge)
    user_submitted_name = models.CharField(max_length = 60)
    ver_photo = models.ImageField(upload_to='verification_photos')
    ver_notes = models.TextField()
    def __unicode__(self):
        return u"Challenge certificate for %s" %self.challenge.description
    
    def save(self):
        super(ChallengeCertificate, self).save()
        if self.ver_photo:
            THUMBNAIL_SIZE = (256, 256)
            filename = str(self.ver_photo.path)
            image = Image.open(filename)
            image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
            image.save(filename)
