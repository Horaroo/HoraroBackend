from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from users.models import CustomUser, TelegramUser, GroupUserTelegram
from rest_framework import mixins
from django.db.models import Q
from .models import Schedule
from rest_framework import status


class ScheduleViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )


class NumberWeekAPI(generics.RetrieveUpdateAPIView):
    queryset = NumberWeek.objects.all()
    serializer_class = NumberWeekSerializer
    permission_classes = (permissions.IsAdminUser, )


class GroupApiView(APIView):
    def get(self, request):
        q = CustomUser.objects.filter(~Q(username='root')).values('username', 'group')
        return Response(q)


class TypeListView(generics.ListAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class GetScheduleView(generics.RetrieveAPIView):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def retrieve(self, request, *args, **kwargs):
        group = CustomUser.objects.filter(group=self.request.query_params.get('group')).first()
        instance = self.queryset.filter(group=group.pk,
                                        week=kwargs.get('week'),
                                        day=kwargs.get('day'),
                                        number_pair=kwargs.get('number')).first()

        if not bool(instance):
            return Response({})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TelegramUserCreate(generics.CreateAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer


class GroupUserCreateOrDelete(generics.CreateAPIView,
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
