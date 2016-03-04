#!/usr/bin/env python3
from api.user.signin import TestApiUserSignin
from api.user.signup import TestApiUserSignup
from api.bulletin.admin import TestApiBulletinAdmin
from api.bulletin.user import TestApiBulletinUser
from api.bulletin.guest import TestApiBulletinGuest
from api.problem.admin import TestApiProblemAdmin
from api.problem.user import TestApiProblemUser
from api.problem.guest import TestApiProblemGuest
import subprocess as sp
import unittest
if __name__ == '__main__':
    ###
    # init db
    sp.call("./init_db.sh", shell=True)
    print('==========================================')
    unittest.main()
