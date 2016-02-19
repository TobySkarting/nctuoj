#!/usr/bin/env python3
import sys
import requests
import json
import config
from util import TestCase
import unittest

class TestApiUserSign(TestCase):
    def test_user_admin_login(self):
        data = {
            "account": config.user_admin,
            "passwd": config.user_admin_password,
        }
        url = "%s/api/users/signin/"%(config.base_url,)
        r = requests.post(url, data=data)
        expect_result = {
            "status_code": 200,
            "body": {
                "msg": "",
                "status": 200,
            }
        }
        self.assertEqualR(r, expect_result)

