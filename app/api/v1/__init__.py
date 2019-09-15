from flask_restplus import Api

from .views import api as ns1

api = Api(
    title='Contacts API',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(ns1, path='/api/v1')