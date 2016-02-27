from permission.base import PermissionBase
from req import Service
from map import *

class ApiVerdictTypesPermission(PermissionBase):
    def post(req, data):
        if map_power['verdict_manage'] not in req.account['power']:
            return (403, 'Permission Denied')
        return None

class ApiVerdictTypePermission(PermissionBase):
    def edit(req, data):
        if map_power['verdict_manage'] not in req.account['power']:
            return (403, 'Permission Denied')
        err, res = yield from Service.Verdict.get_verdict({'id': data['id']})
        if err: return err
        return None

    def get(req, data):
        err, res = yield from Service.Verdict.get_verdict({'id': data['id']})
        if err: return err
        if res['problem_id'] != 0:
            err, problem = yield from Service.Problem.get_problem({'id': res['problem_id']})
            if err: return err
            if map_power['verdict_manage'] not in req.account['power']:
                return (403, 'Permission Denied')
            if problem['group_id'] not in req.group:
                return (403, 'Permission Denied')
            if map_group_power['problem_manage'] not in req.current_group_power:
                return (403, 'Permission Denied')
        return None

    def put(req, data):
        err = yield from ApiVerdictTypePermission.edit(req, data)
        if err: return err
        return None

    def delete(req, data):
        err = yield from ApiVerdictTypePermission.edit(req, data)
        if err: return err
        return None

