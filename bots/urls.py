from django.urls import path

from bots import views

urlpatterns = [
    path("telegram", views.BotAPIView.as_view()),
]
