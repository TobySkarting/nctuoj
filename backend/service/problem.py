from service.base import BaseService
import config

class ProblemService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        ProblemService.inst = self

    ### 
    ###
    ###
    def get_problem_list(self, data={}):
        required_args = ['group_id', 'page', 'count']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        if int(data['group_id']) == 1:
            sql = """SELECT 
            problems.`id`, problems.`title`, problems.`source`, problems.`group_id`, problems.`created_at`, users.`account` 
            FROM `problems`, `users` 
            WHERE (problems.`group_id`=%s OR problems.`visible`=2)
            AND problems.setter_user_id=users.id
            ORDER by problems.id LIMIT %s, %s"""
        else:
            sql = """SELECT 
            problems.`id`, problems.`title`, problems.`source`, problems.`group_id`, problems.`created_at`, users.`account`
            FROM `problems`, `users` 
            WHERE problems.`group_id`=%s  
            AND problems.setter_user_id=users.id 
            ORDER by problems.id LIMIT %s, %s"""
        col = ("id", "title", "source", "group_id", "created_at", "setter_user")
        res = yield from self.db.execute(sql, (data['group_id'], (int(data["page"])-1)*int(data["count"]), data["count"], ), col=col)
        for x in range(len(res)):
            res[x]['id'] = ((int)(data['page'])-1) * (int(data['count'])) + x + 1
        yield from self.db.flush_tables()
        return (None, res)
        
    def get_problem_list_count(self, data={}):
        required_args = ['group_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        if int(data['group_id']) == 1: res = yield from self.db.execute("SELECT COUNT(*) FROM problems WHERE group_id=%s OR visible=2", (data['group_id'],))
        else: res = yield from self.db.execute("SELECT COUNT(*) FROM problems WHERE group_id=%s", (data['group_id'],))
        yield from self.db.flush_tables()
        return (None, res[0][0])
