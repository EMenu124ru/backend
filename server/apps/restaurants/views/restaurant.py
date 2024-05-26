from rest_framework import (
    generics,
    permissions,
    response,
    status,
)

from apps.restaurants.models import Restaurant
from apps.restaurants.permissions import RestaurantPermission
from apps.restaurants.serializers import (
    PlaceSerializer,
    RestaurantSerializer,
    TagToPlaceSerializer,
)


class RestaurantListAPIView(generics.ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.order_by("id").prefetch_related("schedule").all()


class RestaurantPlacesAPIView(generics.RetrieveAPIView):
    permission_classes = (
        permissions.IsAuthenticated & RestaurantPermission,
    )

    def get_object(self):
        return self.request.user.employee.restaurant

    def get(self, request, *args, **kwargs):
        restaurant = self.get_object()
        tags = request.query_params.get('tags')
        free, reserved, busy = restaurant.get_places(tags)
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

        serializer = TagToPlaceSerializer(restaurant_tags, many=True)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)
