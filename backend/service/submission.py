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
        if err: return (err, None)
        subsql = "(SELECT s.id FROM submissions as s, problems as p "
        cond = " WHERE p.id=s.problem_id AND p.group_id=%s AND "
        if data['problem_id']:
            cond += "problem_id=%s AND " % (int(data['problem_id']))
        if data['user_id']:
            cond += "user_id=%s AND " % (int(data['user_id']))
        cond = cond[:-4]
        subsql += cond + "ORDER BY id LIMIT %s OFFSET %s) as s2"
        sql = """
            SELECT s.*,
            u.account as user,
            e.lang
            FROM submissions as s, users as u, execute_types as e,
            """ + subsql + """
            WHERE s.id = s2.id and u.id = s.user_id and e.id=s.execute_type_id
            """

        res = yield from self.db.execute(sql, (data['group_id'], data['count'], (int(data["page"])-1)*int(data["count"])))
        return (None, res)

    def get_submission_list_count(self, data):
        subsql = "SELECT count(*) FROM submissions as s "
        cond = " WHERE "
        if data['problem_id']:
            cond += "problem_id=%s AND " % (int(data['problem_id']))
        if data['user_id']:
            cond += "user_id=%s AND " % (int(data['user_id']))
        if cond == " WHERE ":
            cond = ""
        else:
            cond = cond[:-4]

    def get_submission(self, data):
        if data['id'] == 0:
            pass
        res = yield from self.db.execute("""
        SELECT s.*, e.lang as execute_lang, e.description as execute_description, u.account as submitter, p.title as problem_name
        FROM submissions as s, execute_types as e, users as u, problems as p
        WHERE s.id=%s AND e.id=s.execute_type_id AND u.id=s.user_id AND s.problem_id=p.id
        """, (data['id'],))
        if len(res) == 0:
            return ('No Submission ID', None)
        res = res[0]
        file_path = './../data/submissions/%s/%s' % (res['id'], res['file_name'])
        with open(file_path) as f:
            res['code'] = f.read()
        res['code_line'] = len(open(file_path).readlines())
        return (None, res)

