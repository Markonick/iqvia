import pytest
import os
import json
import datetime
from unittest.mock import Mock, patch

# GETs
def test_get_response_is_200(client, init_database):
    response = client.get('/api/v1/contacts/')
    assert response.status_code == 200

def test_get_response_returns_expected_contacts(client, init_database):
    response = client.get('/api/v1/contacts/')
    json_data = json.loads(response.data)

    assert len(json_data['body']) == 2
    assert json_data['body'][0]['username'] == 'nicomark'
    assert json_data['body'][0]['first_name'] == 'Nicolas'
    assert json_data['body'][0]['last_name'] == 'Markos'
    assert json_data['body'][1]['username'] == 'speedster'
    assert json_data['body'][1]['first_name'] == 'Efi'
    assert json_data['body'][1]['last_name'] == 'Pappa'

def test_get_response_returns_expected_creation_dates(client, init_database):
    response = client.get('/api/v1/contacts/')
    json_data = json.loads(response.data)

    "2019-09-15 12:00:00"
    created = json_data['body'][0]['created']
    assert created == 'Sun, 15 Sep 2019 12:00:00 GMT'

def test_get_response_returns_expected_emails(client, init_database):
    response = client.get('/api/v1/contacts/')
    assert response.status_code == 200

    json_data = json.loads(response.data)

    assert json_data['body'][0]['emails'][0] == 'mark123@gmail.com'
    assert json_data['body'][0]['emails'][1] == 'nicomark66@hotmail.com'
    assert json_data['body'][1]['emails'][0] == 'fifi@gmail.com'

def test_that_we_get_contact_based_on_username(client, init_database):
    username = 'nicomark'
    response = client.get(f'/api/v1/contacts/{username}')
    json_data = json.loads(response.data)

    assert json_data['body']['username'] == 'nicomark'
    assert json_data['body']['first_name'] == 'Nicolas'
    assert json_data['body']['last_name'] == 'Markos'

def test_that_we_get_404_when_username_input_wrong(client, init_database):
    username = 'bicomark'
    response = client.get(f'/api/v1/contacts/{username}')
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data['status'] == 404

# PUTs
def test_that_we_update_contact_username_correctly_based_on_username(client, init_database):
    username = 'nicomark'
    body = create_contact_json()
    headers = {'Content-Type': 'application/json'}
    response = client.put(f'/api/v1/contacts/{username}', data=json.dumps(body), headers=headers)
    json_data = json.loads(response.data)

    assert json_data['status'] == 200
    assert json_data['body']['username'] == 'boxer43'

def test_that_we_get_404_when_updating_with_non_existent_username(client, init_database):
    username = 'bicomark'
    body = create_contact_json()
    headers = {'Content-Type': 'application/json'}
    response = client.put(f'/api/v1/contacts/{username}', data=json.dumps(body), headers=headers)
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data['status'] == 404

def test_that_we_get_404_when_updating_with_body_missing_fields(client, init_database):
    username = 'nicomark'
    body = create_contact_missing_fields_json()
    headers = {'Content-Type': 'application/json'}
    response = client.put(f'/api/v1/contacts/{username}', data=json.dumps(body), headers=headers)
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data['status'] == 404
    assert json_data['body'] == ''

# POSTs
def test_that_when_we_create_a_contact_we_get_201(client, init_database):
    body = create_contact_json()
    headers = {'Content-Type': 'application/json'}
    response = client.post(f'/api/v1/contacts/', data=json.dumps(body), headers=headers)
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data['status'] == 201

def test_that_when_we_create_a_contact_we_have_one_more_contact_in_list(client, init_database):
    body = create_contact_json()
    headers = {'Content-Type': 'application/json'}
    response = client.post('/api/v1/contacts/', data=json.dumps(body), headers=headers)
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data['status'] == 201

    response = client.get('/api/v1/contacts/')
    json_data = json.loads(response.data)

    assert len(json_data['body']) == 3


def test_that_when_we_create_a_contact_fields_are_as_expected(client, init_database):
    body = create_contact_json()
    headers = {'Content-Type': 'application/json'}
    response = client.post('/api/v1/contacts/', data=json.dumps(body), headers=headers)
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data['status'] == 201

    response = client.get('/api/v1/contacts/boxer43')
    json_data = json.loads(response.data)

    assert json_data['body']['username'] == body['username']
    assert json_data['body']['first_name'] == body['first_name']
    assert json_data['body']['username'] == body['username']

# DELETEs
def test_that_we_delete_a_contact_successfully_based_on_username(client, init_database):
    response = client.delete('/api/v1/contacts/nicomark')
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data['status'] == 204

def test_that_when_we_delete_a_contact_successfully_list_length_is_updated_correctly(client, init_database):
    response = client.delete('/api/v1/contacts/nicomark')
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data['status'] == 204

    response = client.get('/api/v1/contacts/')
    json_data = json.loads(response.data)

    assert len(json_data['body']) == 1

def test_that_when_we_delete_a_contact_successfully_if_older_than_one_minute(client, init_database):
    """
    1) Create a contact with time now. This should add to the other 2 contacts 
       that have time frozen to older than a minute in our fixture.
    2) Make a Delete call, should delete the 2 initial contacts
    """
    # 1 - CREATE NEW CONTACT
    body = create_contact_json()
    headers = {'Content-Type': 'application/json'}
    response = client.post('/api/v1/contacts/', data=json.dumps(body), headers=headers)
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data['status'] == 201

    # CHECK CHANGES
    response = client.get('/api/v1/contacts/')
    json_data = json.loads(response.data)
    assert len(json_data['body']) == 3

    # # 2 - DELETE CONTACTS OLDER THAN 1 MINUTE
    params = {'older_than': 60}
    headers = {'Content-Type': 'application/json'}
    response = client.delete('/api/v1/contacts?older_than=60', headers=headers)
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data['status'] == 204

    response = client.get('/api/v1/contacts/')
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data['status'] == 200
    assert len(json_data['body']) == 1

def create_contact_json():
    body = {
      "emails": [
        "galisnik@gmail.com",
        "arianara@hotmail.com"
      ],
      "first_name": "Nick",
      "last_name": "Galis",
      "username": "boxer43"
    }

    return body

def create_contact_missing_fields_json():
    body = {
      "emails": [
        "galisnik@gmail.com",
        "arianara@hotmail.com"
      ],
      "username": "boxer43"
    }

    return body