from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
import requests, os, json
import core.fuzzy as fuzzy_core

api = Namespace('fuzzy', description='Fuzzy related calculations')

STORAGE_URI = os.getenv('DATA_STORAGE_HOST')
STORAGE_PORT = os.getenv('DATA_STORAGE_PORT')

parser = reqparse.RequestParser()
@api.route('/fuzzy')
class RunFuzzy(Resource):
    def post(self):
        body = request.json
        response = fuzzy_core.evaluate_eolic(body['wind'], body['potency'])
        return response

