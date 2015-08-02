from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from act.models import UserProfile, Activity, CommentInfo, RecordInfo, MyJsonEncoder
from django.forms.models import model_to_dict
from django.core import serializers
import json

# Create your views here.
# createActivity


def create_activity(request):
    if request.method == 'POST':
        a = Activity()
        a.Title = request.POST.get('Title')
        a.Content = request.POST.get('Content')
        a.Keyword = request.POST.get('Keyword')
        a.Image = request.POST.get('Image')
        a.State = request.POST.get('State')
        a.StartTime = request.POST.get('StartTime')
        a.EndTime = request.POST.get('EndTime')
        a.RegisterForm = request.POST.get('RegisterForm')
        username = request.POST.get('username')
        u = UserProfile.objects.get(user__username=username)
        a.UID = u
        a.save()
        return HttpResponse(json.dumps(
            {'status': 'successfully create activity'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': 'create activity failed'}),
                            content_type='application/json')


# getActivityList
def get_activity_list(request):
    if request.method == 'GET':
        actlist = Activity.objects.all()
        '''
        activities = json.dumps([model_to_dict(act) for act in actlist], cls = MyJsonEncoder)
        return HttpResponse(json.dumps(
            {'status': 'done', 'activities': activities}), cls = MyJsonEncoder, content_type='application/json')
	'''
        activities = serializers.serialize('json', actlist)
        return HttpResponse(activities,
                            content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': 'request acts failed'}),
                            content_type='application/json')

# getActivity


def get_activity(request, SID):
    if request.method == 'GET':
        if SID:
            activity = Activity.objects.get(SID=SID)
            if activity:
                context = {}
                context['title'] = activity.Title
                context['content'] = activity.Content
                context['conductor'] = activity.UID.user.username
                context['isPublic'] = activity.IsPublic
                context['tags'] = activity.Keyword
                context['State'] = activity.State
                context['StartTime'] = activity.StartTime
                context['EndTime'] = activity.EndTime
                return render(request, 'act/act_detail.html', context)
            else:
                raise Http404


# callOffActivity
def call_off_activity(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        sid = request.POST.get('SID')
        a = Activity.objects.get(SID=sid)
        if a.UID.username == username:
            a.State = 'Off'
            a.save()
            return HttpResponse('cancel the activity successfully')
        else:
            return HttpResponse('no such right to cancel the activity')
    else:
        return HttpResponse('not call off activity')


# updateActivity
def update_activity(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        u = UserProfile.objects.get(user__username=username)
        sid = request.POST.get('SID')
        a = Activity.objects.get(SID=sid)
        update_right = False
        for r in RecordInfo.objects.filter(SID=a, UID=u):
            update_right = True
        if a.UID == u:
            update_right = True
        if update_right:
            a.Title = request.POST.get('Title')
            a.Content = request.POST.get('Content')
            a.Keyword = request.POST.get('Keyword')
            a.Image = request.POST.get('Image')
            a.State = request.POST.get('State')
            a.StartTime = request.POST.get('StartTime')
            a.EndTime = request.POST.get('EndTime')
            a.RegisterForm = request.POST.get('RegisterForm')
            return HttpResponse('update successfully')
        else:
            return HttpResponse('no right to update')
    else:
        return HttpResponse('not update activity')
