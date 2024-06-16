from collections import Counter
from datetime import timedelta

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.db.models import Q, QuerySet
from django.utils import timezone

from apps.orders.models import Order, OrderAndDish
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
    Employee.Roles.CHEF: [
        Order.Statuses.WAITING_FOR_COOKING,
        Order.Statuses.COOKING,
        Order.Statuses.WAITING_FOR_DELIVERY,
    ],
    Employee.Roles.SOUS_CHEF: [
        Order.Statuses.WAITING_FOR_COOKING,
        Order.Statuses.COOKING,
        Order.Statuses.WAITING_FOR_DELIVERY,
    ],
}
ORDER_AND_DISH_STATUS_WEIGHTS = {
    OrderAndDish.Statuses.WAITING_FOR_COOKING: 0,
    OrderAndDish.Statuses.COOKING: 1,
    OrderAndDish.Statuses.DONE: 2,
    OrderAndDish.Statuses.DELIVERED: 3,
}
CHECKED_STATUSES = [
    OrderAndDish.Statuses.WAITING_FOR_COOKING,
    OrderAndDish.Statuses.COOKING,
    OrderAndDish.Statuses.DELIVERED,
    OrderAndDish.Statuses.DONE,
]


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
    statuses = STATUSES_BY_ROLE.get(role, [])
    return Order.objects.filter(
        Q(employee__restaurant_id=restaurant_id) &
        Q(status__in=statuses) &
        (
            Q(created__gte=left_bound) |
            Q(reservation__arrival_time__gte=left_bound)
        )
    ).order_by("status")


def update_order_list_in_layer(employee: Employee, orders: QuerySet | list[Order]) -> None:
    from apps.restaurants.consumers.room import Events, OrderService

    employee_key = f"user__{employee.user.id}__{employee.restaurant.id}"
    channel_name = cache.get(employee_key)
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
    employees = restaurant.employees.filter(role__in=STATUSES_BY_ROLE.keys()).order_by("role")
    for employee in employees:
        orders = get_orders_by_restaurant(restaurant_id, employee.role)
        update_order_list_in_layer(employee, orders)


def order_change_status(order: Order):
    order_status = Order.Statuses.WAITING_FOR_COOKING
    dishes = order.dishes.filter(status__in=CHECKED_STATUSES).all()
    count_dishes = dishes.count()
    if not count_dishes:
        return order_status
    counter = Counter(dishes.values_list("status", flat=True))
    min_status = min(counter, key=lambda obj: ORDER_AND_DISH_STATUS_WEIGHTS[obj])
    if min_status == OrderAndDish.Statuses.WAITING_FOR_COOKING:
        order_status = Order.Statuses.WAITING_FOR_COOKING
    elif min_status == OrderAndDish.Statuses.COOKING:
        order_status = Order.Statuses.COOKING
        if OrderAndDish.Statuses.DONE in counter:
            order_status = Order.Statuses.WAITING_FOR_DELIVERY
    elif min_status == OrderAndDish.Statuses.DONE:
        order_status = Order.Statuses.WAITING_FOR_DELIVERY
    elif min_status == OrderAndDish.Statuses.DELIVERED:
        order_status = Order.Statuses.DELIVERED
    return order_status


def order_change_price(order: Order):
    new_price = 0
    dishes = order.dishes.filter(~Q(status=OrderAndDish.Statuses.CANCELED))
    for dish in dishes:
        new_price += (dish.dish.price * dish.count)
    return new_price
