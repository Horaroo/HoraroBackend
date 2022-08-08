from rest_framework import generics, filters, viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import *
from .models import UserProfile
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK


class RegisterView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        UserProfile(user=user, telegram_id=request.data['telegram_id'], group=request.data['group']).save()
        return HttpResponse(status=HTTP_201_CREATED)


# update schedules
class SchedulesApiUpdate(generics.UpdateAPIView):
    queryset = Schedules.objects.all()
    serializer_class = SchedulesSerializer
    lookup_field = 'group'
    permission_classes = (permissions.IsAuthenticated, )


# create field in the table
class SchedulesAPICreate(generics.CreateAPIView):
    queryset = Schedules.objects.all()
    serializer_class = SchedulesSerializer
    permission_classes = (permissions.IsAuthenticated, )


# To check when creating for the presence of a user with this name
class UserAPIView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, slug):

        if request.data.get('telegram_id', False):
            get_object_or_404(UserProfile.objects.filter(telegram_id=slug).values())
            return HttpResponse(status=HTTP_200_OK)

        elif request.data.get('user', False):
            res = get_object_or_404(User.objects.filter(username=slug).values())
            return Response({'user': res})

        get_object_or_404(UserProfile.objects.filter(group=slug).values())
        return HttpResponse(status=HTTP_200_OK)


class UserChangeAPIView(APIView):
    permission_classes = (permissions.IsAdminUser, )

    def post(self, request, slug):
        user = User.objects.get(pk=UserProfile.objects.get(telegram_id=slug).user_id).username
        group = UserProfile.objects.get(telegram_id=slug).group
        u = User.objects.get(username=user)
        u.set_password(request.data['passwd'])
        u.save()
        return Response({'login': user, 'group': group})


class GroupsAPIView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        return Response({'groups': UserProfile.objects.values('group')})


# To view schedules
class SchedulesAPIView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, slug):
        user = get_object_or_404(UserProfile.objects.filter(group=slug))
        if request.data.get('field', False):
            return Response({'group': Schedules.objects.filter(group=user.user_id).values(request.data.get('field'))})

        elif request.data.get('schedule', False):
            return Response({'schedule': Schedules.objects.filter(group=user.user_id).values(*request.data['fields'])})

        res = Schedules.objects.filter(group=user.user_id).values()
        return Response({'group': res})


class NumberWeekAPI(generics.RetrieveUpdateAPIView):
    queryset = NumberWeek.objects.all()
    serializer_class = NumberWeekSerializer
    permission_classes = (permissions.IsAdminUser, )


class BlockUserAPI(APIView):
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request):
        return Response({'block': BlockUser.objects.all().values()})

    def post(self, request):
        try:
            group = UserProfile.objects.get(group=request.data['username'])
            if not group:
                raise User.DoesNotExist

            user = User.objects.get(pk=group.user.pk)
            BlockUser.objects.create(telegram_id=user.userprofile.telegram_id,
                                     username=user.username)
            user.delete()

            return Response({'message': 'Пользователь успешно забокирован!'})

        except User.DoesNotExist:
            return Response({'message': 'Пользователь не существует!'})

    def delete(self, request):
        username = request.data.get('username')
        try:
            BlockUser.objects.get(username=username).delete()
            return Response({'message': f'"{username}" успешно разблокирован!'})

        except BlockUser.DoesNotExist:
            return Response({'message': f'Пользователь с именем "{username}" не заблокирован!'})
