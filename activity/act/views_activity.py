from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from act.models import UserProfile, Activity, CommentInfo, RecordInfo

# Create your views here.
# createActivity
def create_activity(request):
    if request.method == 'POST':
        a = Activity().objects.create()
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
        return HttpResponse('create successfully')
    else:
        return HttpResponse('not create')


# getActivityList
def get_activity_list(request):
    if request.method == 'POST':
        actlist = Activity.objects.all()
        return render(request, 'xxx.html', actlist)
    else:
        return HttpResponse('not get activity list')

# getActivity
def get_activity(request):
    if request.method == 'POST':
        sid = request.POST.get('SID')
        if sid:
            a = Activity.objects.get(SID=sid)
            if a:
                return render(request, 'xxx.html', a)
            else:
                return HttpResponse('no such activity')
        else:
            title = request.POST.filter('Title')
            content = request.POST.filter('Content')
            state = request.POST.filter('State')
            starttime = request.POST.filter('StartTime')
            endtime = request.POST.filter('EndTime')
            alist = Activity.objects.all()
            if title:
                alist = alist.filter(Title__contains=title)
            if content:
                alist = alist.filter(Content__contains=content)
            if state:
                alist = alist.filter(State__contains=state)
            if starttime:
                alist = alist.filter(StartTime__contains=starttime)
            if endtime:
                alist = alist.filter(Endtime__contains=endtime)
            return render(request, 'xxx.html', alist)
    else:
        return HttpResponse('not get activity')


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
