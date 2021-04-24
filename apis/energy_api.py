from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
import requests
import os
import json
from datetime import datetime, timedelta
import core.helper as helper

api = Namespace('average', description='Average related calculations')

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

        average_tension = 0
        average_current = 0
        average_supply = 0
        i = 0
        sorted(res_json["energyData"],
               key=lambda i: helper.str_to_date(i["createdAt"]))

        for energy in res_json["energyData"]:
            energy["createdAt"] = helper.str_to_date(energy["createdAt"])
            if(energy["createdAt"] < begin):
                continue

            if(energy["createdAt"] > end):
                break
            average_tension += int(energy["averageOutputTension"])
            average_current += int(energy["averageOutputCurrent"])
            average_supply += int(energy["averageSupply"])
            i = i + 1

        if not i:
            return {"averageEnergy": 0, "energyPerTime": []}

        average_tension /= i
        average_current /= i
        average_supply /= i
        average_potency = 0
        if average_current:
            average_potency = average_tension / average_current

        return {"averageTension": average_tension, "averageCurrent": average_current, "averagePotency": average_potency, "averageSupply": average_supply}
