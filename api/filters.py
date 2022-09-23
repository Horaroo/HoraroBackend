from django_filters import rest_framework as filters
from django.http import Http404
from users.models import CustomUser
from django.shortcuts import get_object_or_404


class TelegramUsersFilter(filters.FilterSet):
    is_moder = filters.BooleanFilter(
        field_name='is_moder'
    )


class EventFilter(filters.FilterSet):
    is_main = filters.BooleanFilter(
        field_name='is_main'
    )


class GetScheduleFilter(filters.FilterSet):
    day = filters.CharFilter(field_name='day', method='get_day')
    week = filters.CharFilter(field_name='week', method='get_week')

    def get_day(self, queryset, name, value):
        token = get_object_or_404(CustomUser, username=self.request.GET.get('token'))
        instances = queryset.filter(group=token.pk,
                                    week=self.request.GET.get('week'),
                                    day=value)
        if instances:
            return instances
        raise Http404

    def get_week(self, queryset, name, value):
        token = get_object_or_404(CustomUser, username=self.request.GET.get('token'))
        instances = queryset.filter(group=token.pk,
                                    week=value).order_by('day')
        if instances:
            return instances
        raise Http404
