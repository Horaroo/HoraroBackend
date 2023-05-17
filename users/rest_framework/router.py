from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.rest_framework.api import UserViewSet

router = SimpleRouter()

router.register("auth/detail", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("drf-auth/", include("rest_framework.urls")),
    path(r"auth/", include("djoser.urls.authtoken")),
]
