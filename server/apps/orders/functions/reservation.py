from apps.orders.models import Order, Reservation

MAPPER_ORDER_STATUSES = {
    Order.Statuses.DELAYED: 0,
    Order.Statuses.WAITING_FOR_COOKING: 1,
    Order.Statuses.COOKING: 2,
    Order.Statuses.WAITING_FOR_DELIVERY: 3,
    Order.Statuses.IN_PROCESS_DELIVERY: 4,
    Order.Statuses.DELIVERED: 5,
    Order.Statuses.PAID: 6,
    Order.Statuses.FINISHED: 7,
    Order.Statuses.CANCELED: 8,
}

MAPPER_RESERVATION_STATUS = {
    0: Reservation.Statuses.OPENED,
    1: Reservation.Statuses.OPENED,
    2: Reservation.Statuses.OPENED,
    3: Reservation.Statuses.OPENED,
    4: Reservation.Statuses.OPENED,
    5: Reservation.Statuses.OPENED,
    6: Reservation.Statuses.OPENED,
    7: Reservation.Statuses.FINISHED,
    8: Reservation.Statuses.CANCELED,
}


def change_reservation_status(reservation: Reservation):
    if not reservation:
        return

    orders_statuses = reservation.orders.values_list("status", flat=True).distinct()
    if not orders_statuses:
        return

    statuses = min(orders_statuses, key=lambda x: MAPPER_ORDER_STATUSES[x])
    reservation_status = MAPPER_RESERVATION_STATUS[MAPPER_ORDER_STATUSES[statuses]]
    reservation.status = reservation_status
    reservation.save()
