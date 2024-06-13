import zoneinfo
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import (
    generics,
    permissions,
    response,
    status,
)

from apps.restaurants.models import Restaurant, TagToPlace
from apps.restaurants.permissions import RestaurantPermission
from apps.restaurants.serializers import (
    PlaceSerializer,
    RestaurantSerializer,
    TagToPlaceSerializer,
)
from apps.users.permissions import IsClient


class RestaurantListAPIView(generics.ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.order_by("id").prefetch_related("schedule").all()


class RestaurantPlacesAPIView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = (
        permissions.IsAuthenticated & (IsClient | RestaurantPermission),
    )

    def get_object(self):
        if self.request.user.is_client:
            restaurant_id = self.request.query_params.get('restaurant_id')
            return get_object_or_404(Restaurant, pk=restaurant_id)
        return self.request.user.employee.restaurant

    def get(self, request, *args, **kwargs):
        restaurant = self.get_object()
        tags = request.query_params.get('tags')
        got_time = request.query_params.get('time')

        current_time = timezone.localtime(
            timezone.now(),
            timezone=zoneinfo.ZoneInfo(restaurant.time_zone),
        ).replace(tzinfo=None)
        if got_time:
            got_time = datetime.fromisoformat(got_time)
            if got_time < current_time:
                return response.Response(
                    data={"message": "Переданное время не может быть раньше текущего"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            current_time = got_time

        free, reserved, busy = restaurant.get_places(tags, current_time=current_time)
        data = {
            "free": PlaceSerializer(free, many=True).data,
            "reserved": PlaceSerializer(reserved, many=True).data,
            "busy": PlaceSerializer(busy, many=True).data,
        }
        return response.Response(data=data, status=status.HTTP_200_OK)


class TagToPlaceAPIView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = (
        permissions.IsAuthenticated & (IsClient | RestaurantPermission),
    )

    def get_object(self):
        if self.request.user.is_client:
            restaurant_id = self.request.query_params.get('restaurant_id')
            return get_object_or_404(Restaurant, pk=restaurant_id)
        return self.request.user.employee.restaurant

    def get(self, request, *args, **kwargs):
        restaurant = self.get_object()
        location, number_of_seats = [], []
        for place in restaurant.places.prefetch_related("tags").all():
            tags = place.tags.all()
            location.extend(tags.filter(type=TagToPlace.Types.LOCATION))
            number_of_seats.extend(tags.filter(type=TagToPlace.Types.NUMBER_OF_SEATS))

        restaurant_tags = {
            "location": TagToPlaceSerializer(set(location), many=True).data,
            "number_of_seats": TagToPlaceSerializer(set(number_of_seats), many=True).data,
        }
        return response.Response(data=restaurant_tags, status=status.HTTP_200_OK)
