from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.restaurants.models import Restaurant
from apps.restaurants.serializers import RestaurantSerializer


class RestaurantRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.prefetch_related(
            "plans",
            "schedules",
        ).filter(pk=self.kwargs["pk"])


class RestaurantListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.prefetch_related(
            "plans",
            "schedules",
        ).all()
