from flask import Flask
from flask import render_template
import sqlite3
from sqlite3 import Error
from app import app
from lib.database import Database

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/ingredients')
def ingredients():

    database = Database()
    database_ingredients = database.select_all_ingredients()
    ingredients = []

    for ingredient in database_ingredients:
        row = {}
        row['name'] = ingredient[1]
        row['search'] = ingredient[2]
        row['quantity'] = ingredient[3]
        row['unit'] = ingredient[4]
        ingredients.append(row)

    return render_template('ingredient_list.html', ingredients=ingredients)

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

    return render_template('recipe_list.html', recipes=recipes)

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

    return render_template('recipe.html', ingredients=ingredients)
