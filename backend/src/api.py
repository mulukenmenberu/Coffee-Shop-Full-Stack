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
allowed_to_save_drink = requires_auth('post:drinks')
allowed_to_update_drink =  requires_auth('patch:drinks')
allowed_to_delete_drink =  requires_auth('delete:drinks')
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def drink_list():
    drinks = Drink.query.all()
    #dd = Drink.short(d)
   # print(d)
    short_recipe = []
    for drink in drinks:
        #print (x.recipe)
        short_recipe.append({           
             'id': drink.id,
            'title': drink.title,
            'recipe': json.loads(drink.recipe) 
            })
 
    return jsonify({"success": True, "drinks": short_recipe}),200

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
def drinks_details():
    drinks = Drink.query.all()
    #dd = Drink.short(d)
   # print(d)
    short_recipe = []
    for drink in drinks:
        print (drink.recipe)
        short_recipe.append({           
             'id': drink.id,
            'title': drink.title,
            'recipe': json.loads(drink.recipe) 
            })
 
    return jsonify({"success": True, "drinks": short_recipe}),200

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@allowed_to_save_drink
def save_drink(payload):
    drink_data = request.get_json(force=True)
    drink = Drink(
        title=str(drink_data['title']).replace("'", "\""),
        recipe=str(drink_data['recipe']).replace("'", "\"")
    )
    drink.insert()
    return jsonify({"success": True, "drinks":  drink_data}),200

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@allowed_to_update_drink
def update_drink(payload,id):
    drink_data = request.get_json(force=True)
    get_drink = Drink.query.get(id)
    if not get_drink:
        return jsonify({"success": False,"message":"Drink ID Not Found"}),404
    get_drink.title=str(drink_data['title']).replace("'", "\"")
    get_drink.recipe=str(drink_data['recipe']).replace("'", "\"")
    get_drink.update()
    return jsonify({"success": True, "drinks": "drink"}),200

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@allowed_to_delete_drink
def delete_drink(payload,id):
    drink = Drink.query.get(id)
    if  not drink:
        return jsonify({"message":"Drink not found"}), 404
    drink.delete()

    return jsonify({"success": True, "delete": id}), 200


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return (jsonify({'success': False, 'error': 404,
                        'message': 'resource not found'
                    }), 404)

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(401)
def auth_error(error):
    return AuthError({
            'code': 'authorization error',
            'description': 'Authorization error. please check the token provided is correct'
        }, 401)
if __name__ == '__main__':
    app.run(host='127.0.0.1',port='5000')
