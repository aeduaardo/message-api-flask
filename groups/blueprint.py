from flask import Blueprint, Response, request
from bson.json_util import dumps

from config import db

groups_routes = Blueprint('groups', __name__, url_prefix = '/groups')


@groups_routes.route('')
def getGroups():
    try:      
        groups = db.groups.find()
        
        return Response(
            dumps(groups),
            status = 200,
            content_type = 'application/json'
        )
    except Exception as error:
        return 'Error: %s' % (error)

@groups_routes.route('', methods = ['POST'])
def postGroup():
    members = []
    try:
        group = request.get_json()

        for member in group['members']:
            user = db.users.find_one(member)

            if not user:
                members.append(member)
                group['members'].remove(member)

        db.groups.insert_one(
            {
                'name': group['name'],
                'members': group['members']
            }
        )

        response = {
            'message': 'Group %s created successfully!' % (group['name']),
            'nonexistent_members': members
            }
                
        return Response(
            dumps(response),
            status = 201,
            content_type = 'application/json'
        )

    except Exception as error:
        return 'Error: %s' % (error)

@groups_routes.route('', methods = ['PATCH'])
def changeName():
    try:
        group = request.get_json()
        updated = db.groups.update_one(
            {
                'name': group['name']
            },
            {'$set': {
                'name': group['new_name']
                }
            } 
            )

        if updated.modified_count:
            response = {
                'message': 'Name changed successfully!'
            }       
            return Response(
                dumps(response),
                status = 200,
                content_type = 'application/json'
            )
        if updated.matched_count:
            response = {
                'message': 'Group %s found, but not modified!' % (group['name'])   
            }     
            return Response(
                dumps(response),
                status = 400,
                content_type = 'application/json'
            )
        else:
            response = {
                'message': 'Group %s not found!' % (group['name'])  
            }      
            return Response(
                dumps(response),
                status = 404,
                content_type = 'application/json'
            )
        

    except Exception as error:
        return 'Error: %s' % (error)

@groups_routes.route('/insert', methods = ['PATCH'])
def insert_member():
    try:                    
        group = request.get_json()
        user = db.users.find_one({'email': group['member']})
        if user:
            user = db.groups.find_one({"name": group['name'], "members": {"email": group['member']}})
            if user:
                response = {
                    'message': 'The user %s is already part of the group.' % (group['member'])  
                }      
                return Response(
                    dumps(response),
                    status = 200,
                    content_type = 'application/json'
                )
            else:
                inserted = db.groups.update_one(
                    {
                        'name': group['name']
                    },
                    {'$push': {
                        'members': {
                            'email': group['member']
                        }
                        }
                    } 
                    )

                if inserted.modified_count:
                    response = {
                        'message': 'User %s added successfully!' % (group['member'])
                    }       
                    return Response(
                        dumps(response),
                        status = 200,
                        content_type = 'application/json'
                    )
                if inserted.matched_count:
                    response = {
                        'message': 'Group %s found, but not modified!' % (group['name'])   
                    }     
                    return Response(
                        dumps(response),
                        status = 400,
                        content_type = 'application/json'
                    )
                else:
                    response = {
                        'message': 'Group %s not found!' % (group['name'])  
                    }      
                    return Response(
                        dumps(response),
                        status = 404,
                        content_type = 'application/json'
                    )

        else:
            response = {
                'message': 'User %s not found!' % (group['member'])  
            }      
            return Response(
                dumps(response),
                status = 404,
                content_type = 'application/json'
            )

    except Exception as error:
        return 'Error: %s' % (error)

@groups_routes.route('/remove', methods = ['PATCH'])
def remove_member():
    try:                    
        group = request.get_json()
        user = db.groups.find_one({"name": group['name'], "members": {"email": group['member']}})
        if user:
            removed = db.groups.update_one(
                {
                    'name': group['name']
                },
                {
                    '$pull': {
                        'members': {
                                    'email': group['member']
                             }
                    }
                } 
                )

            if removed.modified_count:
                response = {
                    'message': 'User %s deleted successfully!' % (group['member'])
                }       
                return Response(
                    dumps(response),
                    status = 200,
                    content_type = 'application/json'
                )
            if removed.matched_count:
                response = {
                    'message': 'Group %s found, but user has not been removed!' % (group['name'])   
                }     
                return Response(
                    dumps(response),
                    status = 400,
                    content_type = 'application/json'
                )
            else:
                response = {
                    'message': 'Group %s not found!' % (group['name'])  
                }      
                return Response(
                    dumps(response),
                    status = 404,
                    content_type = 'application/json'
                )
        else:
            response = {
                'message': 'User %s not found in the group %s!' % (group['member'], group['name'])  
            }      
            return Response(
                dumps(response),
                status = 404,
                content_type = 'application/json'
            )

    except Exception as error:
        return 'Error: %s' % (error)

@groups_routes.route('', methods = ['DELETE'])
def deleteGroup():
    try:
        group = request.get_json()
        deleted = db.groups.delete_one(
            {
                'name': group['name']
            }
        )
        
        if deleted.deleted_count:
            response = {
                'message': 'Group %s deleted successfully!' % (group['name'])
            }
            return Response(
                dumps(response),
                status = 200,
                content_type = 'application/json'
            )
        else:
            response = {
                'message': 'Group %s has not been deleted!' % (group['name'])
            }
            return Response(
                dumps(response),
                status = 404,
                content_type = 'application/json'
            )

    except Exception as error:
        return 'Error: %s' % (error)
