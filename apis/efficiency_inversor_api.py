from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
import requests
import os
import json
import core.helper as helper
from datetime import datetime, timedelta


api = Namespace('efficiency_inversor',
                description='Efficiency inversor related calculations')
parser = reqparse.RequestParser()
parser.add_argument('begin', type=str, help='Time that begins')
parser.add_argument('end', type=str, help='Time that ends')
parser.add_argument('format', type=str, help='Format of the time')


@api.route('/<string:id>')
class InversorEfficiency(Resource):
    def get(self, id):
        args = parser.parse_args()
        headers = {"authorization": request.headers.get('authorization')}
        begin = datetime.now()
        end = datetime.now() - timedelta(days=1)

        if(args["begin"] is not None):
            begin = helper.str_to_date(args["begin"], "%Y-%m-%dT%H:%M:%S")

        if(args["end"] is not None):
            end = helper.str_to_date(args["end"], "%Y-%m-%dT%H:%M:%S")

        res_json = helper.get_generator_energy(id, headers)
        average_input_tension = 0
        average_output_tension = 0
        efficiency_per_time = []
        i = 0
        sorted(res_json["energyData"],
               key=lambda i: helper.str_to_date(i["createdAt"]))

        for energy in res_json["energyData"]:
            energy["createdAt"] = helper.str_to_date(energy["createdAt"])
            if(energy["createdAt"] < begin):
                continue

            if(energy["createdAt"] > end):
                break

            average_input_tension += abs(int(energy["averageInputTension"]))
            average_output_tension += abs(int(energy["averageOutputTension"]))

            efficiency = int(energy["averageInputTension"]) / abs(int(energy["averageOutputTension"]))
            efficiency = f'{efficiency}'
            efficiency_per_time.append(
                {"inversorEfficiency": efficiency, "time": helper.date_to_str(energy["createdAt"])})
            i = i + 1

        if not i or not average_output_tension:
            return {"average": 0, "efficiencyPerTime": []}
        average_energy = (average_input_tension/i) / (average_output_tension/i)
        return {"average": average_energy, "efficiencyPerTime": efficiency_per_time}
