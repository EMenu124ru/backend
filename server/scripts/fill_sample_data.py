from random import randint, shuffle

from apps.orders.factories import (
    CategoryFactory,
    DishFactory,
    DishImageFactory,
    OrderAndDishFactory,
    OrderFactory,
    ReservationFactory,
    StopListFactory,
)
from apps.restaurants.factories import (
    RestaurantFactory,
    ScheduleFactory as RestaurantScheduleFactory,
)
from apps.users.factories import (
    UserFactory,
    ClientFactory,
    EmployeeFactory,
    ScheduleFactory as EmployeeScheduleFactory,
)

USERS_COUNT = 20
CLIENTS_COUNT = EMPLOYEES_COUNT = 10
EMPLOYEE_SCHEDULE_COUNT = 5
CATEGORIES_COUNT = 5
ORDERS_COUNT = 10
DISH_REVIEWS_COUNT = 10
DISH_IN_CATEGORY_COUNT = 3
IMAGES_PER_DISH_COUNT = 3
RESTAURANTS_COUNT = 3
SCHEDULES_COUNT = 7


def run():
    """Generate examples."""
    users = UserFactory.create_batch(
        size=USERS_COUNT,
    )
    clients = [
        ClientFactory.create(user=user)
        for user in users[:len(users) // 2]
    ]
    restaurants = []
    for _ in range(RESTAURANTS_COUNT):
        restaurants.append(RestaurantFactory.create())
    for restaurant in restaurants:
        for _ in range(SCHEDULES_COUNT):
            RestaurantScheduleFactory.create(restaurant=restaurant)
    employees = []
    for i in range(EMPLOYEES_COUNT, USERS_COUNT):
        restaurant = restaurants[randint(0, RESTAURANTS_COUNT - 1)]
        employee = EmployeeFactory.create(user=users[i], restaurant=restaurant)
        employees.append(employee)
        EmployeeScheduleFactory.create_batch(
            size=EMPLOYEE_SCHEDULE_COUNT,
            employee=employee,
        )
    categories = CategoryFactory.create_batch(
        size=CATEGORIES_COUNT,
    )
    dishes = []
    for i in range(CATEGORIES_COUNT):
        dishes.extend(DishFactory.create_batch(
            size=DISH_IN_CATEGORY_COUNT,
            category=categories[i],
        ))
    ingredients = []
    for dish in dishes:
        ingredients.extend(dish.ingredients.all())
        DishImageFactory.create_batch(
            dish=dish,
            size=IMAGES_PER_DISH_COUNT,
        )
    orders = []
    for i in range(ORDERS_COUNT):
        reservation = None
        if randint(0, 1):
            restaurant = restaurants[randint(0, RESTAURANTS_COUNT - 1)]
            reservation = ReservationFactory.create(
                restaurant=restaurant,
                client=clients[i],
            )
        order = OrderFactory.create(
            client=clients[i],
            employee=employees[i],
            reservation=reservation,
        )
        orders.append(order)
        for dish in dishes[i: i + 2]:
            OrderAndDishFactory.create(
                order=orders[-1],
                dish=dish,
            )
    shuffle(ingredients)
    for restaurant, ingredient in zip(restaurants, ingredients[:len(ingredients) // 2]):
        StopListFactory.create(
            ingredient=ingredient,
            restaurant=restaurant,
        )
