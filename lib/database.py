import sqlite3
from sqlite3 import Error

db_file = 'database/instacart.db'

create_ingredients_table = """CREATE TABLE IF NOT EXISTS ingredients (
                                    id        integer  NOT NULL PRIMARY KEY,
                                    name      text     NOT NULL,
                                    search    text,
                                    quantity  integer,
                                    unit      text
                                );"""

create_recipes_table = """CREATE TABLE IF NOT EXISTS recipes (
                                    id    integer  NOT NULL PRIMARY KEY,
                                    name  text     NOT NULL
                                );"""

create_recipe_items_table = """CREATE TABLE IF NOT EXISTS recipe_items (
                                    recipe      integer  NOT NULL,
                                    ingredient  integer  NOT NULL,
                                    quantity    integer,
                                    unit        text,
                                    FOREIGN KEY (recipe) references recipe (id),
                                    FOREIGN KEY (ingredient) references ingredients (id)
                                );"""


class Database:

    def __init__(self):
        """ create a database connection to a SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def execute(self, sql_str):
        try:
            c = self.conn.cursor()
            c.execute(sql_str)
        except Error as e:
            print(e)

    def add_ingredient(self, name, search, quantity, unit):
        sql = ''' INSERT INTO ingredients(name,search,quantity,unit)
                  VALUES(?,?,?,?) '''
        try:
            c = self.conn.cursor()
            c.execute(sql, (name, search, quantity, unit))
            self.conn.commit()
        except Error as e:
            print('"{}" - {}'.format(name, e))

    def select_all_ingredients(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM ingredients")

        return cur.fetchall()


if __name__ == '__main__':

    database = Database()

    # Create tables
    if False:
        database.execute(create_ingredients_table)
        database.execute(create_recipes_table)
        database.execute(create_recipe_items_table)

    database_ingredients = database.select_all_ingredients()
    print( database_ingredients[0] )
