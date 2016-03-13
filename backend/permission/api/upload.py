from permission.base import PermissionBase
from req import Service
from map import *

class ApiUploadPermission(PermissionBase):
    def post(req, data={}):
        if map_group_power['problem_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        return None
