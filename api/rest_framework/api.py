from django.db.models import Q
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from api.time.time_services import TimeServices

from api.rest_framework import serializers
from api import models, services
from api.rest_framework import filters
from users import models as user_models


class ScheduleViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = models.Schedule.objects.all().select_related("group")
    serializer_class = serializers.ScheduleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    filterset_class = filters.GetScheduleFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.ScheduleCreatorOrUpdater(serializer.validated_data, serializer=serializer).execute()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"where-are-pairs",
        filterset_class=filters.WhereArePairsFilter,
    )
    def where_are_pairs(self, request):
        token = request.GET.get("token")
        if token is None:
            return Response(
                {"status": "need token"}, status=status.HTTP_400_BAD_REQUEST
            )
        h, m = request.GET.get("h"), request.GET.get("m")
        current_pair = services.CurrentPairGetter(token=token, h=h, m=m).execute()
        return Response(current_pair)

    @action(detail=False, methods=["get"], url_path=r"detail/(?P<username>\w+)")
    def get_info(self, request, username):
        query = request.GET.get("q")
        result = services.AutofillGetter(
            token=username, query=query, field=request.GET
        ).execute()
        return Response({"results": result})

    @action(
        detail=False,
        methods=["post"],
        url_path=r"copy",
        serializer_class=serializers.ScheduleCopySerializer,
        permission_classes=[permissions.IsAuthenticated],
    )
    def copy_schedule(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.Copywriter(
            queryset=self.queryset,
            user=request.user,
            source_week=serializer.data["source_week"],
            target_week=serializer.data["target_week"],
            source_day=serializer.data["source_day"],
            target_day=serializer.data["target_day"],
            source_pair=serializer.data["source_pair"],
            target_pair=serializer.data["target_pair"],
        ).execute()

        return Response(status=status.HTTP_201_CREATED)

    @action(methods=["get"], detail=False, serializer_class=serializers.OneFieldSerializer)
    def get_one_field(self, request):
        username = self.request.GET.get("token")
        instances = (
            self.queryset.filter(group__username=username)
            .distinct()
            .values(request.GET.get("select_field"))
        )
        serializer = serializers.OneFieldSerializer(data=instances, many=True)
        serializer.is_valid(raise_exception=False)
        return Response({"data": serializer.data})

    @swagger_auto_schema(
        method="GET",
        manual_parameters=[
            openapi.Parameter("token", openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter("week", openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
    )
    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        filterset_class=[],
    )
    def get_schedule_week(self, request):
        week = str(int(self.request.query_params.get("week")) - 1)
        token = self.request.query_params.get("token")
        data = services.ScheduleWeekGetter(token=token, week=week).execute()
        return Response(data)


class NumberWeekAPI(APIView):
    _time_service = TimeServices()

    def get(self, request):
        return Response({"Number": self._time_service.get_week_number()})


class GroupApiView(APIView):
    def get(self, request):  # noqa
        q = user_models.CustomUser.objects.filter(~Q(username="root")).values(
            "username", "group", "verified"
        )
        return Response(q)


class TypeListView(generics.ListAPIView):
    queryset = models.Type.objects.all()
    serializer_class = serializers.TypeSerializer


class ScheduleRetrieveOrDestroy(generics.GenericAPIView):
    serializer_class = serializers.ScheduleSerializer
    queryset = models.Schedule.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_instance(self, request, *args, **kwargs):
        group = user_models.CustomUser.objects.filter(
            username=self.request.query_params.get("token")
        ).first()
        instance = self.queryset.filter(
            group_id=group.pk,
            week__name=kwargs.get("week"),
            day__name__exact=kwargs.get("day"),
            number_pair=kwargs.get("number"),
        ).first()
        return instance

    def get(self, request, *args, **kwargs):
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


class TelegramUserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = user_models.TelegramUser.objects.all()
    serializer_class = serializers.TelegramUserSerializer
    filterset_class = filters.TelegramUsersFilter
    lookup_field = "telegram_id"
    lookup_url_kwarg = "telegram_id"

    def create(self, request, *args, **kwargs):
        if self.queryset.filter(telegram_id=request.POST.get("telegram_id")):
            return Response({"Message": "Already created"}, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)


class EventDetailOrList(viewsets.ReadOnlyModelViewSet):
    queryset = models.Event.objects.all().order_by("-id")
    serializer_class = serializers.EventSerializer
    filterset_class = filters.EventFilter
