from collections import OrderedDict

from rest_framework import serializers

from apps.users.models import Client, Employee

from . import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = (
            "id",
            "name",
        )


class DishRetrieveSerializer(serializers.ModelSerializer):

    category = CategorySerializer()

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


class DishImageSerializer(serializers.ModelSerializer):

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
            "place_number"
            "dishes",
        )
