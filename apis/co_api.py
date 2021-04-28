from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
import requests
import os
import json
import core.helper as helper
from datetime import datetime, timedelta


api = Namespace('co_per_time',
                description='Co2 per time related calculations')
parser = reqparse.RequestParser()
parser.add_argument('begin', type=str, help='Time that begins')
parser.add_argument('end', type=str, help='Time that ends')
parser.add_argument('format', type=str, help='Format of the time')


@api.route('/<string:id>')
class CoPerTime(Resource):
    def get(self, id):
        args = parser.parse_args()
        headers = {"authorization": request.headers.get('authorization')}
        begin = datetime.now() - timedelta(days=1)
        end = datetime.now()

        if(args["begin"] is not None):
            begin = helper.str_to_date(args["begin"], "%Y-%m-%dT%H:%M:%S")

        if(args["end"] is not None):
            end = helper.str_to_date(args["end"], "%Y-%m-%dT%H:%M:%S")

        res_json = helper.get_generator_climate(id, headers)
        co = 0
        co_per_time = []
        i = 0
        sorted(res_json["climateData"],
               key=lambda i: helper.str_to_date(i["createdAt"]))

        for climate in res_json["climateData"]:
            climate["createdAt"] = helper.str_to_date(climate["createdAt"])
            if(climate["createdAt"] < begin):
                api.logger.info(f'create: {climate["createdAt"]}, begin: {begin}')
                api.logger.info(climate["createdAt"] == begin)
                continue

            if(climate["createdAt"] > end):
                api.logger.info(f'create: {climate["createdAt"]}, begin: {end}')
                break

            co += int(climate["co2"])
            co_per_time.append(
                {"inversorEfficiency": climate["co2"], "time": helper.date_to_str(climate["createdAt"])})
            i = i + 1

        if not i:
            return {"average": 0, "co2PerTime": []}
        average_energy = co/i
        return {"average": average_energy, "co2PerTime": co_per_time}
