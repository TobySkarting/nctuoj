import inspect
import re
import config
import hashlib
import datetime

def get_module_path(obj):
    path = inspect.getmodule(obj)
    path = re.match("<module '(.*)' from .*", str(path)).groups()[0]
    return (path, obj.__class__.__name__)

def HashPassword(x):
    hpwd = hashlib.sha512(str(x).encode()).hexdigest() + config.TORNADO_SETTING['password_salt']
    hpwd = hashlib.md5(str(x).encode()).hexdigest()
    return hpwd

def GenToken(account):
    token = []
    token.append(config.TOKEN['prefix'])
    token.append(hashlib.md5(account['account'].encode()).hexdigest()[:10])
    token.append(hashlib.md5((account['password'] + str(datetime.datetime.now())).encode()).hexdigest()[:40])
    return '@'.join(token)
