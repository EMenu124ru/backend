from random import (
    choice,
    randint,
    shuffle,
)

from apps.orders.factories import (
    CategoryFactory,
    DishFactory,
    OrderAndDishFactory,
    OrderFactory,
    ReservationFactory,
    StopListFactory,
)
from apps.restaurants.factories import RestaurantFactory
from apps.users.factories import (
    ClientFactory,
    EmployeeFactory,
    UserFactory,
)


USERS_COUNT = 20
CLIENTS_COUNT = EMPLOYEES_COUNT = 10
EMPLOYEE_SCHEDULE_COUNT = 5
CATEGORIES_COUNT = 5
ORDERS_COUNT = 10
DISH_IN_CATEGORY_COUNT = 3
RESTAURANTS_COUNT = 3


def run():
    """Generate examples."""
    users = UserFactory.create_batch(
        size=USERS_COUNT,
    )
    clients = [
        ClientFactory.create(user=user)
        for user in users[:len(users) // 2]
    ]
    restaurants = RestaurantFactory.create_batch(
        size=RESTAURANTS_COUNT,
    )
    employees = []
    for i in range(EMPLOYEES_COUNT, USERS_COUNT):
        restaurant = restaurants[randint(1, RESTAURANTS_COUNT) - 1]
        employee = EmployeeFactory.create(user=users[i], restaurant=restaurant)
        employees.append(employee)
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
    orders = []
    for i in range(ORDERS_COUNT):
        reservation = None
        if randint(0, 1):
            restaurant = restaurants[randint(1, RESTAURANTS_COUNT) - 1]
            reservation = ReservationFactory.create(
                restaurant=restaurant,
                client=clients[i],
                place=choice(restaurant.places.all()),
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
                employee=employees[i],
            )
    shuffle(ingredients)
    for restaurant, ingredient in zip(restaurants, ingredients[:len(ingredients) // 2]):
        StopListFactory.create(
            ingredient=ingredient,
            restaurant=restaurant,
        )
