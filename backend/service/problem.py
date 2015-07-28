from service.base import BaseService
import config

class ProblemService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        ProblemService.inst = self

    def get_problem_list(self, data={}):
        if not "page" in data: data["page"] = 1
        if not "count" in data: data["count"] = 100
        sql = "SELECT `id`, `title`, `group_id`, `created_at` FROM `problems` LIMIT %s, %s"
        col = ("id", "title", "setter", "created_at",)
        res = yield from self.db.execute(sql, ((int(data["page"])-1)*data["count"], data["count"], ), col=col)
        yield from self.db.flush_tables()
        return (None, res)
        
