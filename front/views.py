from django.shortcuts import render
from django.views import View
from .forms import SignInForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponseNotFound
import requests
from api.models import UserProfile
from django.contrib.auth.models import User

HOST = '0.0.0.0:8000'

NAME_DAYS = {'Понедельник': 'monday',
             'Вторник': 'tuesday',
             'Среда': 'wednesday',
             'Четверг': 'thursday',
             'Пятница': 'friday',
             'Суббота': 'saturday'}


def get_schedules(data: dict) -> tuple:
    first = [data['first_subject'][0],
             data['first_type_pair'][0],
             data['first_teacher'][0],
             data['first_aud'][0]]
    second = [data['second_subject'][0],
              data['second_type_pair'][0],
              data['second_teacher'][0],
              data['second_aud'][0]]
    third = [data['third_subject'][0],
             data['third_type_pair'][0],
             data['third_teacher'][0],
             data['third_aud'][0]]
    fourth = [data['fourth_subject'][0],
              data['fourth_type_pair'][0],
              data['fourth_teacher'][0],
              data['fourth_aud'][0]]



    return first, second, third, fourth


def schedules(data: dict) -> str:
    result = ''
    for i, value in enumerate(get_schedules(data), 1):
        if value[0].strip() == '':
            result += f'{i}) {"-" * 10}'
        else:
            result += f'{i}) {" ".join(value)}'
        result += '\n\n'
    return result


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
                usr = requests.get(f'http://{HOST}/api/v1/user/{user}/', json={'user': True}).json()
                if usr['user']['last_login'] is None:
                    user_id = User.objects.get(username=user).pk
                    requests.post(f'http://{HOST}/api/v1/create-schedules/', json={'group': user_id})
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
        requests.patch(f'http://{HOST}/api/v1/update-schedules/{request.user.pk}/', json={field: schedules(data)})

        return render(request, 'front/first.html', context={'success': day})


class Second(View):

    def get(self, request):
        return render(request, 'front/second.html', context={'days': NAME_DAYS})

    def post(self, request):
        data = dict(request.POST)
        day = data['day'][0]

        field = 'second_' + NAME_DAYS[day]

        requests.patch(f'http://{HOST}/api/v1/update-schedules/{request.user.pk}/', json={field: schedules(data)})

        return render(request, 'front/second.html', context={'success': day})


class Third(View):

    def get(self, request):
        return render(request, 'front/third.html', context={'days': NAME_DAYS})

    def post(self, request):
        data = dict(request.POST)
        day = data['day'][0]
        field = 'third_' + NAME_DAYS[day]

        requests.patch(f'http://{HOST}/api/v1/update-schedules/{request.user.pk}/', json={field: schedules(data)})

        return render(request, 'front/third.html', context={'success': day})


class Fourth(View):

    def get(self, request):
        return render(request, 'front/fourth.html', context={'days': NAME_DAYS})

    def post(self, request):
        data = dict(request.POST)
        day = data['day'][0]

        field = 'fourth_' + NAME_DAYS[day]

        requests.patch(f'http://{HOST}/api/v1/update-schedules/{request.user.pk}/', json={field: schedules(data)})

        return render(request, 'front/fourth.html', context={'success': day})

