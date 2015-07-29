from service.base import BaseService
import config

class BulletinService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        BulletinService.inst = self

    def get_bulletin_list(self, data={}):
        required_args = ['group_id']
        if not self.check_required_args(required_args, data) :
            return ('Etoofewargs', None)
        if not "page" in data: data["page"] = 1
        if not "count" in data: data["count"] = 10
        sql = "SELECT bulletins.*, users.account as setter_user FROM bulletins, users WHERE bulletins.group_id = %s and bulletins.setter_user_id = users.id order by bulletins.id DESC limit %s, %s"
        col = ["id", "group_id", "setter_user_id", "title", "content", "created_at", "updated_at", "setter_user"]
        res = yield from self.db.execute(sql, (data["group_id"], (int(data["page"])-1)*data["count"], data["count"], ), col=col)
        for x in range(len(res)):
            res[x]['id'] = x + 1
        yield from self.db.flush_tables()
        return (None, res)


    def get_bulletin(self, data={}):
        required_args = ['group_id', 'id']
        if not self.check_required_args(required_args, data):
            return ('Etoofewargs', None)
        col = ["id", "group_id", "setter_user_id", "title", "content", "created_at", "updated_at", "setter_user"]
        if int(data['id']) == 0:
            res = {}
            for x in col:
                res[x] = ""
            return (None, res)
        sql = "SELECT bulletins.*, users.account as setter_user FROM bulletins, users WHERE bulletins.group_id = %s and bulletins.setter_user_id = users.id order by bulletins.id DESC limit %s, 1"
        res = yield from self.db.execute(sql, (data["group_id"], int(data["id"])-1, ), col=col)
        if len(res) == 0:
            return ('Enoid', None)
        res = res[0]
        res['id'] = data['id']
        yield from self.db.flush_tables()
        return (None, res)

    def post_bulletin(self, data={}):
        required_args = ['id', 'group_id', 'setter_user_id', 'title', 'content']
        if not self.check_required_args(required_args, data):
            return ('Etoofewargs', None)
        if int(data['id']) == 0:
            data.pop('id')
            sql, parma = self.gen_insert_sql("bulletins", data)
            yield from self.db.execute(sql, parma)
        else:
            res = yield from self.db.execute("SELECT id FROM bulletins where group_id=%s order by id DESC limit %s, 1", (data['group_id'], int(data['id'])-1,))
            if len(res) == 0:
                return ('ENoExist', None)
            data.pop('id')
            sql, parma = self.gen_update_sql("bulletins", data)
            yield from self.db.execute(sql + " WHERE id=" + str(res[0][0]), parma)
        yield from self.db.flush_tables()
        return (None, None)
