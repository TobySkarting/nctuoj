#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
sys.path.append("./../")
import config

class TestApiUserSign(unittest.TestCase):
    def test_user_register(self):
        url = "%s/api/users/signup/"%(config.base_url,)
        ### admin login
        data = {
            "email": "",
            "account": "",
            "passwd": config.user_admin,
            "repasswd": config.user_admin_password,
        }
        res = requests.post(url, data=data)
        expect_result = {
            "msg": "",
        }
        self.assertEqual(json.loads(res.text), expect_result)
        self.assertEqual(res.status_code, 200)


unittest.main()
