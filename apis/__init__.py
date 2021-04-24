from flask_restx import Api
from .fuzzy_api import api as fuzzy
from .energy_produced_api import api as energy
api = Api(
    title='API de Processamento de Gatos',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(fuzzy, path='/catatau')
api.add_namespace(energy, path='/produced')