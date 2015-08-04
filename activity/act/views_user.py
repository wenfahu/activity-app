from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from act.forms import UserForm, UserProfileForm
from act.models import UserProfile, Activity, CommentInfo, RecordInfo, MessageInfo
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

        else:
            return HttpResponse(
                json.dumps({'error': 'not found'}),
                content_type='application/json')

# updateProfile


@login_required
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
