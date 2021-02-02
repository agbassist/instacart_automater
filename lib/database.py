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
                                    id          integer  NOT NULL PRIMARY KEY,
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

    def execute( self, sql_str, args=None ):
        try:
            c = self.conn.cursor()
            if args is None:
                c.execute( sql_str )
            else:
                c.execute( sql_str, args )
            self.conn.commit()
        except Error as e:
            print( e )

    def add_ingredient(self, name, search, quantity, unit):
        sql = ''' INSERT INTO ingredients(name,search,quantity,unit)
                  VALUES(?,?,?,?) '''
        try:
            c = self.conn.cursor()
            c.execute(sql, (name, search, quantity, unit))
            self.conn.commit()
        except Error as e:
            print( '"{}" - {}'.format( name, e ) )

    def get_all_ingredients(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM ingredients")

        return cur.fetchall()

    def get_all_ingredient_names(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, name FROM ingredients")

        return cur.fetchall()

    def get_ingredient_id(self,ingredient):
        cur = self.conn.cursor()
        cur.execute('SELECT id FROM ingredients WHERE name="{}"'.format(ingredient))
        return cur.fetchall()[0][0]

    def delete_ingredient_by_id( self, id ):
        try:
            cur = self.conn.cursor()
            cur.execute( 'DELETE FROM ingredients WHERE id={}'.format( id ) ) 
            self.conn.commit()
        except Error as e:
            print( '"{}" - {}'.format( name, e ) )

    def add_recipe(self, name ):
        sql = ''' INSERT INTO recipes(name)
                  VALUES(?) '''
        try:
            c = self.conn.cursor()
            c.execute(sql, (name,))
            self.conn.commit()
        except Error as e:
            print('"{}" - {}'.format(name, e))

    def get_all_recipes(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM recipes")

        return cur.fetchall()

    def get_recipe_id(self,recipe):
        cur = self.conn.cursor()
        cur.execute('SELECT id FROM recipes WHERE name="{}"'.format(recipe))
        return cur.fetchall()[0][0]

    def add_recipe_item(self, recipe,ingredient,quantity,unit ):

        sql = ''' INSERT INTO recipe_items(recipe,ingredient,quantity,unit)
                  VALUES(?,?,?,?) '''
        try:
            c = self.conn.cursor()
            c.execute(sql, (recipe,ingredient,quantity,unit))
            self.conn.commit()
        except Error as e:
            print('"{}" - {}'.format(name, e))

    def get_items_for_recipe(self, recipe_id):
        cur = self.conn.cursor()
        cur.execute('''
                    SELECT
                    ingredients.name, recipe_items.quantity, recipe_items.unit

                    FROM
                    recipe_items
                    
                    INNER JOIN ingredients ON recipe_items.ingredient = ingredients.id
                    INNER JOIN recipes ON recipe_items.recipe = recipes.id

                    WHERE
                    recipes.id = "{}"

                    ;'''.format( recipe_id ) )
        return cur.fetchall()

# Temporary stuff and testing
if __name__ == '__main__':

    database = Database()
    database.execute( 'DROP TABLE temp;' )