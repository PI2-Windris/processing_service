from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
import requests
import os
import json
from datetime import datetime, timedelta
import core.helper as helper

api = Namespace('energy', description='Energy related calculations')

parser = reqparse.RequestParser()
parser.add_argument('begin', type=str, help='Time that begins')
parser.add_argument('end', type=str, help='Time that ends')
parser.add_argument('format', type=str, help='Format of the time')

STORAGE_URI = os.environ.get('DATA_STORAGE_HOST')
STORAGE_PORT = os.environ.get('DATA_STORAGE_PORT')


@api.route('/<string:id>')
class EnergyCalculation(Resource):
    def get(self, id):
        headers = {"authorization": request.headers.get('authorization')}
        args = parser.parse_args()
        res_json = helper.get_generator_energy(id, headers)
        begin = datetime.now()
        end = datetime.now() - timedelta(days=1)
        if(args["begin"] is not None):
            begin = helper.str_to_date(args["begin"], "%Y-%m-%dT%H:%M:%S")

        if(args["end"] is not None):
            end = helper.str_to_date(args["end"], "%Y-%m-%dT%H:%M:%S")

        energy_tension = 0
        energy_current = 0
        energy_per_time = []
        i = 0
        sorted(res_json["energyData"],
               key=lambda i: helper.str_to_date(i["createdAt"]))

        for energy in res_json["energyData"]:
            energy["createdAt"] = helper.str_to_date(energy["createdAt"])
            if(energy["createdAt"] < begin):
                continue

            if(energy["createdAt"] > end):
                break

            energy_tension += int(energy["averageOutputTension"])
            energy_current += abs(int(energy["averageOutputCurrent"]))

            produce = int(energy["averageOutputTension"]) * \
                abs(int(energy["averageOutputCurrent"]))
            energy_per_time.append(
                {"energyProduced": produce, "time": helper.date_to_str(energy["createdAt"])})
            i = i + 1
        if not i:
            return {"averageEnergy": 0, "energyPerTime": []}

        average_energy = (energy_tension/i) * (energy_current/i)
        return {"averageEnergy": average_energy, "energyPerTime": energy_per_time}
