import requests
import random

def GenerateSettlementName():
    name = "None"
    queryd = {'type': 'English Town', 'n': '1'}
    url = 'https://donjon.bin.sh/name/rpc-name.fcgi'
    page = requests.get(url, params=queryd)
    if page.status_code == 200:
        # We are returning only 1 name. Strip the text of all whitespace
        name = page.text.strip()
    return name
