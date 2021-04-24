from datetime import datetime
import os
import json
import requests

STORAGE_URI = os.environ.get('DATA_STORAGE_HOST')
STORAGE_PORT = os.environ.get('DATA_STORAGE_PORT')


def str_to_date(date: str, format="%Y-%m-%dT%H:%M:%S.%fZ"):
    return datetime.strptime(date, format)


def date_to_str(date: datetime, format="%Y-%m-%dT%H:%M:%S"):
    return date.strftime(format)


def get_generator_energy(id: str, headers={}):
    res = requests.get(
        f'http://{STORAGE_URI}:{STORAGE_PORT}/generator/{id}/energy', headers=headers)
    return json.loads(res.text)

def get_generator_climate(id: str, headers={}):
    res = requests.get(
        f'http://{STORAGE_URI}:{STORAGE_PORT}/generator/{id}/climate', headers=headers)
    return json.loads(res.text)
