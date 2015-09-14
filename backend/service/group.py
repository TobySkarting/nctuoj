from service.base import BaseService
import config

class GroupService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)

        GroupService.inst = self

    def get_group_list(self):
        res = self.rs.get('group_list')
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute('SELECT * FROM groups ORDER BY id;')
        self.rs.set('group_list', res)
        self.rs.set('group_list_count', res_cnt)
        return (None, res)

    def get_group_list_count(self):
        res = self.rs.get('group_list_count')
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute('SELECT COUNT(*) FROM groups;')
        self.rs.set('group_list_count', res)
        return (None, res)

    def get_group_member_list(self, data={}):
        required_args = ['id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        res = self.rs.get('group@%s@user'%(str(data['id'])))
        if res: return (None, res)
        res, res_cnt = yield from self.db.execute('SELECT u.* FROM map_group_user as g, users as u WHERE g.user_id=u.id AND g.group_id=%s ORDER BY u.id;', (data['id'], ))
        self.rs.set('group@%s@user'%(str(data['id'])))
        return (None, res)

    def post_group(self, data={}):
        required_args = ['id', 'name', 'description']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        self.rs.delete('group@%s@user'%(str(data['id'])))
        if int(data['id']) == 0:
            data.pop('id')
            sql, param = self.gen_insert_sql('groups', data)
            id = (yield from self.db.execute(sql, param))[0][0]['id']
        else:
            id = data.pop('id')
            sql, param = self.gen_update_sql('groups', data)
            yield from self.db.execute(sql+' WHERE id=%s', param+(id,))
        return (None, id)

    def post_group_user(self, data={}):
        required_args = ['user_id', 'group_id']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        sql, param = self.gen_insert_sql('map_group_user', data)
        id = (yield from self.db.execute(sql, param))[0][0]['id']
        return (None, id)

    def post_group_user_power(self):
        pass

    def delete_group_user(self):
        pass

    def delete_group(self):
        pass
