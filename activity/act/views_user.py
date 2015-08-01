from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from act.forms import UserForm, UserProfileForm
from act.models import UserProfile, Activity, CommentInfo, RecordInfo, MessageInfo

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
def request_user_info(request, offset):
    user = UserProfile.objects.get(user__username=offset)
    if user:
        return render(request,
                      'act/request_user_info.html',
                      {'username': user.user.username,
                       # 'avatar': user.avatar,
                       'Gender': user.Gender,
                       'Telephone': user.Telephone,
                       'Email': user.user.email,
                       #'Type': user.Type}
                       })

    else:
        return HttpResponse('not found')

# updateProfile
def update_user_info(request, offset):
    if request.method == 'POST':
        username = offset
        email = request.POST.get('email')
        password = request.POST.get('oldpassword')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                password = request.POST.get('newpassword')
                user.set_password(password)
                user.email = email
                user.save()
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('your account is disabled')
        else:
            return HttpResponse("wrong password.")
    else:
        user = UserProfile.objects.get(user__username=offset)
        return render(request, 'act/update_user_info.html',
                      {'username': offset,
                       'email': user.user.email})

# write a message
def edit_message(request):
    if request.method == 'POST':
        m = MessageInfo()
        usrname = request.POST.get('username')
        m.UID = UserProfile.objects.get(user__username=usrname).id
        m.TargetID = request.POST.get('Target')
        m.Title = request.POST.get('Title')
        m.Content =request.POST.get('Content')
        m.save()
        return HttpResponse('email has been sent!')
    else:
        return HttpResponse('New Message?')

#write a comment
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


#participate an activity
def participate_activity(request):
    if request.method == 'POST':
        r = RecordInfo()
        usrname = request.POST.get('username')
        usr = UserProfile.objects.get(user__username=usrname)
        actid = request.POST.get('activity_sid')
        act = Activity.objects.get(SID=actid)
        r.UID = usr
        r.SID = act
        r.Content = request.POST.get('register_info')
        isPublic = request.POST.get('ispublic')
        if isPublic == 'true':
            r.IsPublic = 'true'
        else:
            r.IsPublic = 'false'
        r.save()
        return HttpResponse('you have registered in the activity!')
    else:
        return HttpResponse('Participate?')