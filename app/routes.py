from flask import Flask
from flask import render_template, redirect, url_for
from app import app
from lib.database import Database
from app.forms import new_ingredient_form
import os

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route( '/' )
@app.route( '/index' )
def index():
    return render_template('index.html')

@app.route( '/ingredients', methods=['GET', 'POST'] )
def ingredients():

    database = Database()
    form = new_ingredient_form()
    
    if form.validate_on_submit():
        database.add_ingredient( form.data['name'], form.data['search'], form.data['quantity'], form.data['unit'] )
        return redirect( '/ingredients' )
    
    database_ingredients = database.select_all_ingredients()
    ingredients = []

    for ingredient in database_ingredients:
        row = {}
        row['name'] = ingredient[1]
        row['search'] = ingredient[2]
        row['quantity'] = ingredient[3]
        row['unit'] = ingredient[4]
        ingredients.append(row)
    
    return render_template( 'ingredient_list.html', title='Ingredients', ingredients=ingredients, form=form )

@app.route('/recipes')
def recipes():

    database = Database()
    database_recipes = database.get_all_recipes()
    recipes = []

    for database_recipe in database_recipes:
        row = {}
        row['id'] = database_recipe[0]
        row['name'] = database_recipe[1]
        recipes.append(row)

    return render_template( 'recipe_list.html', recipes=recipes )

@app.route('/recipe_id=<id>')
def recipe_id(id):
    database = Database()
    database_ingredients = database.get_items_for_recipe( id )
    ingredients = []

    for ingredient in database_ingredients:
        row = {}
        row['name'] = ingredient[0]
        row['quantity'] = ingredient[1]
        row['unit'] = ingredient[2]
        ingredients.append(row)

    return render_template( 'recipe.html', ingredients=ingredients )
