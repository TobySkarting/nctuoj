from service.base import BaseService
import os
import config

class SubmissionService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        SubmissionService.inst = self
    
    def get_submission_list(self, data):
        required_args = ['page', 'count']
        err = self.check_required_args(required_args, data)
        print(data)
        if err: return (err, None)
        subsql = "(SELECT s.id FROM submissions as s "
        cond = " WHERE "
        if data['problem_id']:
            cond += "problem_id=%s AND " % (int(data['problem_id']))
        if data['user_id']:
            cond += "user_id=%s AND " % (int(data['user_id']))
        if cond == " WHERE ":
            cond == ""
        else:
            cond = cond[:-4]
        subsql += cond + "ORDER BY id LIMIT %s OFFSET %s) as s2"
        sql = """
            SELECT s.* 
            FROM submissions as s, 
            """ + subsql + """
            WHERE s.id = s2.id
            """

        res = yield from self.db.execute(sql, (data['count'], (int(data["page"])-1)*int(data["count"]), ))
        return (None, res)

    def get_submission_list_count(self, data):
        ### if exist data['problem_id']
        ### else exist data['group_id']
        if 'problem_id' in data and data['problem_id']:
            pass
        elif 'group_id' in data and data['group_id']:
            res = self.rs.get('submission_list_count@%s' % (str(data['group_id'])))

