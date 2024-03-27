from django.db.models import QuerySet
from rest_framework import (
    generics,
    permissions,
    response,
    status,
)

from apps.orders.models import Reservation
from apps.restaurants.models import Restaurant
from apps.restaurants.permissions import RestaurantPermission
from apps.restaurants.serializers import (
    PlaceSerializer,
    RestaurantSerializer,
    TagToProjectSerializer,
)


class RestaurantListAPIView(generics.ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.prefetch_related("schedule").all()


class RestaurantPlacesAPIView(generics.RetrieveAPIView):
    permission_classes = (
        permissions.IsAuthenticated & RestaurantPermission,
    )

    def get_object(self):
        return self.request.user.employee.restaurant

    def filter_places(self, places, tags) -> QuerySet:
        if not tags:
            return places
        return places.filter(tags__in=tags.split(",")).order_by("id").distinct()

    def get(self, request, *args, **kwargs):
        restaurant = self.get_object()
        places = restaurant.places.all()
        tags = request.query_params.get('tags')
        places = self.filter_places(places, tags)
        free, reserved, busy = [], [], []
        free_statuses = [
            Reservation.Statuses.CANCELED,
            Reservation.Statuses.FINISHED,
        ]
        for place in places:
            reservations = place.reservations.all()

            opened = reservations.filter(status=Reservation.Statuses.OPENED)
            if opened.filter(orders__isnull=True):
                reserved.append(place)
                continue

            if opened.filter(orders__isnull=False):
                busy.append(place)
                continue

            if not reservations or reservations.filter(status__in=free_statuses):
                free.append(place)
                continue

        data = {
            "free": PlaceSerializer(free, many=True).data,
            "reserved": PlaceSerializer(reserved, many=True).data,
            "busy": PlaceSerializer(busy, many=True).data,
        }
        return response.Response(data=data, status=status.HTTP_200_OK)


class TagToPlaceAPIView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = (
        permissions.IsAuthenticated & RestaurantPermission,
    )

    def get_object(self):
        return self.request.user.employee.restaurant

    def get(self, request, *args, **kwargs):
        restaurant = self.get_object()
        restaurant_tags = set()
        for place in restaurant.places.all():
            tags = place.tags.all()
            restaurant_tags |= set(tags)

        serializer = TagToProjectSerializer(restaurant_tags, many=True)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)
