from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.rest_framework.api import UserViewSet

from api.rest_framework.api import *

router = SimpleRouter()

router.register("schedule", ScheduleViewSet)
router.register("events", EventDetailOrList)
router.register("telegram/detail/user", TelegramUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("number-week/", NumberWeekAPI.as_view()),
    path(r"list/group/", GroupApiView.as_view()),
    path("type-pair/", TypeListView.as_view()),
    path(
        "get-pair/<int:week>/<str:day>/<int:number>/",
        ScheduleRetrieveOrDestroy.as_view(),
    ),
]
