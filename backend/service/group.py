from service.base import BaseService
import config

class GroupService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        GroupService.inst = self
    """
    def get_problem_list(self, data={}):
        if not "page" in data: data["page"] = 1
        if not "count" in data: data["count"] = 100
        sql = "SELECT `id`, `title`, `group_id`, `created_at` FROM `problems` LIMIT %s, %s"
        col = ("id", "title", "setter", "created_at",)
        res = yield from self.db.execute(sql, ((int(data["page"])-1)*data["count"], data["count"], ), col=col)
        return (None, res)
    """

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
