import json
import mysql.connector
import logging
import os
import _pickle

from . import mail, request, util

whitelist_location = 'data/survival_list.json'
requests_location = 'data/requests.pk1'

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pw = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


def get_ban_infos(dc_id):
    result = {}
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT id, reason from active_bans WHERE uuid = (SELECT uuid from dc_users WHERE dc_id = %s)"
    val = (dc_id,)
    cursor.execute(sql, val)
    tmp = cursor.fetchone()
    if tmp:
        result['ban_id'] = tmp[0]
        result['reason'] = tmp[1]
    else:
        return None
    cursor.close()
    db.close()
    return result


def get_db():
    logging.info('Connecting to database...')
    try:
        return mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pw,
            database=db_name
        )
    except mysql.connector.Error as err:
        logging.critical('Error: ' + str(err))
        mail.send_mail("ERROR: Database connection isn't working anymore")


def get_dc_id(uuid):
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT dc_id from dc_users WHERE uuid = %s"
    val = (uuid,)
    cursor.execute(sql, val)
    pre_result = cursor.fetchone()
    if pre_result is None:
        return None
    result = pre_result[0]
    cursor.close()
    db.close()
    return result


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
    db = get_db()
    cursor = db.cursor()
    timestamp = util.now()
    logging.info('Writing database...')
    sql = 'INSERT INTO dc_users (uuid, dc_id, first_name, classs, date) VALUES (%s, %s, %s, %s, %s)'
    val = (uuid, dc_id, first_name, classs, timestamp)
    cursor.execute(sql, val)
    sql = 'INSERT INTO whitelist (uuid) VALUES (%s)'
    val = (uuid, )
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    logging.debug('done')


def ids_in_db(uuid, dc_id):
    logging.info('Checking if IDs are already in the database...')
    result = {}
    db = get_db()
    cursor = db.cursor()
    logging.debug('Looking up UUID in the database...')
    sql = "SELECT COUNT(*) FROM dc_users WHERE uuid = %s;"
    val = (uuid,)
    cursor.execute(sql, val)
    amount_mc = cursor.fetchone()[0]
    # index 0: amount of MC UUIDs
    result['amount_mc'] = amount_mc
    cursor.close()

    logging.debug('Looking up Discord ID in the database...')
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM dc_users WHERE dc_id = %s;"
    val = (dc_id,)
    cursor.execute(sql, val)
    amount_dc = cursor.fetchone()[0]
    # index 1: amount of DC IDs
    result['amount_dc'] = amount_dc
    return result
