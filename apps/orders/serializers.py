from collections import OrderedDict

from django.utils import timezone
from rest_framework import serializers

from apps.restaurants.models import Restaurant
from apps.users.models import Client, Employee

from . import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = (
            "id",
            "name",
        )


class DishImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DishImages
        fields = (
            "id",
            "image",
        )


class DishImageWithDishSerializer(serializers.ModelSerializer):

    dish = serializers.PrimaryKeyRelatedField(
        queryset=models.Dish.objects.all(),
    )

    class Meta:
        model = models.DishImages
        fields = (
            "id",
            "image",
            "dish",
        )


class DishRetrieveSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    images = serializers.SerializerMethodField()

    class Meta:
        model = models.Dish
        fields = (
            "id",
            "category",
            "name",
            "description",
            "short_description",
            "price",
            "compound",
            "weight",
            "images",
        )

    def get_images(serlf, obj):
        return DishImageSerializer(obj.images.all(), many=True).data


class DishCreateSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
    )

    class Meta:
        model = models.Dish
        fields = (
            "id",
            "category",
            "name",
            "description",
            "short_description",
            "price",
            "compound",
            "weight",
        )

    @property
    def data(self) -> OrderedDict:
        return DishRetrieveSerializer(instance=self.instance).data


class OrderRetrieveSerializer(serializers.ModelSerializer):

    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        allow_null=True,
    )
    client = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        allow_null=True,
    )
    dishes = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        fields = (
            "id",
            "status",
            "price",
            "comment",
            "employee",
            "client",
            "place_number",
            "dishes",
        )

    def get_dishes(self, obj) -> list:
        return DishRetrieveSerializer(obj.dishes.all(), many=True).data


class OrderCreateSerializer(serializers.ModelSerializer):

    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        allow_null=True,
    )
    client = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        allow_null=True,
    )
    dishes = serializers.PrimaryKeyRelatedField(
        queryset=models.Dish.objects.all(),
        many=True,
    )

    class Meta:
        model = models.Order
        fields = (
            "id",
            "status",
            "price",
            "comment",
            "employee",
            "client",
            "place_number",
            "dishes",
        )

    @property
    def data(self) -> OrderedDict:
        return OrderRetrieveSerializer(instance=self.instance).data

    def validate_dishes(self, dishes):
        if dishes:
            return dishes
        raise serializers.ValidationError("Заказ не может быть без блюд")


class RestaurantAndOrderRetrieveSerializer(serializers.ModelSerializer):

    order = OrderRetrieveSerializer()
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        allow_null=True,
    )

    class Meta:
        model = models.RestaurantAndOrder
        fields = (
            "id",
            "arrival_time",
            "order",
            "restaurant",
        )


class RestaurantAndOrderCreateSerializer(serializers.ModelSerializer):

    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
    )
    order = OrderCreateSerializer(
        allow_null=True,
    )

    class Meta:
        model = models.RestaurantAndOrder
        fields = (
            "id",
            "arrival_time",
            "order",
            "restaurant",
        )

    def validate_arrival_time(self, arrival_time):
        if timezone.now() >= arrival_time:
            raise serializers.ValidationError("Время прихода не может быть раньше текущего времени")
        return arrival_time

    def create(self, validated_data) -> models.RestaurantAndOrder:
        order_dict = validated_data.pop("order")
        dishes = order_dict.pop("dishes")
        order = models.Order.objects.create(**order_dict)
        order.dishes.set(dishes)
        reservation = models.RestaurantAndOrder.objects.create(
            arrival_time=validated_data["arrival_time"],
            restaurant=validated_data["restaurant"],
            order=order,
        )
        return reservation

    @property
    def data(self) -> OrderedDict:
        return RestaurantAndOrderRetrieveSerializer(
            instance=self.instance,
        ).data
