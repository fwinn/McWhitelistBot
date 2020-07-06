class Request:
    def __init__(self, author_id, admin_msg_id):
        self.author_id = author_id
        self.admin_msg_id = admin_msg_id


class WhitelistRequest(Request):
    def __init__(self, author_id, admin_msg_id, mc_name, uuid):
        super().__init__(author_id, admin_msg_id)
        self.mc_name = mc_name
        self.uuid = uuid

