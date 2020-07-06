from flask import Blueprint, Response, request
from bson.json_util import dumps

from config import db

messages_routes = Blueprint('messages', __name__, url_prefix = '/messages')

@messages_routes.route('')
def getMessages():
    return 'Messages list'

@messages_routes.route('', methods = ['POST'])
def updateMessages():
    try:
        message = request.get_json()      
        if message['group_name']:
            group = db.groups.find({'name': message['group_name']})
            for member in group[0]['members']:
                db.users.update(
                    {
                        'email': member['email']
                    },
                    {
                        '$push': {
                            'messages': {
                                'email': member['email'],
                                'message': message['text']
                            }
                        }
                    })
        
            response = {
                'message': 'The messages has been added successfully!'
            }      
            return Response(
                dumps(response),
                status = 200,
                content_type = 'application/json'
            )
        else:            
            user = db.users.find_one({'email': message['user']})
            if user:
                db.users.update_one(
                    {
                        'email': user['email']
                    },
                    {
                        '$push': {
                            'messages': {
                                'email':  user['email'],
                                'message': message['text']
                            }
                        }
                    }
                )
            
                response = {
                    'message': 'The messages has been added successfully!'
                }      
                return Response(
                    dumps(response),
                    status = 200,
                    content_type = 'application/json'
                )
            else:
                response = {
                    'message': 'User %s not found!' % (message['user'])  
                }      
                return Response(
                    dumps(response),
                    status = 404,
                    content_type = 'application/json'
                )

    except Exception as error:
        return 'Error: %s' % (error)