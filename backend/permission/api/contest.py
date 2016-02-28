from permission.base import PermissionBase
from req import Service
from map import *

class ApiContestsPermission(PermissionBase):
    def post(req, data):
        if map_group_power['contest_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        return None

class ApiContestPermission(PermissionBase):
    def view(req, data):
        err, contest = yield from Service.Contest.get_contest({'id': data['id']})
        if err: return err
        if contest['group_id'] != req.current_group:
            return (403, 'Permission Denied')
        if not (contest['visible'] > 0 or map_group_power['contest_manage'] in req.current_group_power):
            return (403, 'Permission Denied')
        return None

    def edit(req, data):
        if map_group_power['contest_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        err, contest = yield from Service.Contest.get_contest({'id': data['id']})
        if err: return err
        if contest['group_id'] != req.current_group:
            return (403, 'Permission Denied')
        return None

    def get(req, data):
        err = yield from ApiContestPermission.view(req, data)
        if err: return err
        return None

    def put(req, data):
        err = yield from ApiContestPermission.edit(req, data)
        if err: return err
        return None

    def delete(req, data):
        err = yield from ApiContestPermission.edit(req, data)
        if err: return err
        return None

class ApiContestProblemsPermission(PermissionBase):
    def get(req, data):
        err = yield from ApiContestPermission.view(req, data)
        if err: return err
        return None

    def put(req, data):
        err = yield from ApiContestPermission.edit(req, data)
        if err: return err
        return None

class ApiContestScoreboardPermission(PermissionBase):
    def get(req, data):
        err = yield from ApiContestPermission.view(req, data)
        if err: return err
        return None

class ApiContestSubmissionsPermission(PermissionBase):
    def get(req, data):
        err = yield from ApiContestPermission.view(req, data)
        if err: return err
        return None
