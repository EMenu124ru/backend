from random import randint

from apps.orders.factories import (
    CategoryFactory,
    DishFactory,
    DishImageFactory,
    OrderAndDishFactory,
    OrderFactory,
    RestaurantAndOrderFactory,
)
from apps.restaurants.factories import RestaurantFactory, ScheduleFactory
from apps.reviews.factories import ReviewFactory, ReviewImageFactory
from apps.users.factories import ClientFactory, EmployeeFactory, UserFactory

USERS_COUNT = 10
CLIENTS_COUNT = EMPLOYEES_COUNT = 5
CATEGORIES_COUNT = 2
ORDERS_COUNT = 3
DISH_REVIEWS_COUNT = 10
IMAGES_PER_DISH_COUNT = IMAGES_PER_REVIEW_COUNT = 3
RESTAURANTS_COUNT = 3
RESTAURANT_REVIEWS_COUNT = 3
SCHEDULES_COUNT = 7


def run():
    """Generate examples."""
    users = UserFactory.create_batch(
        size=USERS_COUNT,
    )
    clients = [
        ClientFactory.create(user=users[i])
        for i in range(CLIENTS_COUNT)
    ]
    rest_reviews = []
    for _ in range(RESTAURANT_REVIEWS_COUNT):
        client = clients[randint(0, CLIENTS_COUNT - 1)]
        rest_reviews.append(ReviewFactory.create(client=client))
    for review in rest_reviews:
        ReviewImageFactory.create_batch(
            review=review,
            size=IMAGES_PER_REVIEW_COUNT,
        )
    restaurants = []
    for review in rest_reviews:
        restaurants.append(RestaurantFactory.create())
        restaurants[-1].reviews.add(review)
    for _ in range(SCHEDULES_COUNT):
        restaurant = restaurants[randint(0, RESTAURANTS_COUNT - 1)]
        ScheduleFactory.create(restaurant=restaurant)
    employees = []
    for i in range(EMPLOYEES_COUNT, USERS_COUNT):
        restaurant = restaurants[randint(0, RESTAURANTS_COUNT - 1)]
        employees.append(EmployeeFactory.create(user=users[i], restaurant=restaurant))
    dish_reviews = []
    for _ in range(DISH_REVIEWS_COUNT):
        client = clients[randint(0, CLIENTS_COUNT - 1)]
        dish_reviews.append(ReviewFactory.create(client=client))
    for review in dish_reviews:
        ReviewImageFactory.create_batch(
            review=review,
            size=IMAGES_PER_REVIEW_COUNT,
        )
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
        orders.append(OrderFactory.create(
            client=clients[i],
            employee=employees[i],
        ))
        for dish in dishes[i: i + 2]:
            OrderAndDishFactory.create(
                order=orders[-1],
                dish=dish,
            )
    for order in orders:
        restaurant = restaurants[randint(0, RESTAURANTS_COUNT - 1)]
        RestaurantAndOrderFactory.create(
            order=order,
            restaurant=restaurant,
        )
