from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
import requests, os, json
import core.fuzzy as fuzzy_core

api = Namespace('fuzzy', description='Fuzzy related calculations')

STORAGE_URI = os.getenv('DATA_STORAGE_HOST')
STORAGE_PORT = os.getenv('DATA_STORAGE_PORT')

parser = reqparse.RequestParser()
@api.route('/eolic')
class FuzzyEolic(Resource):
    def post(self):
        body = request.json
        response = fuzzy_core.evaluate_eolic(body['wind'], body['potency'])
        return response

@api.route('/solar')
class FuzzySolar(Resource):
    def post(self):
        print("AQUI PAPAI")
        body = request.json
        print(body)
        response = fuzzy_core.evaluate_solar(body['temperature'], body['potency'])
        return response


