from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from act.forms import UserForm, UserProfileForm
from act.models import UserProfile, Activity, CommentInfo, MessageInfo, MyJsonEncoder
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import bson
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

            return HttpResponseRedirect('/act/login')

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
                return HttpResponseRedirect('/act/dashboard')
            else:
                return HttpResponse('your account is disabled')
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'act/login.html', {})

def request_user_page(request, user_name):
    if request.method == 'GET':
        return render(request, 'act/user_info.html', { 'username' : user_name})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('you are not online')

@login_required
def dashboard(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'act/dashboard.html', {'user' : user})


# requestInfo
def request_user_info(request, user_name):
    if request.method == 'GET':
        user = UserProfile.objects.get(user__username=user_name)
        if user:
            acts = user.user.acts_in.all()
            acts_admin = user.acts_admin.all()
            acts_admin_list = [ dict(zip(['title', 'start_time', 'end_time', 'sid'], [act.Title, act.StartTime, act.EndTime, act.SID])) for act in acts_admin]
            act_list = [ dict(zip(['title', 'start_time', 'end_time', 'sid'], [act.Title, act.StartTime, act.EndTime, act.SID])) for act in acts]
            res = {'username': user.user.username,
                   'avatar': user.avatar,
                   'Gender': user.Gender,
                   'acts' : act_list,
                   'acts_admin': acts_admin_list,
                   'Telephone': user.Telephone,
                   'Email': user.user.email,
                   'acts_count' : len(act_list),
                   'acts_admin_count' : len(acts_admin_list),
                   #'Type': user.Type}
                   }
            return HttpResponse(
                json.dumps(res, cls = MyJsonEncoder), content_type='application/json')

        else:
            return HttpResponse(
                json.dumps({'error': 'not found'}),
                content_type='application/json')

# updateProfile


@login_required
def update_user(request):
    if request.is_ajax():
        if request.method == 'POST':
            user_name = request.user.username
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


# write a message
@login_required
def edit_message(request):
    if request.method == 'POST':
        m = MessageInfo()
        usrname = request.POST.get('username')
        m.UID = UserProfile.objects.get(user__username=usrname).id
        m.TargetID = request.POST.get('Target')
        m.Title = request.POST.get('Title')
        m.Content = request.POST.get('Content')
        m.save()
        return HttpResponse('email has been sent!')
    else:
        return HttpResponse('New Message?')

# write a comment


@login_required
def edit_comment(request):
    if request.method == 'POST':
        c = CommentInfo()
        usrname = request.POST.get('username')
        c.UID = UserProfile.objects.get(user__username=usrname)
        c.Title = request.POST.get('Title')
        c.Content = request.POST.get('Content')
        c.save()
        return HttpResponse('comment has been sent!')
    else:
        return HttpResponse('New Comment?')


# participate an activity
@login_required
def participate_activity(request, SID):
    if request.method == 'POST':
        # usrname = request.POST.get('username')
        user = request.user
        # print (user)
        act = Activity.objects.get(SID=SID)
        act.Members.add(user)
        return JsonResponse({'status': 'added'})


@login_required
def quit_activity(request, SID):
    if request.method == 'POST':
        user = request.user
        act = Activity.objects.get(SID=SID)
        act.Members.remove(user)
        return JsonResponse({'status': 'removed'})


def get_user_list(request):
    if request.method == 'GET':
        context = {}
        try:
            users = UserProfile.objects.all()
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'not found'})
        user_list = []
        for user in users:
            item = {}
            item['username'] = user.user.username
            item['email'] = user.user.email
            item['phone'] = user.Telephone
            item['avatar'] = user.avatar
            item['gender'] = user.Gender
            user_list.append(item)

        # res = serializers.serialize('json', user_list, fields = ('user', 'phone', 'avatar', 'gender'))
        res = json.dumps(user_list, cls = MyJsonEncoder) 
        return HttpResponse(res,
                            content_type='application/json')

