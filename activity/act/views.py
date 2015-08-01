from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from act.forms import UserForm, UserProfileForm
from act.models import UserProfile, Activity, CommentInfo, RecordInfo
from act.views_user import *
from act.views_activity import *
import json

# Create your views here.


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'act/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('your account is disabled')
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'act/login.html', {})


# requestInfo
def request_user_info(request, user_name):
    if request.method == 'GET':
        user = UserProfile.objects.get(user__username=user_name)
        if user:
            res = {'username': user.user.username,
                   # 'avatar': user.avatar,
                   'Gender': user.Gender,
                   'Telephone': user.Telephone,
                   'Email': user.user.email,
                   #'Type': user.Type}
                   }
            return HttpResponse(
                json.dumps(res), content_type='application/json')
#         return render(request,
#                       'act/request_user_info.html',
#                       {'username': user.user.username,
#                        # 'avatar': user.avatar,
#                        'Gender': user.Gender,
#                        'Telephone': user.Telephone,
#                        'Email': user.user.email,
#                        #'Type': user.Type}
#                        })

        else:
            return HttpResponse(
                json.dumps({'error': 'not found'}),
                content_type='application/json')

# updateProfile


'''
def update_user(request, user_name=None):
    if request.method == 'POST':
        return HttpResponse(json.dumps({'username': user_name}),
                            content_type='application/json')
'''


def update_user(request, user_name=''):
    if request.is_ajax():
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('oldpassword')
            user = authenticate(username=user_name, password=password)
            if user:
                if user.is_active:
                    password = request.POST.get('newpassword')
                    user.set_password(password)
                    user.email = email
                    user.save()
                    return HttpResponse(json.dumps({'status': 'succeed'}),
                                        content_type='application/json'
                                        )
                else:
                    return HttpResponse(
                        json.dumps({'status': 'account disabled'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"status": "wrong password."}),
                                    content_type='application/json'
                                    )
        else:
            user = UserProfile.objects.get(user__username=user_name)
            return render(request, 'act/update_user_info.html',
                          {'username': user_name,
                           'email': user.user.email})


# createActivity
def create_activity(request):
    if request.method == 'POST':
        a = Activity.objects.create()
        a.Title = request.POST.get('Title')
        a.Content = request.POST.get('Content')
        a.Keyword = request.POST.get('Keyword')
        a.Image = request.POST.get('Image')
        a.State = request.POST.get('State')
        a.StartTime = request.POST.get('StartTime')
        a.EndTime = request.POST.get('EndTime')
        a.RegisterForm = request.POST.get('RegisterForm')
        username = request.POST.get('username')
        u = UserProfile.objects.get(username=username)
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
    if request.methon == 'POST':
        username = request.POST.get('username')
        u = UserProfile.objects.get(username=username)
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
