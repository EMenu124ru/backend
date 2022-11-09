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


class DishSerializer(serializers.ModelSerializer):

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        new_info = {
            "images": DishImageSerializer(instance.images.all(), many=True).data,
            "category": CategorySerializer(instance=instance.category).data,
        }
        data.update(new_info)
        return data


class OrderSerializer(serializers.ModelSerializer):

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

    def validate_dishes(self, dishes) -> list:
        if not dishes:
            raise serializers.ValidationError("Заказ не может быть без блюд")
        return dishes

    def to_representation(self, instance):
        data = super().to_representation(instance)
        new_info = {
            "dishes": DishSerializer(instance.dishes.all(), many=True).data,
        }
        data.update(new_info)
        return data


class RestaurantAndOrderSerializer(serializers.ModelSerializer):

    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
    )
    order = OrderSerializer(
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

    def create(self, validated_data) -> models.RestaurantAndOrder:
        order_dict = validated_data.pop("order")
        dishes = order_dict.pop("dishes")
        order = models.Order.objects.create(**order_dict)
        order.dishes.set(dishes)
        restaurantAndOrders = models.RestaurantAndOrder.objects.create(
            arrival_time=validated_data["arrival_time"],
            restaurant=validated_data["restaurant"],
            order=order,
        )
        return restaurantAndOrders
