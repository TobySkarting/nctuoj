from req import Service
from permission.base import BasePermission

class Session(BasePermission):
    def post(self, req):
        if len(req.account):
            return (401, "You have already signined.")

