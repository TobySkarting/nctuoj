from permission.base import PermissionBase
from req import Service
from map import *

class ApiBulletinsPermission(PermissionBase):
    def get(req, data):
        return None

    def post(req, data):
        if map_group_power['bulletin_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        return None

class ApiBulletinPermission(PermissionBase):
    def edit(req, data):
        if map_group_power['bulletin_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        err, res = yield from Service.Bulletin.get_bulletin(data)
        if err: 
            return err
        if int(res['group_id']) != int(req.current_group):
            return (403, 'Permission Denied')
        return None

    def put(req, data):
        err = yield from ApiBulletinPermission.edit(req, data)
        if err: return err
        return None

    def delete(req, data):
        err = yield from ApiBulletinPermission.edit(req, data)
        if err: return err
        return None

