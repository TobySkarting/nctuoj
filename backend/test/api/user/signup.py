#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
from util import TestCase
import config

class TestApiUserSignup(TestCase):
    url = "%s/api/users/signup/"%(config.base_url,)

    def test_user_signup(self):
        ### sign 'test'
        ### miss email
        data = {
            "account": config.user_test_account,
            "passwd": config.user_test_password,
            "rpasswd": config.user_test_password,
        }
        res = requests.post(self.url, data=data)
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": "",
            }
        }
        self.assertEqualR(res, expect_result)
        ### sign 'test' again
        ### 'test' delete 'test'
        ### 'admin' delete 'test'
        pass


"""
    def test_admin_login(self):
        data = {
            "account": config.user_admin_account,
            "passwd": config.user_admin_password,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 200,
            "body": {
                "msg": "",
            }
        }
        self.assertEqualR(res, expect_result)

    def test_no_exist_user_login(self):
        data = {
            "account": config.user_admin_account + str(datetime.datetime.now()),
            "passwd": str(datetime.datetime.now()),
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "User Not Exist",
            }
        }
        self.assertEqualR(res, expect_result)

    def test_forgot_fill_in_account(self):
        data = {
            "passwd": str(datetime.datetime.now()),
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "User Not Exist", 
            }
        }
        self.assertEqualR(res, expect_result)

    def test_forgot_fill_in_password(self):
        data = {
            "account": config.user_admin_account,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "Wrong Password",
            }
        }
        self.assertEqualR(res, expect_result)
"""
