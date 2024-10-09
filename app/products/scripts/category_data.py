from sqlalchemy.orm import Session

from app.products.models import Category


def add_sample_categories(db: Session):
    category1 = Category(
        name="Electronics",
        slug="electronics",
        is_active=True,
        level=100,
        parent_id=None,
    )

    category2 = Category(
        name="Smartphones",
        slug="smartphones",
        is_active=True,
        level=200,
        parent_id=1,  # Assuming that, Electronics has id = 1
    )

    category3 = Category(
        name="Laptops",
        slug="laptops",
        is_active=True,
        level=200,
        parent_id=1,  # Assuming that, Electronics ma id = 1
    )

    db.add_all([category1, category2, category3])
    db.commit()
