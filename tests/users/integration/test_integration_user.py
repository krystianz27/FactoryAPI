from app.users.models import User
from tests.users.factories.models_factory import get_random_user_dict
from tests.users.utils.hashing_utils import hash_password

"""
- [ ] Test GET protected endpoint with valid user
"""


def test_integration_create_new_user_successful(client, db_session_integration):
    # Arrange: Prepare test data
    user_data = get_random_user_dict()
    user_data.pop("id")  # Usuń 'id', bo będzie generowane przez DB

    # Act: Make a POST request to create a new user
    response = client.post("/users/", json=user_data)

    # Assert: Verify response status code
    assert response.status_code == 201

    # Assert: Verify the response and database state
    created_user = (
        db_session_integration.query(User)
        .filter_by(username=user_data["username"])
        .first()
    )
    assert created_user is not None

    # Assert: Verify response data matches database entry
    assert response.json() == {
        "id": created_user.id,
        "username": created_user.username,
        "email": created_user.email,
        "is_active": created_user.is_active,
        "is_superuser": created_user.is_superuser,
    }


def test_integration_read_protected_user_route(client, db_session_integration):
    # Arrange: Prepare test data
    user_data = get_random_user_dict()
    # user_data["password"] = "user_password"  # Ustaw hasło

    # Create a new user in the database
    hashed_password = hash_password(user_data["password"])
    new_user = User(
        username=user_data["username"],
        email=user_data["email"],
        hashed_password=hashed_password,
    )
    db_session_integration.add(new_user)
    db_session_integration.commit()

    # Act: Log in to get the JWT token
    login_response = client.post(
        "users/token/",
        json={"username": user_data["username"], "password": user_data["password"]},
    )

    assert login_response.status_code == 200

    token = login_response.json().get("access_token")

    # Act: Make a GET request to the protected user route
    protected_response = client.get(
        "/users/protected-user", headers={"Authorization": f"Bearer {token}"}
    )

    # Assert: Verify response status code and content
    assert protected_response.status_code == 200
    protected_user_data = protected_response.json()
    assert protected_user_data["username"] == user_data["username"]
    assert protected_user_data["email"] == user_data["email"]
    assert protected_user_data["is_active"] is True
    assert protected_user_data["is_active"] is True
