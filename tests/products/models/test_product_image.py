from sqlalchemy import Integer, String

"""
## Table and Column Validation
"""

"""
- [ ] Confirm the presence of all required tables within the database schema.
"""


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("product_image")


"""
- [ ] Validate the existence of expected columns in each table, ensuring correct data types.
"""


def test_model_structure_column_data_types(db_inspector):
    table = "product_image"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["alternative_text"]["type"], String)
    assert isinstance(columns["url"]["type"], String)
    assert isinstance(columns["order"]["type"], Integer)
    assert isinstance(columns["product_line_id"]["type"], Integer)


"""
- [ ] Verify nullable or not nullable fields
"""


def test_model_structure_nullable_constraints(db_inspector):
    table = "product_image"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "alternative_text": False,
        "url": False,
        "order": False,
        "product_line_id": False,
    }
    # print(columns)
    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column '{column_name}' is not nullable as expected"


"""
- [ ] Ensure that column foreign keys correctly defined.
"""


def test_model_structure_foreign_key(db_inspector):
    table = "product_image"
    foreign_keys = db_inspector.get_foreign_keys(table)
    # print(foreign_keys)
    product_image_foreign_key = next(
        (
            fk
            for fk in foreign_keys
            if set(fk["constrained_columns"]) == {"product_line_id"}
        ),
        None,
    )
    assert product_image_foreign_key is not None


"""
- [ ] Test columns with specific constraints to ensure they are accurately defined.
"""


def test_model_structure_column_constraints(db_inspector):
    table = "product_image"
    constraints = db_inspector.get_check_constraints(table)
    # print(constraints)
    assert any(
        constraint["name"] == "product_image_order_range" for constraint in constraints
    )
    assert any(
        constraint["name"] == "product_image_alternative_length_check"
        for constraint in constraints
    )
    assert any(
        constraint["name"] == "product_image_url_length_check"
        for constraint in constraints
    )


"""
- [ ] Verify the correctness of default values for relevant columns.
"""

"""
- [ ] Ensure that column lengths align with defined requirements.
"""


def test_model_structure_column_lengths(db_inspector):
    table = "product_image"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["alternative_text"]["type"].length == 100
    assert columns["url"]["type"].length == 100


"""
- [ ]  Validate the enforcement of unique constraints for columns requiring unique values.
"""


def test_model_structure_unique_constraints(db_inspector):
    table = "product_image"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_product_image_order_product_line_id"
        for constraint in constraints
    )
