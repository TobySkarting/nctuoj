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

# def user_login_test():

    # ### try user login
    # data = {
        # "account": config.user_admin,
        # "passwd": config.user_admin_password,
    # }
    # url = "%s/api/users/signin/"%(config.base_url,)
    # result = requests.post(url, data=data)
    # expect_result = {
        # "status_code": 200,
        # "text": {
            # "msg": "",
            # "status": 200,
        # }
    # }
    # util.test("Normal User Login", url, data, expect_result)

    # ### try error password
    # data['account'] = "nothisuser"
    # result = util.test("No Exist User Login", url, data)
    # print(result.status_code, result.text)


    

# if __name__ == "__main__":
    # user_login_test()
