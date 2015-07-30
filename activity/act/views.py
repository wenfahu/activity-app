from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from activity.act.forms import UserForm, UserProfileForm
from activity.act.models import UserProfile, Activity, CommentInfo

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
            print ("Invalid login details: {0}, {1}".format(username, password)) 
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'act/login.html', {})


# requestInfo
def request_user_info(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = UserProfile.objects.get(user__username = username)
        if user:
            print(user)

        else:
            return HttpResponse('not found')
    else:
        return HttpResponse('search page')

