from service.base import BaseService
import config

class BulletinService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        BulletinService.inst = self

    def get_bulletin_list(self, data={}):
        required_args = ['group_id', 'page', 'count']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        sql = "SELECT bulletins.*, users.account as setter_user FROM bulletins, users WHERE bulletins.group_id = %s and bulletins.setter_user_id = users.id order by bulletins.id DESC limit %s, %s"
        col = ["id", "group_id", "setter_user_id", "title", "content", "created_at", "updated_at", "setter_user"]
        res = yield from self.db.execute(sql, (data["group_id"], (int(data["page"])-1)*data["count"], data["count"], ), col=col)
        err, total = yield from self.get_bulletin_list_count(data)
        yield from self.db.flush_tables()
        return (None, res)

    def get_bulletin_list_count(self, data={}):
        required_args = ['group_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = yield from self.db.execute("SELECT COUNT(*) FROM bulletins WHERE group_id=%s", (data['group_id'],));
        yield from self.db.flush_tables()
        return (None, res[0][0])


    def get_bulletin(self, data={}):
        required_args = ['group_id', 'id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        col = ["id", "group_id", "setter_user_id", "title", "content", "created_at", "updated_at", "setter_user"]
        """ new bulletin """
        if int(data['id']) == 0:
            res = {}
            for x in col:
                res[x] = ""
            res['id'] = 0
            return (None, res)

        sql = "SELECT bulletins.*, b.account as setter_user FROM bulletins inner join (SELECT id, account FROM users) as b on bulletins.setter_user_id=b.id WHERE bulletins.id=%s"
        res = yield from self.db.execute(sql, (data["id"]), col=col)
        if len(res) == 0:
            return ('Error bulletin id', None)
        res = res[0]
        if int(res['group_id']) != int(data['group_id']):
            return ('Error mapping bulletin id and group id', None)
        yield from self.db.flush_tables()
        return (None, res)
    
    def get_latest_bulletin(self, data={}):
        required_args = ['group_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        col = ["id", "group_id", "setter_user_id", "title", "content", "created_at", "updated_at", "setter_user"]
        sql = "SELECT bulletins.*, b.account as setter_user FROM bulletins inner join (SELECT id, account FROM users) as b on bulletins.setter_user_id=b.id WHERE bulletins.group_id=%s ORDER BY bulletins.id DESC LIMIT 1"
        res = yield from self.db.execute(sql, (data["group_id"]), col=col)
        if len(res) == 0:
            return ('Empty', None)
        return (None, res[0])
        

    def post_bulletin(self, data={}):
        required_args = ['id', 'group_id', 'setter_user_id', 'title', 'content']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        if int(data['id']) == 0:
            data.pop('id')
            sql, parma = self.gen_insert_sql("bulletins", data)
            yield from self.db.execute(sql, parma)
        else:
            err, res = yield from self.get_bulletin(data)
            if err:
                return (err, None)
            data.pop('id')
            sql, parma = self.gen_update_sql("bulletins", data)
            yield from self.db.execute(sql + " WHERE id=" + str(res['id']), parma)
        yield from self.db.flush_tables()
        return (None, None)

    def delete_bulletin(self, data={}):
        required_args = ['id', 'group_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        err, res = yield from self.get_bulletin(data)
        if err: return (err, None)
        yield from self.db.execute("DELETE FROM bulletins WHERE id=%s", (int(data['id'])))
        return (None, None)
