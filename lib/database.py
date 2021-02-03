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

    def __init__( self ):
        """ create a database connection to a SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print( e )

    def execute( self, sql_str, args=None ):
        """ commit data to database """
        try:
            c = self.conn.cursor()
            if args is None:
                c.execute( sql_str )
            else:
                c.execute( sql_str, args )
            self.conn.commit()
        except Error as e:
            print( e )

    def fetch( self, sql_str ): 
        """ retrieve from database """ 
        try:
            c = self.conn.cursor()
            c.execute( sql_str )
            return c.fetchall()
        except Error as e:
            print( e )            

    #######################################################
    #                     Ingredients
    #######################################################

    def add_ingredient( self, name, search, quantity, unit ):
        sql = ''' INSERT INTO ingredients(name,search,quantity,unit)
                  VALUES(?,?,?,?) '''
        self.execute( sql )

    def get_all_ingredients( self ):
        return self.fetch( 'SELECT * FROM ingredients' )

    def get_all_ingredient_names( self ):
        return self.fetch( 'SELECT id, name FROM ingredients' )

    def get_ingredient_id( self, ingredient ):
        ret = self.fetch( 'SELECT id FROM ingredients WHERE name="{}"'.format( ingredient ) )
        return ret[0][0]

    def delete_ingredient_by_id( self, id ):
        self.execute( 'DELETE FROM ingredients WHERE id={}'.format( id ) )

    #######################################################
    #                       Recipes
    #######################################################

    def add_recipe( self, name ):
        sql = ''' INSERT INTO recipes(name)
                  VALUES(?) '''
        self.execute( sql, (name,) )

    def get_all_recipes( self ):
        return self.fetch( 'SELECT * FROM recipes' )

    def get_recipe_id( self, recipe ):
        ret = self.fetch( 'SELECT id FROM recipes WHERE name="{}"'.format( recipe ) )
        return ret[0][0]

    #######################################################
    #                    Recipe Items
    #######################################################

    def delete_recipe_item_by_id( self, id ):
        self.execute( 'DELETE FROM recipe_items WHERE id={}'.format( id ) )

    def add_recipe_item( self, recipe, ingredient, quantity, unit ):
        sql = ''' INSERT INTO recipe_items(recipe,ingredient,quantity,unit)
                  VALUES(?,?,?,?) '''
        self.execute( sql, (recipe,ingredient,quantity,unit) )

    def get_items_for_recipe( self, recipe_id ):
        sql = ''' SELECT
                  ingredients.name, recipe_items.quantity, recipe_items.unit, recipe_items.id

                  FROM
                  recipe_items
                  
                  INNER JOIN ingredients ON recipe_items.ingredient = ingredients.id
                  INNER JOIN recipes ON recipe_items.recipe = recipes.id

                  WHERE
                  recipes.id = "{}";'''.format( recipe_id )

        return self.fetch( sql )

# Temporary stuff and testing
if __name__ == '__main__':

    database = Database()
    database.execute( 'DROP TABLE temp;' )