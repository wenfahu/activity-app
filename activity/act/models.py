from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageFieldFile, FileField
import uuid
import json
from django.utils import timezone
import datetime
from time import mktime

# Create your models here.


class MyJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            return str(obj)
        elif isinstance(obj, datetime.date):
            # return int(mktime(obj.timetuple()))
            return obj.isoformat()
        else:
            return super(MyJsonEncoder, self).default(obj)


class UserProfile(models.Model):
    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )
    user = models.OneToOneField(User, related_name = 'userprofile')
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    Gender = models.IntegerField(choices = GENDER_CHOICES)
    Telephone = models.CharField(max_length=20)
    Type = models.IntegerField
    Messages = models.TextField
    Likes = models.TextField
    Comments = models.TextField

    def save(self):
        if not self.avatar:
            return super(UserProfile, self).save()
        super(UserProfile, self).save()
        from PIL import Image
        image = Image.open(self.avatar)
        size = (100, 100)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.avatar.path)

    def __str__(self):
        return self.user.username


class Activity(models.Model):
    SID = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
        default=uuid.uuid4)
    UID = models.ForeignKey(UserProfile, related_name='acts_admin')
    Title = models.CharField(max_length=128)
    Content = models.CharField(max_length=256, default='')
    IsPublic = models.BooleanField(default=True)
    Keyword = models.CharField(max_length=128)
    Members = models.ManyToManyField(User, related_name='acts_in')
    Image = models.ImageField(
        upload_to='activity_images',
        blank=True,
        default='')
    State = models.CharField(max_length=128)
    StartTime = models.DateField(default=timezone.now, null = True, blank = True)
    EndTime = models.DateField(default=timezone.now,null = True, blank = True)
    vote = models.IntegerField(default=0)
    RegisterForm = models.TextField
    BlackList = models.TextField

    @property
    def image(self):
        return self.Image

    @image.setter
    def image(self, value):
        self.Image = value


class CommentInfo(models.Model):
    ID = models.AutoField
    Title = models.CharField(max_length=128)
    Content = models.TextField
    UID = models.ForeignKey(UserProfile)
    SID = models.ForeignKey(Activity, default='')
    State = models.BooleanField(default=True)
    Score = models.IntegerField

    def __str__(self):
        return self.Title


class MessageInfo(models.Model):
    ID = models.AutoField
    UID = models.IntegerField
    TargetID = models.IntegerField
    Title = models.CharField(max_length=54)
    Content = models.TextField
    SendTime = models.DateField
    StateFrom = models.BooleanField(default=True)
    StateTo = models.BooleanField(default=True)

    def __str__(self):
        return self.Title
