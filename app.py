# -*- coding: UTF-8 -*-

from flask import Flask, jsonify, abort, request, make_response, url_for


app = Flask(__name__, static_url_path="")

@app.errorhandler(400)
def not_found(error):
    return make_response("", 400)

@app.errorhandler(404)
def not_found(error):
    return make_response("", 404)

recipes = []
recipes_autoinc = 0


@app.route('/', methods = ['GET'])
def app_root():
    return make_response( "", 200 );

@app.route('/recipes', methods = ['GET'])
def get_recipes():
    return make_response(jsonify({'recipes': recipes}), 200)

def answer_missing():
    return make_response(jsonify({'message': 'No Recipe found'}), 200)

def find_recipe(recipe_id):
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
    return make_response(jsonify( { 'message': 'Recipe details by id', 'recipe': recipe } ), 200);

@app.route('/recipes/<int:recipe_id>', methods = ['DELETE'])
def delete_recipe(recipe_id):
    recipe = find_recipe(recipe_id)
    if recipe is None:
        return answer_missing()
    recipes.remove(recipe)
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
    return title, making_time, serves, ingredients, cost

@app.route('/recipes', methods = ['POST'])
def insert_recipe():
    global recipes_autoinc
    title, making_time, serves, ingredients, cost = parse_recipe( request.data.decode("utf-8") )
    if title is None:
        return answer_bad_param()
    recipe = {
        'id': recipes_autoinc,
        'title': title,
        'making_time': making_time,
        'serves': serves,
        'ingredients': ingredients,
        'cost' : cost
    }
    recipes.append(recipe)
    recipes_autoinc = recipes_autoinc + 1
    return make_response(jsonify({ 'message': 'Recipe successfully created!', 'recipe': recipe }), 200)

@app.route('/recipes/<int:recipe_id>', methods = ['PATCH'])
def update_recipe(recipe_id):
    recipe = find_recipe(recipe_id)
    title, making_time, serves, ingredients, cost = parse_recipe( request.data )
    if title is None:
        return answer_bad_param()
    recipe.title = title
    recipe.making_time = making_time
    recipe.serves = serves
    recipe.ingredients = ingredients
    recipe.cost = cost
    return make_response(jsonify({ 'message': 'Recipe successfully updated!', 'recipe': recipe }), 200)
    
