from django_filters import rest_framework as filters


class TelegramUsersFilter(filters.FilterSet):
    is_moder = filters.BooleanFilter(
        field_name='is_moder'
    )


class EventFilter(filters.FilterSet):
    is_main = filters.BooleanFilter(
        field_name='is_main'
    )