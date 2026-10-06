import pandas as pd
from sqlalchemy import create_engine


# Create SQLite database
engine = create_engine("sqlite:///shopping.db")


def create_database():
    products = pd.read_csv("products.csv")

    products.to_sql(
        "products",
        engine,
        if_exists="replace",
        index=False
    )

    print("Products added to database successfully!")


if __name__ == "__main__":
    create_database()