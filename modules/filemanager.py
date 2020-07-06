import json
import os

from . import request

# whitelist_location = os.getenv('whitelist_location')
whitelist_location = '/home/finn/Coding/Data/MCControl/whitelist.json'
# adminlist_location = os.getenv('adminlist_location')
adminlist_location = '/home/finn/Coding/Data/MCControl/adminlist.json'
requests_location = os.getenv('requests_location')


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def json_as_dict(path):
    with open(adminlist_location) as json_data:
        return json.load(json_data)


def save_requests(requests_messages):
    data = []
    for i in requests_messages:
        d = {'type': type(i), 'author_id': i.author_id, 'admin_msg_id': i.admin_msg_id}
        if type(i) == request.WhitelistRequest:
            d['mc_name'] = i.mc_name
            d['uuid'] = i.uuid
        data.append(d)

    with open(requests_location, 'w') as outfile:
        json.dump(data, outfile)


async def write_whitelist(mc_name, uuid):
    print('Writing whitelist...')
    with open(whitelist_location, 'r') as json_data:
        data = json.load(json_data)
        data = merge_two_dicts(data, {"uuid": uuid, "name": mc_name})
    with open(whitelist_location, 'w') as outfile:
        json.dump(data, outfile)
    print('Done')


def get_admin_id(guild_id):
    with open(adminlist_location, 'r') as file:
        data = json.load(file)
    if int(data[str(guild_id)]):
        return int(data[str(guild_id)])
    else:
        return None


def add_admin(admin_id, guild_id):
    admins_dict = json_as_dict(adminlist_location)
    admins_dict[str(guild_id)] = admin_id
    with open(adminlist_location, 'w') as outfile:
        print('Writing admin data...')
        json.dump(admins_dict, outfile)
    print('Success')
