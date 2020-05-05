import requests
import random

def get_settlement_name():
    return query_donjon_service('English Town')


def get_male_name(firstOnly = True):
    name = query_donjon_service('English Male')
    if firstOnly:
        name = name.split()[0]
    return name


def get_female_name(firstOnly = True):
    name = query_donjon_service('English Female')
    if firstOnly:
        name = name.split()[0]
    return name


def query_donjon_service(nameType):
    name = "None"
    queryd = {'type': nameType, 'n': '1'}
    url = 'https://donjon.bin.sh/name/rpc-name.fcgi'

    try:
        page = requests.get(url, params=queryd)
        if page.status_code == 200:
            name = page.text.strip()
    except Exception:
        name = "None"

    return name

