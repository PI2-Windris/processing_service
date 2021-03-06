from flask_restx import Api
from .fuzzy_api import api as fuzzy
from .energy_produced_api import api as energy_produce
from .efficiency_inversor_api import api as inversor_efficiency
from .efficiency_system_api import api as system_efficiency
from .co_api import api as co
from .energy_api import api as energy
from .climate_api import api as climate

api = Api(
    title='API de Processamento de Gatos',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(fuzzy, path='/fuzzy')
api.add_namespace(energy_produce, path='/produced')
api.add_namespace(inversor_efficiency, path="/inversor")
api.add_namespace(system_efficiency, path="/efficiency")
api.add_namespace(co, path="/co")
api.add_namespace(energy, path="/energy")
api.add_namespace(climate, path="/climate")
