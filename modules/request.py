class Request:
    def __init__(self, dc_id, admin_msg_id):
        self.dc_id = dc_id
        self.admin_msg_id = admin_msg_id


class WhitelistRequest(Request):
    def __init__(self, dc_id, admin_msg_id, mc_name, uuid, first_name, classs):
        super().__init__(dc_id, admin_msg_id)
        self.mc_name = mc_name
        self.uuid = uuid
        self.first_name = first_name
        self.classs = classs
