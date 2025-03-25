from typing import Generator

from faker import Faker

from objects.user import User


def user_generator() -> Generator[User, None, None]:
    Faker.seed(0)
    fake = Faker()
    while True:
        user = User()
        user.url = fake.url()
        user.email = fake.email()
        user.last_name = fake.last_name()
        user.first_name = fake.first_name()
        yield user
