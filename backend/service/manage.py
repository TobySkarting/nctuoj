from service.base import BaseService

class GroupManageService(BaseService):
    def __init__(self, db, rs):
        super().__init__(self, db, rs)
        GroupManageService.inst = self
