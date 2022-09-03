from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register('group', GroupsViewSet)
router.register('schedule', ScheduleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('drf-auth/', include('rest_framework.urls')),
    path('number-week/<pk>/', NumberWeekAPI.as_view()),  # To check/update the week number
    path(r'auth/detail/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'list/group/', GroupApiView.as_view()),
    path('type-pair/', TypeListView.as_view()),
    path('get-pair/<int:week>/<int:day>/<int:number>/', GetScheduleView.as_view())

]
