from flask_restx import Api
from .fuzzy_api import api as fuzzy

api = Api(
    title='API de Processamento de Gatos',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(fuzzy, path='/fuzzy')
