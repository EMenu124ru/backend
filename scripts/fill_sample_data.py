from random import randint

from apps.orders.factories import (
    CategoryFactory,
    DishFactory,
    DishImagesFactory,
    OrderFactory,
    RestaurantAndOrderFactory,
)
from apps.restaurants.factories import RestaurantFactory, ScheduleFactory
from apps.reviews.factories import ReviewFactory, ReviewImagesFactory
from apps.users.factories import ClientFactory, EmployeeFactory, UserFactory

USERS_COUNT = 10
CLIENTS_COUNT = EMPLOYEES_COUNT = 5
DISHES_COUNT = 10
CATEGORIES_COUNT = 2
ORDERS_COUNT = 3
DISH_REVIEWS_COUNT = 10
IMAGES_PER_DISH_COUNT = IMAGES_PER_REVIEW_COUNT = 3
RESTAURANTS_COUNT = 3
RESTAURANT_REVIEWS_COUNT = 3
SCHEDULES_COUNT = 7
RESTAURANT_AND_ORDER_COUNT = 3


def run():
    """Generate examples."""
    # creating 10 users, 5 of them are clients,
    # and other 5 are employees
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
        ReviewImagesFactory.create_batch(
            review=review,
            size=IMAGES_PER_REVIEW_COUNT,
        )
    restaurants = [RestaurantFactory.create(reviews=(review,)) for review in rest_reviews]
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
    categories = CategoryFactory.create_batch(
        size=CATEGORIES_COUNT,
    )
    for review in dish_reviews:
        ReviewImagesFactory.create_batch(
            review=review,
            size=IMAGES_PER_REVIEW_COUNT,
        )
    dishes = []
    for review in dish_reviews:
        category = categories[randint(0, CATEGORIES_COUNT - 1)]
        dishes.append(DishFactory.create(
            category=category,
            reviews=(review,),
            ))
    for dish in dishes:
        DishImagesFactory.create_batch(
            dish=dish,
            size=IMAGES_PER_REVIEW_COUNT,
        )
    orders = []
    for i in range(ORDERS_COUNT):
        orders.append(OrderFactory.create(
            client=clients[i],
            employee=employees[i],
            dishes=dishes[i: i + 2],
        ))
    for order in orders:
        restaurant = restaurants[randint(0, RESTAURANTS_COUNT - 1)]
        RestaurantAndOrderFactory.create(
            order=order,
            restaurant=restaurant,
        )
