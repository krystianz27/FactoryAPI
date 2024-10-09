from itertools import count

from faker import Faker

faker = Faker()


def get_random_user_dict(id_: int = None):
    if id_ is None:
        id_counter = count(start=1)
        id_ = next(id_counter)

    return {
        "id": id_,
        "username": faker.user_name(),
        "email": faker.email(),
        "password": faker.password(),
        # "hashed_password": hash_password("default_password"),  # Hasło jest haszowane
        "is_active": True,
        "is_superuser": False,
    }
