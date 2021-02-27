from . import filemanager


def ban_by_dc_id(dc_id):
    db = filemanager.get_db()
    cursor = db.cursor()
    sql = "DELETE FROM dc_users WHERE dc_id = %s"
    val = (dc_id,)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


def ban_by_mc_uuid(uuid):
    db = filemanager.get_db()
    cursor = db.cursor()
    sql = "DELETE FROM dc_users WHERE uuid = %s"
    val = (uuid,)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
