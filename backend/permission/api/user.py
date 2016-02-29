from permission.base import PermissionBase
from req import Service
from map import *

class ApiUsersPermission(PermissionBase):
    def get(req, data):
        if map_power['user_manage'] not in req.account['power']:
            return (403, 'Permission Denied')
        return None

class ApiUserPermission(PermissionBase):
    def put(req, data):
        if int(data['id']) != req.account['id']:
            return (403, 'Permission Denied')
        return None

    def post(req, data):
        if map_power['user_manage'] not in req.account['power']:
            return (403, 'Permission Denied')
        return None

    def delete(req, data):
        if map_power['user_manage'] not in req.account['power']:
            return (403, 'Permission Denied')
        return None

