from flask import Flask
from flask import render_template, redirect, url_for
from app import app
from lib.database import Database
from app.forms import new_ingredient_form, delete_ingredient_form, add_to_recipe_form, new_selected_ingredient_form
import os

'''
These 2 functions are copied from stack overflow
This helps CSS update for new changes as a workaround
for browser caching
'''
@app.context_processor
def override_url_for():
    return dict( url_for=dated_url_for )

def dated_url_for( endpoint, **values ):
    if endpoint == 'static':
        filename = values.get( 'filename', None )
        if filename:
            file_path = os.path.join( app.root_path, endpoint, filename )
            values['q'] = int( os.stat( file_path ).st_mtime )
    return url_for( endpoint, **values )

@app.route( '/', methods=['GET', 'POST'] )
@app.route( '/index', methods=['GET', 'POST'] )
def index():

    # Add ingredient
    new_ingredient = new_selected_ingredient_form()
    new_ingredient.select.choices = [ ( 0, '- Select Ingredient -' ) ] + Database().get_all_ingredient_names()
    
    if new_ingredient.validate_on_submit():

        Database().add_selected_ingredient(
            int( new_ingredient.data[ 'select' ] ),
            new_ingredient.data[ 'quantity' ],
            new_ingredient.data[ 'unit' ] )
            
        return redirect( '/index' )

    # Delete an ingredient
    delete = delete_ingredient_form()    

    # Grab ingredients from database
    ingredients = Database().get_all_selected_ingredients()

    return render_template( 'index.html', new_ingredient=new_ingredient, ingredients=ingredients, delete=delete )

@app.route( '/ingredients', methods=['GET', 'POST'] )
def ingredients():

    form = new_ingredient_form()
    delete = delete_ingredient_form()

    if form.validate_on_submit():
        Database().add_ingredient( form.data['name'], form.data['search'], form.data['quantity'], form.data['unit'] )
        return redirect( '/ingredients' )
    
    database_ingredients = Database().get_all_ingredients()
    ingredients = []

    for ingredient in database_ingredients:
        row = {}
        row['id'] = ingredient[0]
        row['name'] = ingredient[1]
        row['search'] = ingredient[2]
        row['quantity'] = ingredient[3]
        row['unit'] = ingredient[4]
        ingredients.append(row)
    
    return render_template( 'ingredient_list.html', title='Ingredients', ingredients=ingredients, form=form, delete=delete )

@app.route( '/delete_ingredient/id/<id>', methods=['POST'] )
def delete_ingredient( id ):
    
    Database().delete_ingredient_by_id( id )
    
    return redirect( '/ingredients' )

@app.route( '/delete_selected_ingredient/id/<id>', methods=['POST'] )
def delete_selected_ingredient( id ):
    
    Database().delete_selected_ingredient( id )
    
    return redirect( '/index' )

@app.route( '/delete_recipe_item_id=<id>,recipe=<recipe_id>', methods=['POST'] )
def delete_recipe_item( id, recipe_id ):
    
    Database().delete_recipe_item_by_id( id )
    
    return redirect( '/recipe/id/{}'.format( recipe_id ) )

@app.route('/recipes')
def recipes():

    database_recipes = Database().get_all_recipes()
    recipes = []

    for database_recipe in database_recipes:
        row = {}
        row['id'] = database_recipe[0]
        row['name'] = database_recipe[1]
        recipes.append(row)

    return render_template( 'recipe_list.html', title='Recipes', recipes=recipes )

@app.route( '/recipe/id/<id>', methods=['GET', 'POST'] )
def recipe_id( id ):

    delete = delete_ingredient_form()
    delete.recipe_id.label = id

    # Get all ingredients
    form = add_to_recipe_form()
    form.select.choices = [ ( 0, '- Select Ingredient -' ) ] + Database().get_all_ingredient_names()
    if form.validate_on_submit():
        Database().add_recipe_item( id, int( form.data['select'] ), form.data['quantity'], form.data['unit'] )
        return redirect( '/recipe/id/{}'.format( id ) ) 

    # Get ingredients for the recipe
    database_ingredients = database.get_items_for_recipe( id )
    ingredients = []
    delete_fields = []

    for ingredient in database_ingredients:
        row = {}
        row['name'] = ingredient[0]
        row['quantity'] = ingredient[1]
        row['unit'] = ingredient[2]
        row['id'] = ingredient[3]
        ingredients.append(row)

    title = Database().get_recipe_name( id )

    return render_template( 'recipe.html', title=title, ingredients=ingredients, new_ingredient=form, delete=delete )
    