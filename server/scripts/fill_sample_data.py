from random import randint

from apps.orders.factories import (
    CategoryFactory,
    DishFactory,
    DishImageFactory,
    OrderAndDishFactory,
    OrderFactory,
    ReservationFactory,
    IngredientFactory,
)
from apps.restaurants.factories import PlaceFactory, RestaurantFactory
from apps.restaurants.factories import ScheduleFactory as RestaurantScheduleFactory
from apps.restaurants.factories import TagToPlaceFactory
from apps.users.factories import ClientFactory, EmployeeFactory
from apps.users.factories import ScheduleFactory as EmployeeScheduleFactory
from apps.users.factories import UserFactory

USERS_COUNT = 20
CLIENTS_COUNT = EMPLOYEES_COUNT = 10
EMPLOYEE_SCHEDULE_COUNT = 5
CATEGORIES_COUNT = 2
ORDERS_COUNT = 10
DISH_REVIEWS_COUNT = 10
IMAGES_PER_DISH_COUNT = IMAGES_PER_REVIEW_COUNT = 3
RESTAURANTS_COUNT = 3
SCHEDULES_COUNT = 7
TAGS_COUNT = PLACE_COUNT = 10


def run():
    """Generate examples."""
    users = UserFactory.create_batch(
        size=USERS_COUNT,
    )
    clients = [
        ClientFactory.create(user=user)
        for user in users[:len(users) // 2]
    ]
    tags = TagToPlaceFactory.create_batch(size=TAGS_COUNT)
    restaurants = []
    for _ in range(RESTAURANTS_COUNT):
        restaurants.append(RestaurantFactory.create())
    for _ in range(SCHEDULES_COUNT):
        restaurant = restaurants[randint(0, RESTAURANTS_COUNT - 1)]
        RestaurantScheduleFactory.create(restaurant=restaurant)
    for restaurant in restaurants:
        places = PlaceFactory.create_batch(size=PLACE_COUNT, restaurant=restaurant)
        for place in places:
            restaurant.places.add(place)
            for i in range(randint(1, TAGS_COUNT)):
                place.tags.add(tags[i])
    employees = []
    for i in range(EMPLOYEES_COUNT, USERS_COUNT):
        restaurant = restaurants[randint(0, RESTAURANTS_COUNT - 1)]
        employee = EmployeeFactory.create(user=users[i], restaurant=restaurant)
        employees.append(employee)
        EmployeeScheduleFactory.create_batch(
            size=EMPLOYEE_SCHEDULE_COUNT,
            employee=employee,
        )
    dish_reviews = []
    categories = CategoryFactory.create_batch(
        size=CATEGORIES_COUNT,
    )
    dishes = []
    for review in dish_reviews:
        category = categories[randint(0, CATEGORIES_COUNT - 1)]
        dishes.append(DishFactory.create(
            category=category,
        ))
        dishes[-1].reviews.add(review)
    for dish in dishes:
        DishImageFactory.create_batch(
            dish=dish,
            size=IMAGES_PER_REVIEW_COUNT,
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
