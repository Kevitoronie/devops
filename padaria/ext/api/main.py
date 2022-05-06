import json
from padaria.ext.db import db, auth
import requests

def consult_cnpj(cnpj):
    url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
    qs= {'token': 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX','cnpj': '06990590000123', 'plugin': 'RF'}
    response = requests.request('GET', url, params=qs)
    resp = json.loads(response.text)
    return resp

#consult_cnpj('44732884000144')