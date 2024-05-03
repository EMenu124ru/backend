from datetime import timedelta

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.db.models import Q, QuerySet
from django.utils import timezone

from apps.orders.models import Order
from apps.restaurants.models import Restaurant
from apps.users.models import Employee

STATUSES_BY_ROLE = {
    Employee.Roles.WAITER: [
        Order.Statuses.WAITING_FOR_COOKING,
        Order.Statuses.COOKING,
        Order.Statuses.WAITING_FOR_DELIVERY,
        Order.Statuses.IN_PROCESS_DELIVERY,
        Order.Statuses.DELIVERED,
        Order.Statuses.PAID,
    ],
    Employee.Roles.MANAGER: [
        Order.Statuses.DELAYED,
        Order.Statuses.WAITING_FOR_COOKING,
        Order.Statuses.COOKING,
        Order.Statuses.WAITING_FOR_DELIVERY,
        Order.Statuses.IN_PROCESS_DELIVERY,
        Order.Statuses.DELIVERED,
        Order.Statuses.PAID,
        Order.Statuses.FINISHED,
        Order.Statuses.CANCELED,
    ],
    Employee.Roles.COOK: [
        Order.Statuses.WAITING_FOR_COOKING,
        Order.Statuses.COOKING,
    ],
    Employee.Roles.CHEF: [
        Order.Statuses.WAITING_FOR_COOKING,
        Order.Statuses.COOKING,
    ],
    Employee.Roles.SOUS_CHEF: [
        Order.Statuses.WAITING_FOR_COOKING,
        Order.Statuses.COOKING,
    ],
    Employee.Roles.HOSTESS: [],
}


def get_restaurant_id(order: Order):
    employee = order.employee
    if employee and employee.restaurant_id:
        return employee.restaurant_id

    reservation = order.reservation
    if reservation and reservation.restaurant_id:
        return reservation.restaurant_id


def get_orders_by_restaurant(restaurant_id: int, role: Employee.Roles) -> QuerySet:
    delta = timedelta(hours=14)
    now = timezone.now()
    left_bound = now - delta
    return Order.objects.filter(
        Q(employee__restaurant_id=restaurant_id) &
        Q(status__in=STATUSES_BY_ROLE[role]) &
        (
            Q(created__gte=left_bound) |
            Q(reservation__arrival_time__gte=left_bound)
        )
    ).order_by("status")


def update_order_list_in_layer(employee: Employee, orders: QuerySet | list[Order]) -> None:
    from apps.restaurants.consumers.room import Events, OrderService

    channel_name = cache.get(f"user__{employee.user.id}")
    if channel_name:
        body = {"orders": OrderService.get_orders_list_sync(orders)}
        async_to_sync(get_channel_layer().send)(
            channel_name,
            {
                "type": Events.LIST_ORDERS,
                "body": body,
            },
        )


def update_order_list_in_group(restaurant_id: int) -> None:
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    for employee in restaurant.employees.all():
        orders = get_orders_by_restaurant(restaurant_id, employee.role)
        update_order_list_in_layer(employee, orders)
