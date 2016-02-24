from service.base import BaseService
from req import Service
from utils.form import form_validation
import config

class GroupService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        GroupService.inst = self

    def get_group_list(self, data={}):
        required_args = [{
            'name': '+page',
            'type': int,
        }, {
            'name': '+count',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute('SELECT * FROM groups ORDER BY id LIMIT %s OFFSET %s;', (data['count'], int(data['page']-1)*int(data['count']),))
        return (None, res.fetchall())


    def get_group_list_count(self):
        # res = self.rs.get('group_list_count')
        # if res: return (None, res)
        res = yield self.db.execute('SELECT COUNT(*) FROM groups;')
        res = res.fetchone()
        # self.rs.set('group_list_count', res['count'])
        return (None, res['count'])

    def get_group(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        if int(data['id']) == 0:
            col = ["id", "name", "description", "type"]
            res = { x: "" for x in col }
            res['id'] = 0
            res['type'] = 0
            return (None, res)
        if err: return (err, None)
        # res = self.rs.get('group@%s'%(str(data['id'])))
        res = None
        if res is None:
            res = yield self.db.execute('SELECT * FROM groups WHERE id=%s;', (data['id'],))
            res = res.fetchone()
            # self.rs.set('group@%s'%(str(data['id'])), res)
        err, res['members'] = yield from self.get_group_member_list(data)
        return (None, res)

    def get_group_member_list(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        # res = self.rs.get('group@%s@user'%(str(data['id'])))
        # if res: return (None, res)
        res = yield self.db.execute('SELECT u.* FROM map_group_user as g, users as u WHERE g.user_id=u.id AND g.group_id=%s ORDER BY u.id;', (data['id'], ))
        res = res.fetchall()
        for x in res:
            err, x['group_power'] = yield from self.get_group_user_power({
                'user_id': x['id'], 
                'group_id': data['id']
            })
            x.pop('passwd')
            x.pop('token')
        return (None, res)

    def post_group(self, data={}):
        required_args = [{
            'name': '+name',
            'type': str,
        }, {
            'name': '+description',
            'type': str,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        # self.rs.delete('group@%s@user'%(str(data['id'])))
        sql, param = self.gen_insert_sql('groups', data)
        id = (yield self.db.execute(sql, param)).fetchone()['id']
        return (None, id)

    def put_group(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }, {
            'name': '+name',
            'type': str,
        }, {
            'name': '+description',
            'type': str,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        # self.rs.delete('group@%s@user'%(str(data['id'])))
        id = data.pop('id')
        sql, param = self.gen_update_sql('groups', data)
        yield self.db.execute(sql+' WHERE id=%s', param+(id,))
        # self.rs.delete('group@%s'%(str(id)))
        return (None, id)

    def post_group_user(self, data={}):
        required_args = [{
            'name': 'user_id',
            'type': int,
        }, {
            'name': 'group_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        sql, param = self.gen_insert_sql('map_group_user', data)
        try: res = yield self.db.execute(sql, param)
        except: return ('Already in', None)
        id = res.fetchone()['id']
        return (None, id)

    def delete_group_user(self, data={}):
        required_args = [{
            'name': '+user_id',
            'type': int,
        }, {
            'name': '+group_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute('DELETE FROM map_group_user WHERE user_id=%s AND group_id=%s RETURNING id;', (data['user_id'], data['group_id'],))
        print('RES: ',res)
        if res.rowcount == 0:
            return ("User isn't in this group", None)
        # self.rs.delete('group@%s@user'%(str(data['group_id'])))
        return (None, res.fetchone()['id'])

    def get_group_user_power(self, data={}):
        required_args = [{
            'name': '+user_id',
            'type': int,
        }, {
            'name': '+group_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        # res = self.rs.get('user_group_power@%s@%s' % (str(uid), str(gid)))
        # if res: return (None, res)
        res = yield self.db.execute("SELECT power from map_group_user_power where user_id=%s AND group_id=%s", (data['user_id'], data['group_id'],))
        power = list({ x['power'] for x in res })
        # self.rs.set('user_group_power@%s@%s' % (str(uid), str(gid)), power)
        return (None, power)

    def post_group_user_power(self, data={}):
        required_args = [{
            'name': '+user_id',
            'type': int,
        }, {
            'name': '+group_id',
            'type': int,
        }, {
            'name': '+power',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        err, current_power = yield from self.get_group_user_power(data)
        print(current_power)
        if int(data['power']) in current_power:
            yield self.db.execute('DELETE FROM map_group_user_power WHERE user_id=%s AND group_id=%s AND power=%s;', (data['user_id'], data['group_id'], data['power'],))
        else:
            sql, param = self.gen_insert_sql('map_group_user_power', data)
            # yield self.db.execute('INSERT INTO map_group_user_power (user_id, group_id, power) VALUES(%s, %s, %s);', (uid, gid, power))
            yield self.db.execute(sql, param)
        # self.rs.delete('user_group_power@%s@%s' % (str(uid), str(gid)))
        return (None, None)

    def get_user_contest(self, id):
        #res = self.rs.get('user@%scontest'%(str(id)))
        #if res: return (None, res)
        res = yield self.db.execute('SELECT contest_id FROM map_contest_user WHERE user_id=%s;', (id,))
        res = set(x['contest_id'] for x in res)
        return (None, res)

    def delete_group(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute('DELETE FROM groups WHERE id=%s RETURNING id;', (data['id'],))
        if res.rowcount == 0:
            return ('No ID exist', None)
        # self.rs.delete('group@%s'%(str(data['id'])))
        # self.rs.delete('group@%s@user'%(str(data['id'])))
        return (None, res.fetchone()['id'])

    def get_group_user_problem_info(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }, {
            'name': '+group_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        sql = '''SELECT s.*, s.id AS submission_id, p.id AS problem_id FROM (SELECT p.* FROM problems as p WHERE p.group_id=%s ORDER BY p.id) AS p LEFT JOIN (SELECT s2.*, v.abbreviation FROM (SELECT MIN(s2.id) AS submission_id FROM (SELECT s.problem_id, MAX(v.priority) AS priority FROM map_verdict_string AS v, submissions AS s WHERE v.id=s.verdict AND s.user_id=%s GROUP BY s.problem_id) AS s1, map_verdict_string AS v, submissions AS s2 WHERE v.priority=s1.priority AND v.id=s2.verdict AND s2.problem_id=s1.problem_id) AS s1, submissions AS s2, map_verdict_string AS v WHERE s2.id=s1.submission_id AND s2.verdict=v.id) AS s ON p.id=s.problem_id;'''
        res = yield self.db.execute(sql, (data['id'], data['group_id']))
        return (None, res.fetchall())

