from rest_framework import generics, filters, viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from users.models import Group, CustomUser
from rest_framework import mixins
from django.db.models import Q
from .models import Schedule


# update schedules
# class SchedulesApiUpdate(generics.UpdateAPIView):
#     queryset = Schedules.objects.all()
#     serializer_class = SchedulesSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#     authentication_classes = (TokenAuthentication, )
#     lookup_field = 'group'
#
#
# class SchedulesAPICreate(generics.CreateAPIView):
#     queryset = Schedules.objects.all()
#     serializer_class = SchedulesSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#

class GroupsViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    queryset = Group.objects.all()
    permission_classes = (permissions.AllowAny, )
    # pagination_class = LimitOffsetPagination
    serializer_class = GroupSerializer

    def get_queryset(self):
        if self.request.query_params.get('q'):
            queryset = self.queryset.filter(name__startswith=self.request.query_params.get('q').upper())
            return queryset[:5] if queryset else None
        else:
            return self.queryset.filter(~Q(name='root'))[:5]


class ScheduleViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class NumberWeekAPI(generics.RetrieveUpdateAPIView):
    queryset = NumberWeek.objects.all()
    serializer_class = NumberWeekSerializer
    permission_classes = (permissions.IsAdminUser, )


class GroupApiView(APIView):
    def get(self, request):
        q = CustomUser.objects.filter(~Q(name='root')).values('group__name', 'group__faculty__name')
        return Response(q)
