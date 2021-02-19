from datetime import datetime
import json
import mysql.connector
import os
import _pickle

from . import request

whitelist_location = 'data/survival_list.json'
requests_location = 'data/requests.pk1'

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pw = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pw,
    database=db_name
)
cursor = db.cursor()


def json_as_dict(path):
    with open(path) as json_data:
        return json.load(json_data)


def save_requests(requests_messages):
    with open(requests_location, 'wb') as output:
        _pickle.dump(requests_messages, output, -1)


def load_requests():
    try:
        with open(requests_location, 'rb') as file:
            r = _pickle.load(file)
    except FileNotFoundError:
        r = []
    return r


async def write_whitelist(r: request.WhitelistRequest):
    uuid = r.uuid
    first_name = r.first_name
    classs = r.classs
    dc_id = r.dc_id

    # Database:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('Writing database...')
    sql = 'INSERT INTO dc_users (uuid, dc_id, first_name, classs, date) VALUES (%s, %s, %s, %s, %s)'
    val = (uuid, dc_id, first_name, classs, timestamp)
    cursor.execute(sql, val)
    db.commit()
    print('done')


def uuid_in_whitelist(uuid):
    print('Looking up UUID in the database...')
    sql = "SELECT COUNT(*) FROM dc_users WHERE uuid = '%s'" % uuid
    cursor.execute(sql)
    result = cursor.fetchone()
    print('Result: ' + str(result))
    return result[0]


def dc_id_in_whitelist(dc_id):
    print('Looking up Discord ID in the database...')
    sql = "SELECT COUNT(*) FROM dc_users WHERE dc_id = '%s'" % dc_id
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]
