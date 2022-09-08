import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# this will check is the user has access to the requested resource or not

allowed_to_save_drink = requires_auth('post:drinks')
allowed_to_update_drink = requires_auth('patch:drinks')
allowed_to_delete_drink = requires_auth('delete:drinks')
allowed_to_see_drink_detail = requires_auth('get:drinks-detail')

db_drop_and_create_all()

# ROUTES

# Public URL:


@app.route('/drinks', methods=['GET'])
def drink_list():
    drinks = Drink.query.all()
    short_recipe = []
    for drink in drinks:
        short_recipe.append({
            'id': drink.id,
            'title': drink.title,
            'recipe': json.loads(drink.recipe)
        })

    return jsonify({"success": True, "drinks": short_recipe}), 200

# URL accessed by Manager and Birista


@app.route('/drinks-detail', methods=['GET'])
@allowed_to_see_drink_detail
def drinks_details(payload):
    drinks = Drink.query.all()
    long_recipe = []
    for drink in drinks:
        long_recipe.append({
            'id': drink.id,
            'title': drink.title,
            'recipe': json.loads(drink.recipe)
        })

    return jsonify({"success": True, "drinks": long_recipe}), 200

# URL accessed by Manager


@app.route('/drinks', methods=['POST'])
@allowed_to_save_drink
def save_drink(payload):
    try:
        drink_data = request.get_json(force=True)
    except:
        return jsonify({"success": False, "message": "invalid request, please check your inputs"}), 400
    if not drink_data['title']  or len(drink_data)<=0:
        return jsonify({"success": False, "message": "invalid request"}), 400
    drink = Drink(
        title=str(drink_data['title']).replace("'", "\""),
        recipe=str(drink_data['recipe']).replace("'", "\"")
    )
    try:
        drink.insert()
    except:
        return jsonify({"success": False, "message": "invalid request, please check your inputs"}), 400
    drink_long_reprentation = drink.long()
    return jsonify({"success": True, "drinks": [drink_long_reprentation]}), 200

# URL accessed by Manager


@app.route('/drinks/<int:id>', methods=['PATCH'])
@allowed_to_update_drink
def update_drink(payload, id):
    drink_data = request.get_json(force=True)
    get_drink = Drink.query.get(id)
    if not get_drink:
        return jsonify(
            {"success": False, "message": "Drink ID Not Found"}), 404
    get_drink.title = str(drink_data['title']).replace("'", "\"")
    get_drink.recipe = str(drink_data['recipe']).replace("'", "\"")
    get_drink.update()
    drink_long_reprentation = get_drink.long()
    return jsonify({"success": True, "drinks": [drink_long_reprentation]}), 200

# URL accessed by Manager


@app.route('/drinks/<int:id>', methods=['DELETE'])
@allowed_to_delete_drink
def delete_drink(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        return jsonify({"message": "Drink not found"}), 404
    drink.delete()

    return jsonify({"success": True, "delete": id}), 200


# Error Handling for unprocessable entity

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


# Error Handling for resource not found
@app.errorhandler(404)
def not_found(error):
    return (jsonify({'success': False, 'error': 404,
                     'message': 'resource not found'
                     }), 404)


# Error Handling for unauthorized access
@app.errorhandler(401)
def auth_error(error):
    return AuthError({
        'code': 'authorization error',
        'description': 'Authorization error. please check the token provided is correct'
    }, 401)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')
