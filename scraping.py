import os
import sqlite3
import random
from time import sleep

import requests
from bs4 import BeautifulSoup
import json

from utils.database import Database


def get_data(url):

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/135.0.0.0 Safari/537.36"
    }

    # req = requests.get(url=url, headers=headers)
    # src = req.text
    #
    # soup = BeautifulSoup(src, "lxml")
    # categories = soup.find_all("a", class_="main-categories__item")
    #
    # categories_names = []
    # categories_urls = []
    #
    # for category in categories:
    #     link = category.get("href")
    #     categories_urls.append("https://www.forward-sport.ru" + link)
    #
    #     name = category.find("div", class_="main-categories__text").text
    #     categories_names.append(name)
    #
    # with open("scrap_data/categories_urls.txt", "w", encoding="utf-8") as file:
    #     for line in categories_urls:
    #         file.write(f"{line}\n")
    #
    # with open("scrap_data/categories_names.txt", "w", encoding="utf-8") as file:
    #     for line in categories_names:
    #         file.write(f"{line}\n")

    with open("scrap_data/categories_urls.txt", encoding="utf-8") as file:
        src = [line.strip() for line in file.readlines()]

    created_folders = 0  # счётчик для перечисления имён категорий

    # парсим всё необходимое с каждой ссылки
    for link in src:

        with open("scrap_data/categories_names.txt", encoding="utf-8") as file:
            names = [line.strip() for line in file.readlines()]

        folder_name = f"scrap_data/{names[created_folders]}"
        os.makedirs(folder_name, exist_ok=True)

        page = 1
        while True:
            req = requests.get(url=link + f"?PAGEN_1={page}", headers=headers)
            src = req.text

            soup = BeautifulSoup(src, "lxml")
            products = soup.find_all("div", class_="col-6 col-md-4 col-xxl-3 section_item")
            pagination = soup.find_all("a", class_="disabled pagination_custom__page icon_custom_next")

            product_info = []  # спарсенная страница
            for i in products:
                product_img = i.find("a", class_="main_product__img").find("div", class_="product__img").find("img").get("src")
                product_title = i.find("a", class_="main_product__title").text
                if i.find("p", class_="main_product__price").find("span", class_="main_product__old_price"):
                    product_price = i.find("p",
                                    class_="main_product__price").next_element.next_element.next_element.next_element.text.replace(
                                    "\xa0", "").strip()
                else:
                    product_price = i.find("p", class_="main_product__price").text.replace("\xa0", "").strip()

                product_info.append({
                    "Image": product_img,
                    "Title": product_title,
                    "Price": product_price.replace('₽', '')
                })

            for item in product_info:
                db = Database(f'{folder_name}/products_page.db')
                db.add_product(item['Image'], item['Title'], item['Price'])

            print(f"Страница {page} записана")
            page += 1

            if pagination:
                print("Завершение цикла")
                break

            sleep(random.randrange(1, 2))

        created_folders += 1

        # scrap_data / {url.split("/")[-2]}


def main():
    get_data("https://www.forward-sport.ru/")

if __name__ == "__main__":
    main()



