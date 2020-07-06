from flask import Blueprint, Response, request
from bson.json_util import dumps

from config import db

users_routes = Blueprint('users', __name__, url_prefix = '/users')

@users_routes.route('')
def getUsers():
    try:      
        users = db.users.find()
        
        return Response(
            dumps(users),
            status = 200,
            content_type = 'application/json'
        )
    except Exception as error:
        return 'Error: %s' % (error)

@users_routes.route('', methods = ['POST'])
def postUser():
    try:
        user = request.get_json()
        db.users.insert_one(
            {
                'name': user['name'],
                'email': user['email'],
                'messages': []
            }
        )

        response = {
            'message': 'User %s added successfully!' % (user['name'])
        }
        
        return Response(
            dumps(response),
            status = 201,
            content_type = 'application/json'
        )

    except Exception as error:
        return 'Error: %s' % (error)

@users_routes.route('', methods = ['PATCH'])
def updateUser():
    try:
        user = request.get_json()
        updated = db.users.update_one(
            {'email': user['email']},
            {'$set': user} )

        if updated.modified_count:
            response = {
                'message': 'User %s updated successfully!' % (user['name']) 
            }       
            return Response(
                dumps(response),
                status = 200,
                content_type = 'application/json'
            )
        if updated.matched_count:
            response = {
                'message': 'User %s found, but not modified!' % (user['name'])   
            }     
            return Response(
                dumps(response),
                status = 400,
                content_type = 'application/json'
            )
        else:
            response = {
                'message': 'User %s not found!' % (user['name'])  
            }      
            return Response(
                dumps(response),
                status = 404,
                content_type = 'application/json'
            )
        

    except Exception as error:
        return 'Error: %s' % (error)

@users_routes.route('', methods = ['DELETE'])
def deleteUser():
    try:
        user = request.get_json()
        deleted = db.users.delete_one(
            {
                'email': user['email']
            }
        )
        
        if deleted.deleted_count:
            response = {
                'message': 'User %s deleted successfully!' % (user['email'])
            }
            return Response(
                dumps(response),
                status = 200,
                content_type = 'application/json'
            )
        else:
            response = {
                'message': 'User %s has not been deleted!' % (user['email'])
            }
            return Response(
                dumps(response),
                status = 404,
                content_type = 'application/json'
            )

    except Exception as error:
        return 'Error: %s' % (error)
