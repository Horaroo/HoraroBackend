from rest_framework import generics, filters, viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from .helpers import send_message_to_mail
from django.http import Http404
from rest_framework.authentication import TokenAuthentication


class RegisterView(generics.GenericAPIView):
    pass

#     permission_classes = (permissions.AllowAny, )
#     serializer_class = RegisterSerializer
#
#     def post(self, request, *args,  **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         UserProfile(user=user, telegram_id=request.data['telegram_id'], group=request.data['group']).save()
#         return HttpResponse(status=HTTP_201_CREATED)


# update schedules
class SchedulesApiUpdate(generics.UpdateAPIView):
    queryset = Schedules.objects.all()
    serializer_class = SchedulesSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    lookup_field = 'group'


# create field in the table
class SchedulesAPICreate(generics.CreateAPIView):
    queryset = Schedules.objects.all()
    serializer_class = SchedulesSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChangePasswordAPI(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        to_email = request.data.get('email')
        # try:
        #     to_email = CustomUser.objects.get(email=request_email)
        # except CustomUser.DoesNotExist:
        #     raise Http404("Email не найден")

        send_message_to_mail(to_email=to_email)
        return Response({"message": f"Инструкция для сброса пароля отправлена на {to_email}"})


# To check when creating for the presence of a user with this name
class UserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        return Response({'response': 'success'})
#     permission_classes = (permissions.AllowAny, )
#
#     def get(self, request, slug):
#
#         if request.data.get('telegram_id', False):
#             get_object_or_404(UserProfile.objects.filter(telegram_id=slug).values())
#             return HttpResponse(status=HTTP_200_OK)
#
#         elif request.data.get('user', False):
#             res = get_object_or_404(User.objects.filter(username=slug).values())
#             return Response({'user': res})
#
#         get_object_or_404(UserProfile.objects.filter(group=slug).values())
#         return HttpResponse(status=HTTP_200_OK)
#
#
class UserChangeAPIView(APIView):
    pass

#     permission_classes = (permissions.IsAdminUser, )
#
#     def post(self, request, slug):
#         user = User.objects.get(pk=UserProfile.objects.get(telegram_id=slug).user_id).username
#         group = UserProfile.objects.get(telegram_id=slug).group
#         u = User.objects.get(username=user)
#         u.set_password(request.data['passwd'])
#         u.save()
#         return Response({'login': user, 'group': group})
#
#
class GroupsAPIView(APIView):
    pass

#     permission_classes = (permissions.AllowAny, )
#
#     def get(self, request):
#         return Response({'groups': UserProfile.objects.values('group')})
#
#
# # To view schedules
class SchedulesAPIView(APIView):
    pass
#     permission_classes = (permissions.AllowAny, )
#
#     def get(self, request, slug):
#         user = get_object_or_404(UserProfile.objects.filter(group=slug))
#         if request.data.get('field', False):
#             return Response({'group': Schedules.objects.filter(group=user.user_id).values(request.data.get('field'))})
#
#         elif request.data.get('schedule', False):
#             return Response({'schedule': Schedules.objects.filter(group=user.user_id).values(*request.data['fields'])})
#
#         res = Schedules.objects.filter(group=user.user_id).values()
#         return Response({'group': res})


class NumberWeekAPI(generics.RetrieveUpdateAPIView):
    queryset = NumberWeek.objects.all()
    serializer_class = NumberWeekSerializer
    permission_classes = (permissions.IsAdminUser, )


class BlockUserAPI(APIView):
    pass

#     permission_classes = (permissions.IsAdminUser, )
#
#     def get(self, request):
#         return Response({'block': BlockUser.objects.all().values()})
#
#     def post(self, request):
#         try:
#             group = UserProfile.objects.get(group=request.data['username'])
#             if not group:
#                 raise User.DoesNotExist
#
#             user = User.objects.get(pk=group.user.pk)
#             BlockUser.objects.create(telegram_id=user.userprofile.telegram_id,
#                                      username=user.username)
#             user.delete()
#
#             return Response({'message': 'Пользователь успешно забокирован!'})
#
#         except User.DoesNotExist:
#             return Response({'message': 'Пользователь не существует!'})
#
#     def delete(self, request):
#         username = request.data.get('username')
#         try:
#             BlockUser.objects.get(username=username).delete()
#             return Response({'message': f'"{username}" успешно разблокирован!'})
#
#         except BlockUser.DoesNotExist:
#             return Response({'message': f'Пользователь с именем "{username}" не заблокирован!'})
