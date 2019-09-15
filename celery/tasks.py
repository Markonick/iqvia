import json
import os
import requests
from datetime import datetime
import random
import string
import logging
from celery import Celery

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger('CELERY-TASKS')

# Get env vars
endpoint = os.environ.get('CONTACTS_ENDPOINT')
broker = os.environ.get('CELERY_BROKER_URL')
backend = os.environ.get('CELERY_RESULT_BACKEND')

celery = Celery(broker=broker, backend=backend)

# Add periodic tasks to scheduler
@celery.on_after_configure.connect
def add_periodic_task(sender, **kwargs):
    sender.add_periodic_task(15.0, create_contact, name='Create contact every 15 sec')
    sender.add_periodic_task(60.0, remove_contact, name='Remove contact every 60 sec')

@celery.task
def create_contact():
    logger.info(f'CREATE CONTACT - Before call!!!! ENDPOINT: {endpoint}')
    headers = {'Content-Type': 'application/json'}
    data = create_random_data()
    data_json = json.dumps(data)
    logger.debug(f'DATA: {data}')
    response = requests.post(endpoint, data=data_json, headers=headers)

@celery.task
def remove_contact():
    logger.info(f'REMOVE CONTACT - Before call!!!!')
    headers = {'Content-Type': 'application/json'}
    params = {'older_than': 60}
    response = requests.delete(endpoint, params=params, headers=headers)
    if response:
        logger.info(f'REMOVE CONTACT - Response is not None: {response}')

def create_random_data():
    number_of_emails = random.randint(1, 5)

    emails = [create_random_email_address() for i in range(number_of_emails)]

    random_contact_item = {
        'username': create_random_string_and_digits(),
        'first_name': create_random_string(),
        'last_name': create_random_string(),
        'emails': emails,
        'created': str(datetime.utcnow())
    }

    return random_contact_item

def create_random_email_address():
    return f'{create_random_string()}@{create_random_string()}.com'

def create_random_string_and_digits():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5,20)))

def create_random_string():
    return ''.join(random.choices(string.ascii_letters, k=random.randint(5,20)))