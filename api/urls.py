from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import *

router = SimpleRouter()
router.register('group', GroupsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('drf-auth/', include('rest_framework.urls')),
    # path('send/', ChangePasswordAPI.as_view()),  # TODO
    path('update-schedules/va312/ase4/<group>/', SchedulesApiUpdate.as_view()),
    path('create-schedules/', SchedulesAPICreate.as_view()),
    # path('user/<slug>/', UserAPIView.as_view()),  # TODO: need to rename
    # path('group/<slug>/', SchedulesAPIView.as_view()),
    path('number-week/<pk>/', NumberWeekAPI.as_view()),  # To check/update the week number
    path(r'auth/detail/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'list/group/', GroupApiView.as_view()),

]
