from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings


urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('first-week', First.as_view(), name='first_week'),
    path('second-week', Second.as_view(), name='second_week'),
    path('third-week', Third.as_view(), name='third_week'),
    path('fourth-week', Fourth.as_view(), name='fourth_week'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout'),
]
