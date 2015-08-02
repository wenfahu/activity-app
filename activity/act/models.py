from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageFieldFile, FileField
import uuid
import json
from django.utils import timezone

# Create your models here.


class MyJsonEncoder(json.JSONEncoder):

    def default(self, img):
        if isinstance(img, ImageFieldFile):
            return super(MyJsonEncoder, self).default(str(img))
        else:
            return super(MyJsonEncoder, self).default(img)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    Gender = models.CharField(max_length=128)
    Telephone = models.CharField(max_length=20)
    Type = models.IntegerField
    Messages = models.TextField
    Likes = models.TextField
    Comments = models.TextField

    def __str__(self):
        return self.user.username


class Activity(models.Model):
    SID = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
        default=uuid.uuid4)
    UID = models.ForeignKey(UserProfile)
    Title = models.CharField(max_length=128)
    Content = models.CharField(max_length=256, default = '')
    IsPublic = models.BooleanField(default=True)
    Keyword = models.CharField(max_length=128)
    Image = models.ImageField(
        upload_to='activity_images',
        blank=True,
        default='')
    State = models.CharField(max_length=128)
    StartTime = models.DateField(default= timezone.now())
    EndTime = models.DateField(default= timezone.now())
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


class RecordInfo(models.Model):
    ID = models.AutoField
    UID = models.ForeignKey(UserProfile)
    SID = models.ForeignKey(Activity)
    Content = models.TextField
    IsPublic = models.BooleanField(default=True)
    Type = models.CharField(max_length=128, default='normal')

    def __str__(self):
        return self.Type


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
