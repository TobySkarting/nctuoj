from service.base import BaseService
import os
import config

class ContestService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        ContestService.inst = self

    def get_contest_list(self, data={}):
        required_args = ['group_id', 'page', 'count']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        sql = """
            SELECT 
            c.*,
            u.id as setter_user_id, u.account as setter_user,
            g.id as group_id, g.name as group_name
            FROM contests as c, users as u, groups as g
            WHERE u.id=c.setter_user_id AND g.id=c.group_id AND
            """
        if int(data['group_id']) == 1:
            sql += """ (c.group_id=%s OR c.visible=2) """
        else:
            sql += """ (p.group_id=%s) """
        sql += """ ORDER BY c.id limit %s OFFSET %s """

        res, res_cnt = yield from self.db.execute(sql, (data['group_id'], data['count'], (int(data["page"])-1)*int(data["count"]), ))
        return (None, res)
        
    def get_contest_list_count(self, data={}):
        required_args = ['group_id']
