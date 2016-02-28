import tornado
from req import Service
from permission.base import PermissionBase

class ApiBulletinsPermission(PermissionBase):
    def get(req, data):
        return None
    
    def post(req, data):
        print(req.current_group)
        print(req.current_group_power)
        print(req.map_group_power)
        return None
        
