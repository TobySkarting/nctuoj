import json
import logging
import msgpack
import types
import datetime
import collections
import tornado.template
import tornado.gen
import tornado.web
import tornado.websocket
import datetime
import re
from map import map_power, map_group_power, map_lang, map_visible


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class Service:
    pass

class RequestHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        try:
            self.get_argument('json')
            self.res_json = True

        except tornado.web.HTTPError:
            self.res_json = False
    def log(self, msg):
        if not self.acct:
            id = 0
        else:
            id = self.acct['id']
        msg = '<USER %d> '%id + str(msg)
        logging.debug(msg)

    def get_args(self, name):
        meta = {}
        for n in name:
            try:
                if n[-2:] == "[]":
                    meta[n[:-2]] = self.get_arguments(n)
                elif n[-6:] == "[file]":
                    n = n[:-6]
                    meta[n] = self.request.files[n][0]
                else:
                    meta[n] = self.get_argument(n, None)
            except:
                meta[n] = None
                print("get_args error: ", n)
        return meta

    def prepare(self):
        try:
            self.current_group = re.search(r'.*/group/(\d+).*', self.request.uri).groups(1)[0]
        except:
            self.current_group = 0
        self.map_power = map_power
        self.map_group_power = map_group_power
        self.map_lang = map_lang




class ApiRequestHandler(RequestHandler):
    def render(self, code=200, msg=""):
        self.finish(json.dumps({'status': code,
                                'msg': msg}, cls=DatetimeEncoder))
        return
    @tornado.gen.coroutine
    def prepare(self):
        super().prepare()
        self.account = {}
        token = (self.get_args(['token']))['token']
        if token == None:
            self.account['id'] = 0
        else:
            err, data = yield from Service.User.get_user_basic_info_by_token(token)
            if err:
                self.account['id'] = 0
            else:
                self.account = data
        if self.request.method != 'GET':
            if self.account['id'] == 0:
                self.render(403, 'Permission Denied')
        id = self.account['id']
        err, self.account['power'] = yield from Service.User.get_user_power_info(id)
        err, self.group = yield from Service.User.get_user_group_info(id)
        err, self.current_group_power = yield from Service.User.get_user_group_power_info(id, self.current_group)
            

class WebRequestHandler(RequestHandler):
    def set_secure_cookie(self, name, value, expires_days=30, version=None, **kwargs):
        kwargs['httponly'] = True
        super().set_secure_cookie(name, value, expires_days, version, **kwargs)

    def write_error(self, status_code, **kwargs):
        self.Render('./err/'+str(status_code)+'.html')

    def Render(self, templ, **kwargs):
        kwargs['map_power'] = self.map_power
        kwargs['map_group_power'] = self.map_group_power
        kwargs['map_lang'] = self.map_lang
        kwargs['map_visible'] = map_visible
        kwargs['account'] = self.account
        kwargs['title'] = kwargs["title"] + " | NCTUOJ" if "title" in kwargs else "NCTUOJ"
        kwargs['group'] = self.group
        kwargs['current_group'] = self.current_group
        kwargs['current_group_power'] = self.current_group_power
        kwargs['current_group_active'] = self.current_group_active
        print("This function in req.py's render: ", kwargs)
        self.render('./web/template/'+templ, **kwargs)

    @tornado.gen.coroutine
    def prepare(self):
        super().prepare()
        ### No group => 0
        ### No user => 0 (guest)
        try:
            self.current_group_active = re.search(r'/group/\d+/(\w+)/.*', self.request.uri).groups(1)[0]
        except:
            self.current_group_active = "bulletins"

        self.account = {}
        self.group = {}
        try:
            id = self.get_secure_cookie('id').decode()
            err, data = yield from Service.User.get_user_basic_info(id)
            if err:
                id = 0
                self.clear_cookie('id')
            else:
                self.account = data
        except:
            id = 0
            self.clear_cookie('id')
        if id==0:
            self.account['token'] = ""
        self.account["id"] = id
        err, self.account['power'] = yield from Service.User.get_user_power_info(id)
        err, self.group = yield from Service.User.get_user_group_info(id)
        err, self.current_group_power = yield from Service.User.get_user_group_power_info(id, self.current_group)

        """ if the user not in the group render(403) """
        in_group = False
        for x in self.group:
            if x['id'] == int(self.current_group):
                in_group = True
        if not in_group and int(self.current_group) != 0:
            self.write_error(403)
            return
        

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

