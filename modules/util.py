import ast
import requests


def get_uuid(mc_name):
    d = ast.literal_eval(requests.get('https://api.mojang.com/users/profiles/minecraft/' + mc_name).text)
    unformatted = d['id']
    part = unformatted[:8], unformatted[8:12], unformatted[12:16], unformatted[16:20], unformatted[20:]
    return part[0] + '-' + part[1] + '-' + part[2] + '-' + part[3] + '-' + part[4]
