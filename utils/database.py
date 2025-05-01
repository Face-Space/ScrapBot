import sqlite3


class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = ("CREATE TABLE IF NOT EXISTS products("
                     "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "img_url TEXT,"
                     "product_name TEXT,"
                     "product_price FLOAT)")
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as E:
            print("Произошла ошибка при создании базы данных!", E)


    def add_product(self, img_url, product_name, product_price):
        self.cursor.execute("INSERT INTO products (img_url, product_name, product_price) VALUES (?, ?, ?)",
                            (img_url, product_name, product_price))
        self.connection.commit()


    def get_min_price(self):
        # query = "SELECT * FROM products WHERE product_price = (SELECT MIN(product_price) FROM products)"
        query = "SELECT * FROM products ORDER BY product_price ASC LIMIT 3"
        self.cursor.execute(query)
        min_product = self.cursor.fetchall()
        return min_product


    def get_max_price(self):
        # query = "SELECT * FROM products WHERE product_price = (SELECT MAX(product_price) FROM products)"
        query = "SELECT * FROM products ORDER BY product_price DESC LIMIT 3"
        self.cursor.execute(query)
        max_product = self.cursor.fetchall()
        return max_product

    def get_all_products(self):
        query = "SELECT * FROM products"
        self.cursor.execute(query)
        all_products = self.cursor.fetchall()
        return all_products

    def __del__(self):
        self.cursor.close()
        self.connection.close()


