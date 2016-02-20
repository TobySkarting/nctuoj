#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
sys.path.append("./../")
import config

class TestApiUserSign(unittest.TestCase):
    url = "%s/api/users/signin/"%(config.base_url,)
    def test_user_login(self):
        url = "%s/api/users/signin/"%(config.base_url,)
        ### admin login
        data = {
            "account": config.user_admin_account,
            "passwd": config.user_admin_password,
        }
        res = requests.post(url, data=data)
        expect_result = {
            "msg": "",
        }
        self.assertEqual(json.loads(res.text), expect_result)
        self.assertEqual(res.status_code, 200)

        ### no exist user login
        data = {
            "account": config.user_admin_account + str(datetime.datetime.now()),
            "passwd": str(datetime.datetime.now()),
        }
        res = requests.post(url, data=data)
        expect_result = {
            "msg": "User Not Exist",
        }
        self.assertEqual(json.loads(res.text), expect_result)
        self.assertEqual(res.status_code, 403)

        ### error password
        data = {
            "account": config.user_admin_account,
            "passwd": str(datetime.datetime.now()),
        }
        res = requests.post(url, data=data)
        expect_result = {
            "msg": "Wrong Password",
        }
        self.assertEqual(json.loads(res.text), expect_result)
        self.assertEqual(res.status_code, 403)

        ### forgot fill in account
        data = {
            "passwd": str(datetime.datetime.now()),
        }
        res = requests.post(url, data=data)
        expect_result = {
            "msg": "User Not Exist", 
        }
        self.assertEqual(json.loads(res.text), expect_result)
        self.assertEqual(res.status_code, 403)

        ### forgot fill in password
        data = {
            "account": config.user_admin_account
        }
        res = requests.post(url, data=data)
        expect_result = {
            "msg": "Wrong Password",
        }
        self.assertEqual(json.loads(res.text), expect_result)
        self.assertEqual(res.status_code, 403)

unittest.main()
