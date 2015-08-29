from service.base import BaseService
import config

class GroupService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        GroupService.inst = self

    def get_groups_list(self):
        pass

    def get_group_member_list(self):
        pass

    def create_group(self):
        pass

    def add_member_to_group(self):
        pass

    def modify_member_right(self):
        pass
