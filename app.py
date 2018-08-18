# -*- coding: UTF-8 -*-
import os

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, static_url_path="")


DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/recipes.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100),nullable=False)
    making_time = db.Column(db.String(100),nullable=False)
    serves      = db.Column(db.String(100),nullable=False)
    ingredients = db.Column(db.String(300),nullable=False)
    cost        = db.Column(db.Integer,nullable=False)

    def __init__(self, title, making_time, serves, ingredients, cost):
        self.title       = title
        self.making_time = making_time
        self.serves      = serves
        self.ingredients = ingredients
        self.cost        = cost

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'making_time': self.making_time,
            'serves': self.serves,
            'ingredients': self.ingredients,
            'cost': self.cost
        }

@app.errorhandler(400)
def not_found(error):
    return make_response("", 400)

@app.errorhandler(404)
def not_found(error):
    return make_response("", 404)


@app.route('/', methods = ['GET'])
def app_root():
    return make_response( "", 200 );

@app.route('/recipes', methods = ['GET'])
def get_recipes():
    return make_response(jsonify({'recipes': list(map( lambda r: r.as_dict(),Recipe.query.all()))}), 200)

def answer_missing():
    return make_response(jsonify({'message': 'No Recipe found'}), 200)

def find_recipe(recipe_id):
    return Recipe.query.get(recipe_id)
    recipe = list(filter( lambda r: r['id'] == recipe_id, recipes))
    if len(recipe) == 0:
        return None
    print (recipe)
    return recipe[0]

@app.route('/recipes/<int:recipe_id>', methods = ['GET'])
def get_recipe(recipe_id):
    recipe = find_recipe(recipe_id)
    if recipe is None:
        return answer_missing()
    return make_response(jsonify( { 'message': 'Recipe details by id', 'recipe': recipe.as_dict() } ), 200);

@app.route('/recipes/<int:recipe_id>', methods = ['DELETE'])
def delete_recipe(recipe_id):
    recipe = find_recipe(recipe_id)
    if recipe is None:
        return answer_missing()
    db.session.delete(recipe)
    db.session.commit()
    return make_response(jsonify({ 'message': 'Recipe successfully removed!' }), 200)

def answer_bad_param():
    return make_response( jsonify({ 
        'message'  : 'Recipe creation failed!', 
        'required' : 'title, making_time, serves, ingredients, cost' 
    }), 200 )

def parse_recipe(input):
    #print(input)
    if not input:
        return None
    title, making_time, serves, ingredients, cost = input.split(',')
    
    #print("\n".join((title, making_time, serves, ingredients, cost)))
    if \
        title is None or \
        making_time is None or \
        serves is None or \
        ingredients is None or \
        cost is None:
            return None
    return title, making_time, serves, ingredients, int(cost)

@app.route('/recipes', methods = ['POST'])
def insert_recipe():
    global recipes_autoinc
    title, making_time, serves, ingredients, cost = parse_recipe( request.data.decode("utf-8") )
    if title is None:
        return answer_bad_param()
    recipe = Recipe(title,making_time,serves,ingredients,cost)
    db.session.add(recipe)
    db.session.commit()
    return make_response(jsonify({ 'message': 'Recipe successfully created!', 'recipe': recipe.as_dict() }), 200)

@app.route('/recipes/<int:recipe_id>', methods = ['PATCH'])
def update_recipe(recipe_id):
    recipe = find_recipe(recipe_id)
    if recipe is None:
        return answer_missing()
    title, making_time, serves, ingredients, cost = parse_recipe( request.data.decode("utf-8") )
    if title is None:
        return answer_bad_param()
    recipe.title = title
    recipe.making_time = making_time
    recipe.serves = serves
    recipe.ingredients = ingredients
    recipe.cost = cost

    db.session.commit()
    return make_response(jsonify({ 'message': 'Recipe successfully updated!', 'recipe': recipe.as_dict() }), 200)
    
