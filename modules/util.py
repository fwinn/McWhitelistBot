import ast
import json
import requests


def get_uuid(mc_name):
    print('Requesting API...')
    html = requests.get('https://api.mojang.com/users/profiles/minecraft/' + mc_name).text
    if len(html) < 1:
        return
    d_string = json.loads(json.dumps(html))
    d = ast.literal_eval(d_string)
    if "id" in d:
        unformatted = d["id"]
    else:
        return
    part = unformatted[:8], unformatted[8:12], unformatted[12:16], unformatted[16:20], unformatted[20:]
    return part[0] + '-' + part[1] + '-' + part[2] + '-' + part[3] + '-' + part[4]
