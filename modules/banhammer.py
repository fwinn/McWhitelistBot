from . import filemanager, util


def ban_by_dc_id(dc_id, reason):
    db = filemanager.get_db()
    cursor = db.cursor()
    sql = """
    INSERT INTO active_bans (uuid, dc_id, first_name, classs, date_registered, date_banned, reason)
    SELECT uuid, dc_id, first_name, classs, date, %s, %s FROM dc_users WHERE dc_id = %s;
    """
    val = (util.now(), reason, dc_id, )
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def ban_by_mc_uuid(uuid, reason):
    db = filemanager.get_db()
    cursor = db.cursor()
    sql = """
       INSERT INTO active_bans (uuid, dc_id, first_name, classs, date_registered, date_banned, reason)
       SELECT uuid, dc_id, first_name, classs, date, %s, %s FROM dc_users WHERE uuid = %s;
       """
    val = (util.now(), reason, uuid,)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
