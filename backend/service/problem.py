from service.base import BaseService
import config

class ProblemService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        ProblemService.inst = self

    def get_problem_list(self, data={}):
        required_args = ['group_id', 'page', 'count']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        sql = """
            SELECT
            p.`id`, p.`title`, p.`source`, p.`group_id`, p.`created_at`, 
            u.`id` as setter_user_id, u.`account` as setter_user,
            g.`name` as `group_name`
            FROM `problems` as p, `users` as u, `groups` as g
            """
        if int(data['group_id']) == 1:
            if data['is_admin']:
                sql += "WHERE (p.group_id=%s OR p.visible = 2)"
            else:
                sql += "WHERE ((p.group_id=%s AND p.visible <> 0) OR p.visible = 2)"
        else:
            if data['is_admin']:
                sql += "WHERE p.group_id=%s"
            else:
                sql += "WHERE p.group_id=%s AND p.visible <> 0"
        sql += """
            AND u.id = p.setter_user_id AND g.id = p.group_id
            ORDER by p.id LIMIT %s, %s
            """
        res = yield from self.db.execute(sql, (data['group_id'], (int(data["page"])-1)*int(data["count"]), data["count"], ))
        for x in range(len(res)):
            res[x]['real_id'] = res[x]['id']
            res[x]['id'] = ((int)(data['page'])-1) * (int(data['count'])) + x + 1
        return (None, res)
        
    def get_problem_list_count(self, data={}):
        required_args = ['group_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('problem_list_count@%s@%s' 
                % (str(data['is_admin']), str(data['group_id'])))
        if res: return (None, res)
        sql = "SELECT COUNT(*) FROM problems "
        if int(data['group_id']) == 1:
            if data['is_admin']:
                sql += "WHERE (problems.group_id=%s OR problems.visible = 2)"
            else:
                sql += "WHERE ((problems.group_id=%s AND problems.visible <> 0) OR problems.visible = 2)"
        else:
            if data['is_admin']:
                sql += "WHERE problems.group_id=%s"
            else:
                sql += "WHERE problems.group_id=%s AND problems.visible <> 0"
        res = yield from self.db.execute(sql, (data['group_id'],))
        self.rs.set('problem_list_count@%s@%s'
                % (str(data['is_admin']), str(data['group_id'])), res[0]['COUNT(*)'])
        return (None, res[0]['COUNT(*)'])

    def get_problem(self, data={}):
        required_args = ['group_id', 'id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        if int(data['id']) == 0:
            col = ["id", "title", "description", "input", "output", "sample_input", "sample_output", "hint", "source", "group_id", "setter_user_id", "visible", "interactive", "checker_id", "created_at", "updated_at"]
            res = { x: "" for x in col }
            res['id'] = 0
            return (None, res)
        res = self.rs.get('problem@%s' % str(data['id']))
        if res: return (None, res)
        sql = "SELECT p.*, u.account as setter_user FROM problems as p, users as u WHERE p.setter_user_id=u.id AND p.id=%s"
        res = yield from self.db.execute(sql, (data["id"]))
        if len(res) == 0:
            return ('Error problem id', None)
        res = res[0]
        if int(res['group_id']) != int(data['group_id']) and int(res['visible']) != 2:
            return ('Error mapping problem id and group id', None)
        self.rs.set('problem@%s' % str(data['id']), res)
        return (None, res)

    def post_problem(self, data={}):
        required_args = ['id', 'group_id', 'setter_user_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        if int(data['id']) == 0:
            data.pop('id')
            sql, parma = self.gen_insert_sql("problems", data)
            insert_id = yield from self.db.execute(sql, parma)
            return (None, insert_id)
        else:
            err, res = yield from self.get_problem(data)
            self.rs.delete('problem@%s' % str(data['id']))
            if err:
                return (err, None)
            if int(res['group_id']) != int(data['group_id']):
                return ('Error mapping problem id and group id', None)
            data.pop('id')
            sql, parma = self.gen_update_sql("problems", data)
            yield from self.db.execute("%s WHERE id = %s" % (sql, str(res['id'])), parma)
            return (None, res['id'])

    def delete_problem(self, data={}):
        required_args = ['id', 'group_id', 'setter_user_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        err, res = yield from self.get_problem(data)
        if int(res['group_id']) != int(data['group_id']):
            return ('Error mapping problem id and group id', None)
        if err: return (err, None)
        yield from self.db.execute("DELETE FROM problems WHERE id=%s", (int(data['id'])))
        return (None, None)
