import json
import typing
import os
import logging
from flask import request, jsonify
from flask_restplus import Resource, Namespace

from app.factories import (
    create_contact_list_service,
    create_contact_service,
)

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger('API')

api = Namespace('contacts', description='Contact related operations')


@api.route("/contacts", strict_slashes=False)
class ContactList(Resource):
    """
    Endpoint that returns a serialised ordered list of contact items
    """
    def get(self):
        svc = create_contact_list_service()
        contact_list = svc.get_contact_list()
        body = []

        for contact in contact_list:
            emails = [email.address for email in contact.emails]
            contact = {
                'username': contact.username,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'emails': emails,
                'created': contact.created
            }
            body.append(contact)

        result = \
        {
            "status": 200, 
            "message": f"Found {len(contact_list)} contact items!",
            "body": body,
        }
        
        return jsonify(result)

    def post(self):
        # Read body fields
        body = request.get_json()
        username = body.get("username")
        first_name = body.get("first_name")
        last_name = body.get("last_name")
        emails = body.get("emails")

        # Instantiate service from factory
        svc = create_contact_list_service()

        # Create contact
        contact = svc.create_contact(username, first_name, last_name, emails)

        if contact:
            result = \
            {
                "status": 201, 
                "message": f"Created contact successfully!",
            }
        else:
            result = \
            {
                "status": 500, 
                "message": f"contact creation unsuccessful!",
            }
        
        return jsonify(result)


@api.route("/contacts/", defaults={'username': None}, strict_slashes=False)
@api.route("/contacts/<string:username>", strict_slashes=False)
class ContactItem(Resource):
    """
    Endpoint that handles a serialised item
    """
    def get(self, username):
        svc = create_contact_service()
        contact = svc.get_contact(username)

        if contact:
            emails = [email.address for email in contact.emails]
            body = {
                'username': contact.username,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'emails': emails,
                'created': contact.created
            }
            result = \
            {
                "status": 200, 
                "message": f"Found contact item!",
                "body": body
            }
        else:
            result = \
            {
                "status": 404, 
                "message": f"contact item not found!",
            }
        
        return jsonify(result)

    def put(self, username):
        # Read body fields
        body = request.get_json()
        new_username = body.get("username")
        first_name = body.get("first_name")
        last_name = body.get("last_name")
        emails = body.get("emails")

        # Instantiate service from factory
        svc = create_contact_service()

        # Modify contact if exists
        contact = svc.update_contact(username, new_username, first_name, last_name, emails)
        
        # If contact doesnt exist return error
        if not contact:
            result = \
            {
                "status": 404, 
                "message": f"contact item not found!",
                "body": ''
            }
        
            return jsonify(result)

        emails = [email.address for email in contact.emails]
        body = {
            'username': contact.username,
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'emails': emails,
            'created': contact.created
        }
        
        result = \
        {
            "status": 200, 
            "message": f"Updated contact item!",
            "body": body
        }
        
        return jsonify(result)

    def delete(self, username):
        svc = create_contact_service()
    
        # Get query params
        logger.debug(f'IN DELETE API BEFORE OLDER!!!!!!!')
        older_than = request.args.get("older_than")
        logger.debug(f'OLDER THAN: {older_than}')
        contact_deleted = svc.delete_contact(username, older_than)

        if contact_deleted:
            result = \
            {
                "status": 204, 
                "message": f"Deleted contact item!",
            }
        else:
            result = \
            {
                "status": 404, 
                "message": f"contact item not deleted!",
            }
        
        return jsonify(result)