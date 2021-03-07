import ast
from datetime import datetime
import json
import logging
import requests


def get_uuid(mc_name):
    logging.debug('Requesting Mojang API...')
    html = requests.get('https://api.mojang.com/users/profiles/minecraft/' + mc_name).text
    if len(html) == 0:
        return
    d_string = json.loads(json.dumps(html))
    d = ast.literal_eval(d_string)
    if "id" in d:
        unformatted = d["id"]
    else:
        return
    part = unformatted[:8], unformatted[8:12], unformatted[12:16], unformatted[16:20], unformatted[20:]
    uuid = '-'.join(part)
    logging.info('UUID fetched: ' + uuid)
    return uuid


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
