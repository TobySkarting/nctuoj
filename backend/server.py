### tornado 
import tornado.ioloop
import tornado.httpserver
import tornado.web

### self define
from req import RequestHandler
from req import reqenv
from req import Service

### my app
import config
import mysql
import myredis

### built-in module
import time
import signal
import logging

### service class
from service.user import UserService
from service.problem import ProblemService
from service.bulletin import BulletinService
### api class from api.user import ApiUserSignupHandler
from api.user import ApiUserSigninHandler
from api.user import ApiUserChangePasswordHandler
from api.user import ApiUserLogoutHandler
from api.user import ApiUserInfoHandler
from api.user import ApiUserListHandler


### web class
from web.err import Web404Handler
from web.index import WebIndexHandler
from web.bulletin import WebBulletinsHandler
from web.bulletin import WebBulletinHandler
from web.problem import WebProblemsHandler
from web.problem import WebProblemHandler
from web.submission import WebSubmissionsHandler
from web.contest import WebContestsHandler

from web.user import WebUsersHandler
from web.user import WebUserSignHandler
from web.user import WebUserHandler
#from web.problem import WebProblemHandler
#from web.problem import WebProblemListHandler

def sig_handler(sig, frame):
    print('catch stop signal')
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    print('stopping server')
    srv.stop()
    io_loop = tornado.ioloop.IOLoop.instance()
    deadline = time.time() + config.MAX_WAIT_SECOND_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            print('Shutdown')
    stop_loop()



if __name__ == '__main__':
    '''
    logging.basicConfig(level=logging.DEBUG,
            format='[%(asctime)s]: %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename=config.LOG_FILE_PATH,
            filemode='a')
    '''
    db = mysql.AsyncMysql(user=config.DBUSER,
            database=config.DBNAME,
            passwd=config.DBPASSWORD,
            host=config.DBHOST)
    rs = myredis.MyRedis(db=1)

    app = tornado.web.Application([
        ('/', WebIndexHandler),
        ### api handler
        #('/api/user/signup/', ApiUserSignupHandler),
        #('/api/user/signin/', ApiUserSigninHandler),
        #('/api/user/logout/', ApiUserLogoutHandler),
        #('/api/user/(\d+)/change_password/', ApiUserChangePasswordHandler),
        #('/api/user/(\d+)/', ApiUserInfoHandler),           # get => info post => modify
        #('/api/user/', ApiUserListHandler),
        ### bulletin
        ('/group/(\d+)/bulletins/',                 WebBulletinsHandler),
        ('/group/(\d+)/bulletins/(\d+)/(\w*/?)',    WebBulletinHandler),
        ('/group/(\d+)/problems/',                  WebProblemsHandler),
        ('/group/(\d+)/submissions/',               WebSubmissionsHandler),
        ('/group/(\d+)/contests/',                  WebContestsHandler),

        ###""" problem handler
        ### user handler
        ('/users/', WebUsersHandler),
        ('/user/', WebUserHandler),
        ('/user/(sign\w*)/?', WebUserSignHandler),
        ('/user/(\d+)/(\w*)/?', WebUserHandler),
        ### web handler
        ('/asset/(.*)', tornado.web.StaticFileHandler, {'path': '../http'}),
        ('/.*', Web404Handler)
        ], cookie_secret=config.COOKIE_SECRET, autoescape='xhtml_escape')
    global srv
    srv = tornado.httpserver.HTTPServer(app)
    srv.listen(config.PORT)
    Service.User = UserService(db, rs)
    Service.Problem = ProblemService(db, rs)
    Service.Bulletin = BulletinService(db, rs)
    print('start')
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    tornado.ioloop.IOLoop().instance().start()
