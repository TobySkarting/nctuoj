from permission.base import PermissionBase
from req import Service
from map import *

class ApiGroupsPermission(PermissionBase):
    def post(req, data):
        if map_power['group_manage'] not in req.account['power']:
            return (403, 'Permission Denied')
        return None

class ApiGroupPermission(PermissionBase):
    def edit(req, data):
        err, res = yield from Service.Group.get_group({'id': data['id']})
        if err: return err
        if map_power['group_manage'] in req.account['power']:
            return None
        if map_group_power['group_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        return None

    def put(req, data):
        err = yield from ApiGroupPermission.edit(req, data)
        if err: return err
        return None

    def delete(req, data):
        err = yield from ApiGroupPermission.edit(req, data)
        if err: return err
        return None

class ApiGroupUserPermission(PermissionBase):
    def get(req, data):
        if int(data['user_id']) == int(req.account['id']):
            return None
        if map_group_power['group_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        return None

    def post(req, data):
        if int(data['user_id']) == req.account['id']:
            return None
        if map_group_power['group_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        return None

    def delete(req, data):
        if map_group_power['group_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        return None

class ApiGroupUserPowerPermission(PermissionBase):
    def get(req, data):
        if int(data['user_id']) == int(req.account['id']):
            return None
        if map_group_power['group_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        return None

    def post(req, data):
        if map_group_power['group_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        return None
