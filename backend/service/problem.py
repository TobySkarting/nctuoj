from service.base import BaseService
import os
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
            p.id, p.title, p.source, p.visible, p.created_at,
            u.id as setter_user_id, u.account as setter_user,
            g.id as group_id, g.name as group_name
            FROM problems as p, users as u, groups as g
            WHERE u.id=p.setter_user_id AND g.id=p.group_id AND
            """
        #if int(data['group_id']) == 1:
        #    sql += """ (p.group_id=%s OR p.visible=2) """
        #else:
        sql += """ (p.group_id=%s) """
        sql += """ ORDER BY p.id limit %s OFFSET %s """

        res, res_cnt = yield from self.db.execute(sql, (data['group_id'], data['count'], (int(data["page"])-1)*int(data["count"]), ))
        return (None, res)
        
    ### Should be improvement
    def get_problem_list_count(self, data={}):
        required_args = ['group_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('problem_list_count@%s' 
                % (str(data['group_id'])))
        if res: return (None, res)
        sql = "SELECT COUNT(*) FROM problems as p "
        #if int(data['group_id']) == 1:
        #    sql += "WHERE (p.group_id=%s OR p.visible = 2)"
        #else:
        sql += "WHERE p.group_id=%s"
        res, res_cnt = yield from self.db.execute(sql, (data['group_id'],))
        self.rs.set('problem_list_count@%s'
                % (str(data['group_id'])), res[0]['count'])
        return (None, res[0]['count'])

    def get_problem(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)

        if int(data['id']) == 0:
            col = ["id", "title", "description", "input", "output", "sample_input", "sample_output", "hint", "source", "group_id", "setter_user_id", "visible", "interactive", "checker_id", "created_at", "updated_at"]
            res = { x: "" for x in col }
            res['id'] = 0
            res['visible'] = 0
            return (None, res)

        res = self.rs.get('problem@%s' % str(data['id']))
        if not res:
            sql = "SELECT p.*, u.account as setter_user FROM problems as p, users as u WHERE p.setter_user_id=u.id AND p.id=%s"
            res, res_cnt = yield from self.db.execute(sql, (data["id"], ))
            if res_cnt == 0:
                return ('No problem id', None)
            res = res[0]
            self.rs.set('problem@%s' % str(data['id']), res)
        err, res['execute'] = yield from self.get_problem_execute(data)
        err, res['testdata'] = yield from self.get_problem_testdata_list(data)
        return (None, res)

    def reset_rs_problem_count(self, group_id):
        self.rs.delete('problem_list_count@%s' % str(group_id))
        self.rs.delete('problem_list_count@1')


    def post_problem(self, data={}):
        required_args = ['id', 'group_id', 'setter_user_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        if int(data['id']) == 0:
            self.reset_rs_problem_count(data['group_id'])
            data.pop('id')
            sql, parma = self.gen_insert_sql("problems", data)
            insert_id = (yield from self.db.execute(sql, parma))[0][0]['id']
            return (None, insert_id)
        else:
            self.reset_rs_problem_count(data['group_id'])
            id = data.pop('id')
            self.rs.delete('problem@%s' % str(id))
            sql, parma = self.gen_update_sql("problems", data)
            yield from self.db.execute("%s WHERE id = %s" % (sql, id), parma)
            return (None, id)

    def delete_problem(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        err, data = yield from self.get_problem(data)
        if err: return (err, None)
        self.reset_rs_problem_count(data['group_id'])
        yield from self.db.execute("DELETE FROM problems WHERE id=%s", (int(data['id']),))
        yield from self.db.execute("DELETE FROM testdata WHERE problem_id=%s", (int(data['id']),))
        yield from self.db.execute("DELETE FROM submissions WHERE problem_id=%s", (int(data['id']),))
        yield from self.db.execute("DELETE FROM map_problem_execute WHERE problem_id=%s", (int(data['id']),))
        self.rs.delete('problem@%s' % str(data['id']))
        self.rs.delete('problem@%s@execute' % str(data['id']))
        self.rs.delete('problem@%s@testdata' % str(data['id']))
        return (None, None)

    def get_problem_execute(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('problem@%s@execute' % str(data['id']))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute("SELECT e.* FROM execute_types as e, map_problem_execute as m WHERE m.execute_type_id=e.id and m.problem_id=%s ORDER BY e.priority", (data['id'],))
        self.rs.set('problem@%s@execute' % str(data['id']), res)
        return (None, res)

    def post_problem_execute(self, data={}):
        yield from self.delete_problem_execute(data)
        if data['execute']:
            for x in data['execute']:
                yield from self.db.execute("INSERT INTO map_problem_execute (execute_type_id, problem_id) values (%s, %s)", (x, data['id']))
        return (None, None)

    def delete_problem_execute(self, data={}):
        self.rs.delete('problem@%s@execute' % str(data['id']))
        yield from self.db.execute("DELETE FROM map_problem_execute WHERE problem_id=%s", (data['id'],))
    

    def get_problem_testdata_list(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('problem@%s@testdata' % str(data['id']))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute("SELECT t.* FROM testdata as t, (SELECT id FROM testdata WHERE problem_id=%s ORDER BY id ASC) as t2 where t.id=t2.id;", (data['id'],))
        self.rs.set('problem@%s@testdata' % str(data['id']), res)
        return (None, res)
        
    def get_problem_testdata(self, data={}):
        required_args = ['testdata_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res, res_cnt = yield from self.db.execute("SELECT * FROM testdata WHERE id=%s", (data['testdata_id'], ))
        if res_cnt == 0:
            return ('No testdata id', None)
        return (None, res[0])

    def post_problem_testdata(self, data={}):
        required_args = ['id', 'testdata_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        self.rs.delete('problem@%s@testdata' % str(data['id']))
        if int(data['testdata_id']) == 0:
            id, cnt = yield from self.db.execute("INSERT INTO testdata (problem_id) VALUES (%s) RETURNING id;", (data['id'],))
            print('ID', id)
            return (None, id)
        else:
            required_args = ['time_limit', 'memory_limit', 'output_limit', 'score']
            err = self.check_required_args(required_args, data)
            if err: return (err, None)
            meta = { x: data[x] for x in required_args }
            sql, parma = self.gen_update_sql("testdata", meta)
            yield from self.db.execute("%s WHERE id=%s" % (sql, data['testdata_id']), parma)

            """ create folder """
            folder = "../data/testdata/%s/" % data['testdata_id']
            remote_folder = "./data/testdata/%s/" % data['testdata_id']
            try: os.makedirs(folder)
            except: pass

            """ save file and upload to ftp """
            for x in ['input', 'output']:
                if data[x] != None:
                    file_path = "%s/%s" % (folder, x)
                    with open(file_path, 'wb+') as f:
                        f.write(data[x]['body'])
                    remote_path = "%s/%s" % (remote_folder, x)
                    yield from self.ftp.upload(file_path, remote_path)
            return (None, data['testdata_id'])

    
    def delete_problem_testdata(self, data={}):
        required_args = ['testdata_id', 'id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        yield from self.db.execute("DELETE FROM testdata WHERE id=%s", (data['testdata_id'],))
        self.rs.delete('problem@%s@testdata' % str(data['id']))
        return (None, None)

    def post_rejudge_problem(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res, res_cnt = self.db.execute('SELECT s.id FROM submissions as s WHERE s.problem_id=%s;', (data['id'],))
        ### TODO add s.id in to wait_submissions
        for x in res:
            self.rs.delete('submission@%s'%(str(x['id'])))
        return (None, str(data['id']))
