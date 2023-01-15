from django.urls import path

from bots import views

# Path should be as below:
# webhook/pubdict/telergam-bot/<language name>

urlpatterns = [
    path("telegram", views.HoraroAPIView.as_view()),
]
