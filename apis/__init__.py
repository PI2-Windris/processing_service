from flask_restx import Api
from .fuzzy_api import api as fuzzy
from .energy_produced_api import api as energy
from .efficiency_inversor_api import api as inversor_efficiency

api = Api(
    title='API de Processamento de Gatos',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(fuzzy, path='/catatau')
api.add_namespace(energy, path='/produced')
api.add_namespace(inversor_efficiency, path="/inversor")