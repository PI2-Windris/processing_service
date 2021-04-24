from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
import requests
import os
import json
import core.helper as helper
from datetime import datetime, timedelta


api = Namespace('efficiency_system',
                description='Efficiency system related calculations')
parser = reqparse.RequestParser()
parser.add_argument('begin', type=str, help='Time that begins')
parser.add_argument('end', type=str, help='Time that ends')
parser.add_argument('format', type=str, help='Format of the time')


@api.route('/<string:id>')
class SystemEfficiency(Resource):
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
        eps = 0
        epe = 0
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

            epe += abs(int(energy["averageInputTension"])) * \
                abs(int(energy["averageOutputTension"]))
            eps += abs(int(energy["averageOutputTension"])) * \
                abs(int(energy["averageOutputCurrent"]))

            efficiency = eps / epe
            efficiency = f'{efficiency}'
            efficiency_per_time.append(
                {"SystemEfficiency": efficiency, "time": helper.date_to_str(energy["createdAt"])})
            i = i + 1

        if not i or not epe:
            return {"average": 0, "efficiencyPerTime": []}
        average_energy = (eps/i) / (epe/i)
        return {"average": average_energy, "efficiencyPerTime": efficiency_per_time}
