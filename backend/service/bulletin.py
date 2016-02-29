from service.base import BaseService
from utils.form import form_validation
import config
### need to add rs
class BulletinService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        BulletinService.inst = self

    def get_bulletin_list(self, data={}):
        required_args = [{
                'name': '+group_id',
                'type': int,
            },{
                'name': '+page',
                'type': int,
            },{
                'name': '+count',
                'type': int,
            }
        ]
        err = form_validation(data, required_args)
        if err: return (err, None)
        sql = "SELECT bulletins.*, users.account as setter_user FROM bulletins, users WHERE ( bulletins.group_id = %s OR bulletins.group_id=1 )and bulletins.setter_user_id = users.id order by bulletins.id DESC limit %s offset %s"
        res = yield self.db.execute(sql, (data["group_id"], data['count'], (int(data["page"])-1)*data["count"],))
        return (None, res.fetchall())

    def get_bulletin_list_count(self, data={}):
        required_args = [{
            'name': '+group_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        res = yield self.db.execute("SELECT COUNT(*) FROM bulletins WHERE group_id=%s OR group_id=1", (data['group_id'],))
        return (None, res.fetchone()['count'])

    def get_bulletin(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        """ new bulletin """
        if int(data['id']) == 0:
            col = ['content', 'title']
            res = { x: "" for x in col }
            res['id'] = 0
            return (None, res)

        sql = "SELECT b.*, u.account as setter_user FROM bulletins as b, users as u WHERE b.setter_user_id=u.id AND b.id=%s"
        res = yield self.db.execute(sql, (data["id"], ))
        if res.rowcount == 0:
            return ((404, 'Error bulletin id'), None)
        return (None, res.fetchone())
    
    def get_latest_bulletin(self, data={}):
        required_args = [{
            'name': '+group_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        # res = self.rs.get('latest_bulletin@%s' % str(data["group_id"]))
        # if res: return (None, res)
        sql = "SELECT b.*, u.account as setter_user FROM bulletins as b, users as u WHERE b.setter_user_id=u.id AND group_id=%s ORDER BY b.id DESC LIMIT 1"
        res = yield self.db.execute(sql, (data["group_id"],))
        if res.rowcount == 0: return ((404, 'Empty'), None)
        res = res.fetchone()
        # self.rs.set('latest_bulletin@%s' % str(data["group_id"]), res)
        return (None, res)

    def put_bulletin(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }, {
            'name': '+group_id',
            'type': int,
        }, {
            'name': '+setter_user_id',
            'type': int,
        }, {
            'name': '+title',
            'type': str,
            'xss': True,
        }, {
            'name': '+content',
            'type': str,
            'xss': True,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        err, res = yield from self.get_bulletin(data)
        if err: return (err, None)
        data.pop('id')
        sql, parma = self.gen_update_sql("bulletins", data)
        yield self.db.execute("%s WHERE id=%%s AND group_id=%%s;"%sql, parma+(res['id'],res['group_id'],))
        return (None, None)

    def post_bulletin(self, data={}):
        required_args = [{
            'name': '+group_id',
            'type': int,
        }, {
            'name': '+setter_user_id',
            'type': int,
        }, {
            'name': '+title',
            'type': str,
            'non_empty': True,
            'xss': True,
        }, {
            'name': '+content',
            'non_empty': True,
            'type': str,
            'xss': True,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        sql, parma = self.gen_insert_sql("bulletins", data)
        id = (yield self.db.execute(sql, parma)).fetchone()['id']
        return (None, str(id))

    def delete_bulletin(self, data={}):
        required_args = [{
            'name': '+id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        yield self.db.execute("DELETE FROM bulletins WHERE id=%s AND group_id=%s", (data['id'],data['group_id'],))
        return (None, None)
