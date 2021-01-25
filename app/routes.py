from flask import Flask
from flask import render_template
import sqlite3
from sqlite3 import Error
from app import app
from lib.database import Database

@app.route('/')
@app.route('/index')
def index():

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

    return render_template('index.html', ingredients=ingredients)
