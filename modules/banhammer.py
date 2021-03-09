from . import filemanager, util


def ban_by_dc_id(dc_id, reason):
    db = filemanager.get_db()
    cursor = db.cursor()
    sql = """
    INSERT INTO active_bans (uuid,  date_banned, reason)
    SELECT uuid,  %s, %s FROM dc_users WHERE dc_id = %s;
    """
    val = (util.now(), reason, dc_id)
    cursor.execute(sql, val)
    sql = "DELETE FROM whitelist WHERE uuid = (SELECT uuid FROM dc_users WHERE dc_id = %s);"
    val = (dc_id, )
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def ban_by_mc_uuid(uuid, reason):
    db = filemanager.get_db()
    cursor = db.cursor()
    sql = """
       INSERT INTO active_bans (uuid,  date_banned, reason)
       SELECT uuid, %s, %s FROM dc_users WHERE uuid = %s;
       """
    val = (util.now(), reason, uuid,)
    cursor.execute(sql, val)
    sql = "DELETE FROM whitelist WHERE uuid = %s;"
    val = (uuid,)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
