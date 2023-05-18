from django.urls import include, path
from rest_framework.routers import SimpleRouter

from schedules.rest_framework import api

router = SimpleRouter()

router.register("schedule", api.ScheduleViewSet)
router.register("events", api.EventDetailOrList)
router.register("telegram/detail/user", api.TelegramUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("number-week/", api.NumberWeekAPI.as_view()),
    path(r"list/group/", api.GroupApiView.as_view()),
    path("type-pair/", api.TypeListView.as_view()),
    path(
        "get-pair/<int:week>/<str:day>/<int:number>/",
        api.ScheduleRetrieveOrDestroy.as_view(),
    ),
]
