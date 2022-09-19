from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from users.models import CustomUser, TelegramUser, GroupUserTelegram
from rest_framework import mixins
from django.db.models import Q, F
from .models import Schedule
from rest_framework import status
from .filters import TelegramUsersFilter, EventFilter
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action


class ScheduleViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

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
        for data in Schedule.objects.filter(group__username=username,
                                            week_id=from_week).all():
            Schedule.objects.update_or_create(group__username=username,
                                              week_id=to_week,
                                              number_pair=data.number_pair,
                                              day=data.day,
                                              defaults={"number_pair": data.number_pair,
                                                        "subject": data.subject,
                                                        "teacher": data.teacher,
                                                        "audience": data.audience,
                                                        "week": week,
                                                        "group": data.group,
                                                        "type_pair": data.type_pair,
                                                        "day": data.day})
        return Response(status=status.HTTP_201_CREATED)


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
        return Response(status.HTTP_204_NO_CONTENT)


class TelegramUserListOrUpdateOrCreate(
    generics.CreateAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
    generics.ListAPIView,
):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TelegramUsersFilter
    lookup_filed = 'telegram_id'


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


class ScheduleViewList(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def list(self, request, *args, **kwargs):
        group = CustomUser.objects.filter(username=self.request.query_params.get('token')).first()
        if self.request.query_params.get('day'):
            instances = self.queryset.filter(group=group.pk,
                                             week=self.request.query_params.get('week'),
                                             day=self.request.query_params.get('day'))

        elif self.request.query_params.get('week'):
            instances = self.queryset.filter(group=group.pk,
                                             week=self.request.query_params.get('week')).order_by('day')

        else:
            instances = self.queryset.filter(group=group.pk)

        if not bool(instances):
            return Response({})
        serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data)


class EventDetailOrList(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter
