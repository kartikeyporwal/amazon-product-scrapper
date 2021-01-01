import os
import time

import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from parse_amazon import ingest_data


def save_page_source(file_path, page_source):
    with open(file_path, "w", encoding="UTF-8") as f:
        f.write(page_source)


def get_next_page_url(file_path):
    """Retrieves path of the next page from the downloaded web page.

    Arguments:
        file_path {str} -- file path of the downloaded web page
    
    Returns:
        next_page_url {str} -- url of the next product page
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            file_data = f.read()

        soup = bs4.BeautifulSoup(file_data, "lxml")

        return url + soup.find("ul", class_=pagination_class).find("li", class_=last_page_class).find("a").attrs.get("href", None)

    except Exception as error:
        print(f"Error occurred when locating next page url")
        return None


if __name__ == "__main__":

    product_to_search = "baby milk"

    # classes and ids
    search_bar_id = "twotabsearchtextbox"
    pagination_class = "a-pagination"
    last_page_class = "a-last"

    url = r"https://www.amazon.com"

    driver = webdriver.Firefox(
        executable_path=r"geckodriver.exe")
    driver.maximize_window()
    print(f"Driver initialized")

    product_page_dir = os.path.join(
        os.path.dirname(__file__), rf"{product_to_search}")
    os.makedirs(product_page_dir, exist_ok=True)

    page_count = 1
    page_path = os.path.join(
        product_page_dir, f"{product_to_search}_{page_count}.html")

    # loading amazon.com
    driver.get(url)
    print(f"Amazon loaded")

    # searching for the product
    search_bar = driver.find_element_by_id(search_bar_id)
    search_bar.send_keys(product_to_search, Keys.ENTER)

    print(f"Product is searched for page - {page_count}")
    time.sleep(10)

    # saving all the pages
    save_page_source(
        file_path=page_path,
        page_source=driver.page_source)

    next_page_url = get_next_page_url(file_path=page_path)

    while next_page_url:
        driver.get(next_page_url)
        time.sleep(10)
        page_count += 1
        print(f"Product is searched for page - {page_count}")

        page_path = os.path.join(
            product_page_dir, f"{product_to_search}_{page_count}.html")

        save_page_source(
            file_path=page_path,
            page_source=driver.page_source)

        next_page_url = get_next_page_url(file_path=page_path)

    ingest_data(page_dir=product_page_dir,
                csv_file_path=f"{product_to_search}.csv")
