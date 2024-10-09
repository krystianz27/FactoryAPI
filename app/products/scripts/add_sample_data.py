from app.db_connection import get_db_session
from app.products.scripts.category_data import add_sample_categories

# from app.scripts.product_data import add_sample_products
# from app.scripts.product_line_data import add_sample_product_lines


def main():
    with get_db_session() as db:
        add_sample_categories(db)
        # add_sample_products(db)
        # add_sample_product_lines(db)


if __name__ == "__main__":
    main()
