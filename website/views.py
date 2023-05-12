from django.shortcuts import render
from django.views import View


class DashboardView(View):

    def get(self, request, *args, **kwargs):  # noqa
        return render(request, "website/index.html")
