from service.base import BaseService
import config

class ProblemService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        ProblemService.inst = self

    def get_problem_list(self, data={}):
        required_args = ['group_id', 'page', 'count']
        if not self.check_required_args(required_args, data) :
            return ('Etoofewargs', None)
        sql = "SELECT `id`, `title`, `group_id`, `created_at` FROM `problems` LIMIT %s, %s"
        col = ("id", "title", "setter", "created_at",)
        res = yield from self.db.execute(sql, ((int(data["page"])-1)*data["count"], data["count"], ), col=col)
        yield from self.db.flush_tables()
        return (None, res)
        
    def get_problem_list_count(self, data={}):
        required_args = ['group_id']
        if not self.check_required_args(required_args, data):
            return ('Etoofewargs', None)
        res = yield from self.db.execute("SELECT COUNT(*) FROM problems WHERE group_id=%s", (data['group_id'],));
        yield from self.db.flush_tables()
        return (None, res[0][0])
