from django.shortcuts import render
from django.views import View
from .forms import SignInForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponseNotFound
import requests
from requests.auth import HTTPBasicAuth
from api.models import UserProfile
from django.contrib.auth.models import User
from .helper import HOST, get_schedules, get_url_for_update, NAME_DAYS, schedules


class MainPage(View):
    def get(self, request):
        return render(request, 'front/mainpage.html')


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'front/signin.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                usr = requests.get(f'{HOST}/api/v1/user/{user}/', json={'user': True}).json()
                if usr['user']['last_login'] is None:
                    user_id = User.objects.get(username=user).pk
                    requests.post(f'{HOST}/api/v1/create-schedules/', json={'group': user_id},
                                  auth=HTTPBasicAuth(username, password))
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'front/signin.html', context={
            'form': form,
        })


class First(View):

    def get(self, request):
        return render(request, 'front/first.html', context={'days': NAME_DAYS})

    def post(self, request):
        data = dict(request.POST)
        day = data['day'][0]
        field = 'first_' + NAME_DAYS[day]
        requests.patch(get_url_for_update(request.user.pk), json={field: schedules(data)})
        return render(request, 'front/first.html', context={'success': day})


class Second(View):

    def get(self, request):
        return render(request, 'front/second.html', context={'days': NAME_DAYS})

    def post(self, request):
        data = dict(request.POST)
        day = data['day'][0]
        field = 'second_' + NAME_DAYS[day]
        requests.patch(get_url_for_update(request.user.pk), json={field: schedules(data)})
        return render(request, 'front/second.html', context={'success': day})


class Third(View):

    def get(self, request):
        return render(request, 'front/third.html', context={'days': NAME_DAYS})

    def post(self, request):
        data = dict(request.POST)
        day = data['day'][0]
        field = 'third_' + NAME_DAYS[day]
        requests.patch(get_url_for_update(request.user.pk), json={field: schedules(data)})
        return render(request, 'front/third.html', context={'success': day})


class Fourth(View):

    def get(self, request):
        return render(request, 'front/fourth.html', context={'days': NAME_DAYS})

    def post(self, request):
        data = dict(request.POST)
        day = data['day'][0]
        field = 'fourth_' + NAME_DAYS[day]
        requests.patch(get_url_for_update(request.user.pk), json={field: schedules(data)})
        return render(request, 'front/fourth.html', context={'success': day})

