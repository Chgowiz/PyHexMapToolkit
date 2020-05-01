import requests
import random

def GetSettlementName():
    return GetDonjonName('English Town')


def GetMaleName(firstOnly = True):
    name = GetDonjonName('English Male')
    if firstOnly:
        name = name.split()[0]
    return name


def GetFemaleName(firstOnly = True):
    name = GetDonjonName('English Female')
    if firstOnly:
        name = name.split()[0]
    return name


def GetDonjonName(nameType):
    name = "None"
    queryd = {'type': nameType, 'n': '1'}
    url = 'https://donjon.bin.sh/name/rpc-name.fcgi'
    page = requests.get(url, params=queryd)
    if page.status_code == 200:
        name = page.text.strip()
    return name
