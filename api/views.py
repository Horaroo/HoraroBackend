from django.db.models.functions import Concat
from django.forms import CharField
from django.http import QueryDict
from rest_framework import generics, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from users.models import TelegramUser, GroupUserTelegram
from rest_framework import mixins
from django.db.models import Q
from django.db.models import F, Value, Func
from .models import Schedule
from rest_framework import status
from .filters import *
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from api.time.time_services import TimeServices
from api.time.configs.dataclasses import Time
from api.helpers import copy_week
from .time.configs.constants import WEEK_DAYS_RU
from django.db.models.functions import Concat


class ScheduleViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = GetScheduleFilter
    _time_services = TimeServices()

    @action(detail=False,
            methods=['get'],
            url_path=r'where-are-pairs',
            filterset_class=WhereArePairsFilter)
    def where_are_pairs(self, request):
        token = request.GET.get('token')

        if token is None:
            return Response({'status': 'need token'}, status=status.HTTP_400_BAD_REQUEST)

        h, m = request.GET.get('h'), request.GET.get('m')

        if h is not None and m is not None:
            time = Time(hour=int(h), minute=int(m))
        else:
            time = None

        group = get_object_or_404(CustomUser, username=token)
        week_day = self._time_services.get_week_day().name
        week_number = str(self._time_services.get_week_number())

        qs = super().get_queryset().filter(
            group=group,
            week__name__startswith=week_number,
            day__name__icontains=week_day,
        ).order_by('number_pair')

        current_pair = self._time_services.get_current_pair(qs, time=time)
        return Response(current_pair.to_dict())

    @action(detail=False,
            methods=['get'],
            url_path=r'detail/(?P<username>\w+)')
    def get_info(self, request, username):
        group = CustomUser.objects.get(username=username)
        query = request.GET.get('q')
        if request.GET.get('teacher'):
            resp = self.queryset.filter(teacher__istartswith=query, group=group).values(name=F('teacher'))
        elif request.GET.get('subject'):
            resp = self.queryset.filter(subject__istartswith=query, group=group).values(name=F('subject'))
        else:
            resp = self.queryset.filter(audience__istartswith=query, group=group).values(name=F('audience'))
        return Response({'results': resp.distinct()})

    @action(detail=False,
            methods=['post'],
            url_path=r'copy-week',
            serializer_class=ScheduleCopySerializer,
            permission_classes=[permissions.AllowAny])
    def copy_schedule(self, request):
        serializer = ScheduleCopySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']
        from_week = serializer.data['from_week']
        to_week = serializer.data['to_week']
        week = Week.objects.get(pk=to_week)
        instances = self.queryset.filter(group__username=username, week_id=to_week)
        if instances:
            instances.delete()
        copy_week(self.queryset, username, from_week, week)

        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['get'],
            detail=False,
            serializer_class=OneFieldSerializer)
    def get_one_field(self, request):
        user = get_object_or_404(CustomUser, username=self.request.GET.get('token'))
        instances = self.queryset.filter(group=user.pk).distinct().values(
            request.GET.get('select_field'))
        serializer = OneFieldSerializer(data=instances, many=True)
        serializer.is_valid(raise_exception=False)
        return Response({'data': serializer.data})


class NumberWeekAPI(generics.RetrieveUpdateAPIView):
    queryset = NumberWeek.objects.all()
    serializer_class = NumberWeekSerializer
    permission_classes = (permissions.IsAdminUser,)


class GroupApiView(APIView):
    def get(self, request):
        q = CustomUser.objects.filter(~Q(username='root')).values('username', 'group', 'verified')
        return Response(q)


class TypeListView(generics.ListAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class ScheduleRetrieveOrDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_instance(self, request, *args, **kwargs):
        group = CustomUser.objects.filter(username=self.request.query_params.get('token')).first()
        instance = self.queryset.filter(group=group.pk,
                                        week=kwargs.get('week'),
                                        day=kwargs.get('day'),
                                        number_pair=kwargs.get('number')).first()
        return instance

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_instance(request, *args, **kwargs)
        if not bool(instance):
            return Response({})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_instance(request, *args, **kwargs)
        if not bool(instance):
            return Response({})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TelegramUsersFilter
    _time_services = TimeServices()
    lookup_field = 'telegram_id'
    lookup_url_kwarg = 'telegram_id'

    def _get_week_data(self, action):
        week_day_num = self._time_services.get_week_day().num
        week_number = str(self._time_services.get_week_number())
        if action == 'PTW':
            week_day_num = (self._time_services.get_week_day().num + 1) % 7
            if week_day_num == 0:
                week_number = str((self._time_services.get_week_number() + 1) % 4)

        return WEEK_DAYS_RU[week_day_num], week_number

    @action(
        methods=['GET'],
        detail=False
    )
    def notifications(self, request):
        """query param - h (current hour)"""
        hour = request.GET.get('h')
        if hour is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        qs_users = self.queryset.filter(
            notification_time=hour,
        )

        result = []
        for user in qs_users:
            week_day, week_number = self._get_week_data(user.action)
            temp = {
                'telegram_id': user.telegram_id,
                'data': Schedule.objects.filter(
                    group=user.token.pk,
                    week__name__startswith=week_number,
                    day__name__icontains=week_day,
                )
            }
            result.append(temp)

        serializer = NotificationSerializer(data=result, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)


class GroupUserCreateOrDeleteOrList(generics.CreateAPIView,
                                    generics.DestroyAPIView,
                                    generics.ListAPIView):
    queryset = GroupUserTelegram.objects.all()
    serializer_class = GroupUserTelegramSerializer

    def destroy(self, request, *args, **kwargs):
        telegram_id = self.request.query_params.get('telegram_id')
        token = self.request.query_params.get('token')
        try:
            self.queryset.get(user__telegram_id=telegram_id, token=token).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GroupUserTelegram.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        telegram_id = self.request.query_params.get('telegram_id')
        return self.queryset.filter(user__telegram_id=telegram_id).values()


class EventDetailOrList(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter
