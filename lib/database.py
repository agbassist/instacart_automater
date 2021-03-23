import sqlite3
from sqlite3 import Error
from lib.ingredient import Ingredient

db_file = 'database/instacart.db'

sql_create_ingredients_table = """CREATE TABLE IF NOT EXISTS ingredients (
                                  id        integer  NOT NULL PRIMARY KEY,
                                  name      text     NOT NULL,
                                  search    text,
                                  quantity  integer,
                                  unit      text
                               );"""

sql_create_recipes_table = """CREATE TABLE IF NOT EXISTS recipes (
                              id    integer  NOT NULL PRIMARY KEY,
                              name  text     NOT NULL
                           );"""

sql_create_recipe_items_table = """CREATE TABLE IF NOT EXISTS recipe_items (
                                   id          integer  NOT NULL PRIMARY KEY,
                                   recipe      integer  NOT NULL,
                                   ingredient  integer  NOT NULL,
                                   quantity    integer,
                                   unit        text,
                                   FOREIGN KEY (recipe) references recipe (id),
                                   FOREIGN KEY (ingredient) references ingredients (id)
                                );"""

sql_create_selected_recipes_table = """CREATE TABLE IF NOT EXISTS selected_recipes (
                                       id        integer  NOT NULL PRIMARY KEY,
                                       recipe    integer  NOT NULL,
                                       FOREIGN KEY (recipe) references recipe (id)
                                    );"""

sql_create_selected_ingredients_table = """CREATE TABLE IF NOT EXISTS selected_ingredients (
                                           id         integer  NOT NULL PRIMARY KEY,
                                           ingredient integer  NOT NULL,
                                           quantity   integer,
                                           unit       text,
                                           FOREIGN KEY (ingredient) references ingredients (id)
                                        );"""                                

class Database( object ):

    def __init__( self ):
        """ create a database connection to a SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print( "ARG Error: " + e )

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

    def create_ingredient_table( self ):
        self.execute( sql_create_ingredients_table )

    def add_ingredient( self, name, search, quantity, unit ):
        sql = ''' INSERT INTO ingredients( name, search, quantity, unit )
                  VALUES( ?, ?, ?, ? ) '''
        self.execute( sql, ( name, search, quantity, unit ) )

    def get_all_ingredients( self ):
        ret = []
        ingredients = self.fetch( 'SELECT * FROM ingredients' )

        if ingredients is not None:
            for ingredient in ingredients:
                row = {}
                row[ 'id' ] = ingredient[ 0 ]
                row[ 'name' ] = ingredient[ 1 ]
                row[ 'search' ] = ingredient[ 2 ]
                row[ 'quantity' ] = ingredient[ 3 ]
                row[ 'unit' ] = ingredient[ 4 ]
                ret.append( row )

        return ret

    def get_all_ingredient_names( self ):
        return self.fetch( 'SELECT id, name FROM ingredients' )

    def get_ingredient_id( self, ingredient ):
        ret = self.fetch( 'SELECT id FROM ingredients WHERE name="{}"'.format( ingredient ) )
        if ret is None:
            return None
        else:
            return ret[ 0 ][ 0 ]

    def get_ingredient_by_id( self, id ):
        ingredient = self.fetch( 'SELECT * FROM ingredients WHERE id={}'.format( id ) )

        if len( ingredient ) == 0:
            assert False
        else:
            ret = {}
            ret[ 'id' ] = ingredient[ 0 ][ 0 ]
            ret[ 'name' ] = ingredient[ 0 ][ 1 ]
            ret[ 'search' ] = ingredient[ 0 ][ 2 ]
            ret[ 'quantity' ] = ingredient[ 0 ][ 3 ]
            ret[ 'unit' ] = ingredient[ 0 ][ 4 ]
            return ret 

    def delete_ingredient_by_id( self, id ):
        self.execute( 'DELETE FROM ingredients WHERE id={}'.format( id ) )
        self.execute( 'DELETE FROM selected_ingredients WHERE ingredient={}'.format( id ) )

    #######################################################
    #                       Recipes
    #######################################################

    def create_recipes_table( self ):
        self.execute( sql_create_recipes_table )

    def add_recipe( self, name ):
        sql = ''' INSERT INTO recipes( name )
                  VALUES( ? ) '''
        self.execute( sql, ( name, ) )

    def get_all_recipes( self ):
        ret = []
        recipes = self.fetch( 'SELECT * FROM recipes' )
        
        if recipes is not None:
            for recipe in recipes:
                row = {}
                row[ 'id' ] = recipe[ 0 ]
                row[ 'name' ] = recipe[ 1 ]
                ret.append( row )

        return ret

    def get_all_recipes_tuple_list( self ):
        ret = []
        for database_recipe in self.get_all_recipes():
            ret.append( ( database_recipe[ 'id' ], database_recipe[ 'name' ] ) )

        return ret

    def get_recipe_id( self, recipe ):
        ret = self.fetch( 'SELECT id FROM recipes WHERE name="{}"'.format( recipe ) )
        if ret is None:
            return None
        else:
            return ret[ 0 ][ 0 ]

    def get_recipe_name( self, id ):
        ret = self.fetch( 'SELECT name FROM recipes WHERE id="{}"'.format( id ) )
        if ret is None:
            return None
        else:
            return ret[ 0 ][ 0 ]

    def delete_recipe( self, id ):
        self.execute( 'DELETE FROM recipes WHERE id={}'.format( id ) )
        self.execute( 'DELETE FROM recipe_items WHERE recipe={}'.format( id ) )
        self.execute( 'DELETE FROM selected_recipes WHERE recipe={}'.format( id ) )

    #######################################################
    #                    Recipe Items
    #######################################################

    def create_recipe_items_table( self ):
        self.execute( sql_create_recipe_items_table )

    def delete_recipe_item_by_id( self, id ):
        self.execute( 'DELETE FROM recipe_items WHERE id={}'.format( id ) )

    def add_recipe_item( self, recipe, ingredient, quantity, unit ):
        sql = ''' INSERT INTO recipe_items( recipe, ingredient, quantity, unit)
                  VALUES( ?, ?, ?, ? ) '''
        self.execute( sql, ( recipe, ingredient, quantity, unit ) )

    def get_ingredients_for_recipe( self, recipe_id ):
        sql = ''' SELECT
                  ingredients.name, recipe_items.quantity, recipe_items.unit, ingredients.id

                  FROM
                  recipe_items
                  
                  INNER JOIN ingredients ON recipe_items.ingredient = ingredients.id
                  INNER JOIN recipes ON recipe_items.recipe = recipes.id

                  WHERE
                  recipes.id = "{}";'''.format( recipe_id )

        ret = []
        ingredients = self.fetch( sql )

        if ingredients is not None:
            for ingredient in ingredients:
                row = {}
                row[ 'name' ] = ingredient[ 0 ]
                row[ 'quantity' ] = ingredient[ 1 ]
                row[ 'unit' ] = ingredient[ 2 ]
                row[ 'id' ] = ingredient[ 3 ]
                ret.append( row )

        return ret

    #######################################################
    #                  Selected Recipes
    #######################################################

    def create_selected_recipes_table( self ):
        self.execute( sql_create_selected_recipes_table )

    def add_selected_recipe( self, recipe_id ):
        sql = ''' INSERT INTO selected_recipes( recipe )
                  VALUES( ? ) '''
        self.execute( sql, ( recipe_id, ) )

    def delete_selected_recipe( self, id ):
        self.execute( 'DELETE FROM selected_recipes WHERE id={}'.format( id ) )

    def get_all_selected_recipes( self ):
        sql = '''SELECT
                 selected_recipes.id,
                 recipes.name,
                 recipes.id

                 FROM
                 selected_recipes

                 INNER JOIN recipes on recipes.id = selected_recipes.recipe'''

        ret = []
        recipes = self.fetch( sql )

        if recipes is not None:
            for recipe in recipes:
                recipe_dict = {}
                recipe_dict[ 'id' ] = recipe[ 0 ]
                recipe_dict[ 'name' ] = recipe[ 1 ]
                recipe_dict[ 'recipe_id' ] = recipe[ 2 ]
                ret.append( recipe_dict )

        return ret

    #######################################################
    #                Selected Ingredients
    #######################################################

    def create_selected_ingredients_table( self ):
        self.execute( sql_create_selected_ingredients_table )

    def add_selected_ingredient( self, ingredient, quantity, unit ):
        sql = ''' INSERT INTO selected_ingredients( ingredient, quantity, unit )
                  VALUES( ?, ?, ? ) '''
        self.execute( sql, ( ingredient, quantity, unit ) )

    def delete_selected_ingredient( self, id ):
        self.execute( 'DELETE FROM selected_ingredients WHERE id={}'.format( id ) )

    def get_all_selected_ingredients( self ):
        sql = '''SELECT
                 ingredients.id,
                 ingredients.name,
                 ingredients.search,
                 selected_ingredients.quantity,
                 selected_ingredients.unit,
                 selected_ingredients.id

                 FROM
                 selected_ingredients

                 INNER JOIN ingredients ON ingredients.id = selected_ingredients.ingredient'''

        ingredients = self.fetch( sql )
        ret = []
        
        if ingredients is not None:
            for ingredient in ingredients:
                ingredient_dict = {}
                ingredient_dict[ 'id' ] = ingredient[ 0 ]
                ingredient_dict[ 'name' ] = ingredient[ 1 ]
                ingredient_dict[ 'search' ] = ingredient[ 2 ]
                ingredient_dict[ 'quantity' ] = ingredient[ 3 ]
                ingredient_dict[ 'unit' ] = ingredient[ 4 ]
                ingredient_dict[ 'selected_id' ] = ingredient[ 5 ]
                ret.append( ingredient_dict )

        return ret 

    #######################################################
    #                Get Shopping List
    #######################################################

    def get_shopping_list( self ):
        '''Returns a shopping list compatible with web_automater.py'''

        all_ingredients = []
        all_ingredients += self.get_all_selected_ingredients()
        all_ingredients += [ ingredient 
                             for recipe in self.get_all_selected_recipes()
                             for ingredient in self.get_ingredients_for_recipe( recipe[ 'recipe_id' ] ) ]

        shopping_list_dict = {}
        for ingredient in all_ingredients:
            if shopping_list_dict.get( ingredient[ 'id' ] ) is None:
                shopping_list_dict[ ingredient[ 'id' ] ] = ingredient[ 'quantity' ]
            else:
                shopping_list_dict[ ingredient[ 'id' ] ] += ingredient[ 'quantity' ]

        shopping_list = []
        for id, quantity in shopping_list_dict.items():
            db_ingredient = self.get_ingredient_by_id( id )

            shopping_item = Ingredient( db_ingredient[ 'search' ] )
            buy_quantity = int( db_ingredient[ 'quantity' ] // quantity )
            if db_ingredient[ 'quantity' ] % quantity > 0:
                quantity = quantity + 1
            shopping_item.add( buy_quantity )
            shopping_list.append( shopping_item )

        return shopping_list

# Temporary stuff and testing
if __name__ == '__main__':

    ingredients = Database().get_all_selected_ingredients()
    i = 1