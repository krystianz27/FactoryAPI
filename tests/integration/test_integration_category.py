from app.models import Category
from tests.factories.models_factory import get_random_category_dict

"""Test POST new category successfully"""


def test_integration_create_new_category_successful(client, db_session_integration):
    # Arrange: Prepare test data
    category_data = get_random_category_dict()
    category_id = category_data.pop("id")

    # Act: Make a POST request to create a new category
    response = client.post("api/category/", json=category_data)

    # Assert: Verify response
    assert response.status_code == 201

    # Assert: Verify the response and database state
    create_category = (
        db_session_integration.query(Category).filter_by(id=category_id).first()
    )
    assert create_category is not None

    # Assert: Verify response data matches database entry
    assert response.json() == {
        column.name: getattr(create_category, column.name)
        for column in create_category.__table__.columns
    }


"""
- [ ] Test POST new category duplicate name and level
"""


def test_integration_create_new_category_duplicate(client, db_session_integration):
    category_data = get_random_category_dict()
    new_category = Category(**category_data)
    db_session_integration.add(new_category)
    db_session_integration.commit()
    category_data.pop("id")

    response = client.post("api/category/", json=category_data)

    assert response.status_code == 400


"""
- [ ] Test POST new category duplicate slug
"""


def test_integration_create_new_category_duplicate_slug(client, db_session_integration):
    # Generate two random categories
    category1 = get_random_category_dict()
    category2 = get_random_category_dict()

    # Ensure both categories have the same slug
    slug = "same-slug"
    category1["slug"] = slug
    category2["slug"] = slug

    # Add the first category to the database
    db_session_integration.add(Category(**category1))
    db_session_integration.commit()

    # Attempt to add the second category via the API endpoint
    response = client.post("api/category/", json=category2)

    # Verify that the insertion of the second category fails due to duplicate slug
    assert response.status_code == 400


"""
- [ ] Test to return all categories successfully
"""


def test_integration_get_all_categories(client, db_session_integration):
    categories = [get_random_category_dict() for i in range(5)]

    for category_data in categories:
        category_data.pop("id", None)
        new_category = Category(**category_data)
        db_session_integration.add(new_category)
        db_session_integration.commit()

    response = client.get("/api/category/")

    assert response.status_code == 200
    assert response.json() is not None

    returned_catgories = response.json()
    assert isinstance(returned_catgories, list)
    assert len(returned_catgories) == len(categories)

    for returned_category, inserted_category_data in zip(
        returned_catgories, categories
    ):
        assert returned_category["name"] == inserted_category_data["name"]
        assert returned_category["slug"] == inserted_category_data["slug"]
        assert returned_category["is_active"] == inserted_category_data["is_active"]
        assert returned_category["level"] == inserted_category_data["level"]


"""
- [ ] Test update category successfully
"""


def test_integration_update_category_successfully(client, db_session_integration):
    initial_category_data = get_random_category_dict()
    new_category = Category(**initial_category_data)
    db_session_integration.add(new_category)
    db_session_integration.commit()

    updated_category_data = {
        "name": "Updated Name",
        "slug": "updated-slug",
        "is_active": False,
        "level": 10,
    }

    response = client.put(
        f"/api/category/{new_category.id}", json=updated_category_data
    )

    assert response.status_code == 200

    updated_category = (
        db_session_integration.query(Category).filter_by(id=new_category.id).first()
    )

    assert updated_category is not None
    assert updated_category.name == updated_category_data["name"]
    assert updated_category.slug == updated_category_data["slug"]
    assert updated_category.is_active == updated_category_data["is_active"]
    assert updated_category.level == updated_category_data["level"]


"""
- [ ] Test delete category successfully
"""


def test_integration_delete_category_successfully(client, db_session_integration):
    category_data = get_random_category_dict()
    new_category = Category(**category_data)
    db_session_integration.add(new_category)
    db_session_integration.commit()

    response = client.delete(f"/api/category/{new_category.id}")

    assert response.status_code == 200

    assert response.json()["id"] == category_data["id"]
    assert response.json()["name"] == category_data["name"]

    deleted_category = (
        db_session_integration.query(Category).filter_by(id=new_category.id).first()
    )

    assert deleted_category is None
