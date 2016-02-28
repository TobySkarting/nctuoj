from permission.base import PermissionBase
from req import Service
from map import *

class ApiExecuteTypesPermission(PermissionBase):
    def post(req, data):
        if map_power['execute_manage'] not in req.account['power']:
            return (403, 'Permission Denied')
        return None

class ApiExecuteTypePermission(PermissionBase):
    def edit(req, data):
        if map_power['execute_manage'] not in req.account['power']:
            return (403, 'Permission Denied')
        err, res = yield from Service.Execute.get_execute({'id': data['id']})
        if err: return err
        return None

    def put(req, data):
        err = yield from ApiExecuteTypePermission.edit(req, data)
        if err: return err
        return None

    def delete(req, data):
        err = yield from ApiExecuteTypePermission.edit(req, data)
        if err: return err
        return None

class ApiExecuteTypesPriorityPermission(PermissionBase):
    def post(req, data):
        if map_power['execute_manage'] not in req.account['power']:
            return (403, 'Permission Denied')
        return None

