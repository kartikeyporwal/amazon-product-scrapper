import bs4
import os
import pandas as pd
import pymysql
import glob

file_path = r"C:\Users\kartikey\Desktop\saviance\baby milk\baby milk_1.html"


def parse_page(file_path):
    print(f"Parsing file - {file_path}")
    with open(file_path, "r", encoding="UTF-8") as f:
        file_data = f.read()

    soup = bs4.BeautifulSoup(file_data, "lxml")

    products_list = []

    product_class = "s-main-slot s-result-list s-search-results sg-row"

    sponsored_product_class = "sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col sg-col-4-of-20"
    normal_product_class = "sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"
    product_title_class = "a-size-base-plus a-color-base a-text-normal"
    review_count_class = "a-size-base"
    rating_class = "a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom"
    price_class = "a-price"

    products = soup.find("div", class_=product_class)
    if products:
        sponsored_products = products.find_all(
            "div", class_=sponsored_product_class)
        normal_products = products.find_all("div", class_=normal_product_class)

        # processing all sponsored products
        for sponsored_product in sponsored_products:
            asin = sponsored_product.attrs.get("data-asin", None)
            product_name = getattr(sponsored_product.find(
                "span", class_=product_title_class), "text", None)

            review_count = getattr(sponsored_product.find(
                "span", class_=review_count_class), "text", None)

            rating = getattr(sponsored_product.find(
                "i", class_=rating_class), "text", None)

            price = getattr(sponsored_product.find(
                "span", class_=price_class), "text", None)
            price = price[:price.rindex("$")] if price else price

            product_dict = {
                "asin": asin,
                "product_name": product_name,
                "price": price,
                "sponsored": "Yes",
                "review_count": review_count,
                "ratings": rating,
            }

            products_list.append(
                product_dict
            )

        # processing all normal products
        for normal_product in normal_products:
            asin = normal_product.attrs.get("data-asin", None)
            product_name = getattr(normal_product.find(
                "span", class_=product_title_class), "text", None)
            review_count = getattr(normal_product.find(
                "span", class_=review_count_class), "text", None)
            rating = getattr(normal_product.find(
                "i", class_=rating_class), "text", None)
            price = getattr(normal_product.find(
                "span", class_=price_class), "text", None)
            price = price[:price.rindex("$")] if price else price

            product_dict = {
                "asin": asin,
                "product_name": product_name,
                "price": price,
                "sponsored": "No",
                "review_count": review_count,
                "ratings": rating,
            }


            products_list.append(
                product_dict
            )

    else:
        print(f"No Products are retrieved for file - {file_path}")

    return products_list

# print(products_list)

# pd.DataFrame(products_list).to_csv("test.csv", index=False)


def ingest_data(page_dir, csv_file_path):
    complete_product_list = []
    for file_path in glob.iglob(os.path.join(page_dir, "*.html")):
        complete_product_list.extend(
            parse_page(file_path)
        )

    insert_data(data=complete_product_list)

    pd.DataFrame(complete_product_list).to_csv(csv_file_path, index=False)


def insert_data(data):
    db_config = {
        "user": "user",
        "host": "localhost",
        "port": 3307,
        "db": "test_db",
        "password": "user"
    }

    connection = pymysql.connect(
        **db_config,
        # cursors=pymysql.cursors.DictCursor
    )

    with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        query = """INSERT into amazon (asin,
                                    product_name,
                                    price,
                                    sponsored,
                                    review_count,
                                    ratings)
                                    VALUES(
                                        %(asin)s,
                                        %(product_name)s,
                                        %(price)s,
                                        %(sponsored)s,
                                        %(review_count)s,
                                        %(ratings)s
                                    )
                                    """
        cursor.executemany(query, data)

        connection.commit()

    print(f"Data inserted")


if __name__ == "__main__":
    ingest_data(page_dir=r"C:\Users\kartikey\Desktop\saviance\baby milk",
             csv_file_path="temp.csv")
