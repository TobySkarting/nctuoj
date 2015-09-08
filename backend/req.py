import json
import logging
import types
import datetime
import collections
import tornado.template
import tornado.gen
import tornado.web
import tornado.websocket
import datetime
import re
from map import *
import config
import markdown as markdown

def md(s):
    if s is None: s = ''
    return markdown.markdown(s)

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
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
        msg = '<USER %d> %s' % (id, str(msg))
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
                    meta[n] = self.get_argument(n)
            except:
                meta[n] = None
                print("get_args error: ", n)
        return meta

    @tornado.gen.coroutine
    def prepare(self):
        try:
            self.current_group = int(re.search(r'.*/group/(\d+).*', self.request.uri).groups(1)[0])
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
            if self.account['id'] == 0 and self.request.uri not in config.API_URI_WITHOUT_SIGNIN:
                self.render(403, 'Permission Denied')
                return
        id = self.account['id']
        err, self.account['power'] = yield from Service.User.get_user_power_info(id)
        err, self.group = yield from Service.User.get_user_group_info(id)
        err, self.current_group_power = yield from Service.User.get_user_group_power_info(id, self.current_group)

        in_group = False
        for x in self.group:
            if x['id'] == self.current_group:
                in_group = True
        if not in_group and self.current_group != 0:
            self.render(403, 'Permission Denied')
            return
            

class WebRequestHandler(RequestHandler):
    def set_secure_cookie(self, name, value, expires_days=30, version=None, **kwargs):
        kwargs['httponly'] = True
        super().set_secure_cookie(name, value, expires_days, version, **kwargs)

    def write_error(self, status_code, err=None, **kwargs):
        kwargs['err'] = err
        self.Render('./err/'+str(status_code)+'.html', **kwargs)

    def Render(self, templ, **kwargs):
        kwargs['md'] = md
        kwargs['map_power'] = self.map_power
        kwargs['map_group_power'] = self.map_group_power
        kwargs['map_lang'] = self.map_lang
        kwargs['map_visible'] = map_visible
        kwargs['account'] = self.account
        kwargs['title'] = kwargs["title"] + " | NCTUOJ" if "title" in kwargs else "NCTUOJ"
        kwargs['group'] = self.group
        kwargs['current_contest'] = self.current_contest
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
            id = int(self.get_secure_cookie('id').decode())
            err, data = yield from Service.User.get_user_basic_info(id)
            if err:
                id = 0
                self.clear_cookie('id')
            else:
                self.account = data
        except:
            id = 0
            self.clear_cookie('id')
        if id == 0:
            self.account['token'] = ""
        self.account["id"] = id
        err, self.current_contest = yield from Service.User.get_user_current_contest(id)
        err, self.account['power'] = yield from Service.User.get_user_power_info(id)
        err, self.group = yield from Service.User.get_user_group_info(id)
        err, self.current_group_power = yield from Service.User.get_user_group_power_info(id, self.current_group)

        """ if the user not in the group render(403) """
        in_group = self.current_group in (x['id'] for x in self.group)
        if not in_group and self.current_group != 0:
            self.write_error(403)
            return
        
        if self.current_contest:
            if re.search(r'/group/\d+/contests/(\w*)/', self.request.uri) is None:
                self.redirect('/group/%s/contests/%s/'%(str(self.current_contest['group_id']), str(self.current_contest['id'])))



        

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def reqenv(func):
    @tornado.gen.coroutine
    def wrap(self,*args,**kwargs):
        ret = func(self,*args,**kwargs)
        if isinstance(ret,types.GeneratorType):
            ret = yield from ret
        return ret
    return wrap
