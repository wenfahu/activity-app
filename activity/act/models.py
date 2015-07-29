from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to = 'profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Activity(models.Model):
    SID = models.AutoField
    Title = models.CharField(max_length=128)
    Content = models.TextField
    IsPublic = models.BooleanField(default=True)
    Keyword = models.CharField(max_length=128)
    Image = models.ImageField(upload_to = 'activity_images', blank=True)
    Comments = models.ForeignKey(UserProfile)
    State = models.CharField(max_length=128)
    StartTime = models.DateField
    EndTime = models.DateField
    RegisterForm = models.TextField
    BlackList = models.TextField

    def __str__(self):
        return self.SID


class CommentInfo(models.Model):
    ID = models.AutoField
    Title = models.CharField(max_length=128)
    Content = models.TextField
    UID = models.ForeignKey(UserProfile)
    SID = models.ForeignKey(Activity)
    State = models.BooleanField(default=True)
    Score = models.IntegerField

    def __str__(self):
        return self.ID

