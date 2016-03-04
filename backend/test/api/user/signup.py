#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
from util import TestCase
import common
import config

class TestApiUserSignup(TestCase):
    url = "%s/api/users/signup/"%(config.base_url,)

    def test_account(self):
        data = {
            'email': config.user_test_email,
            'passwd': config.user_test_password,
            'rpasswd': config.user_test_password,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'account not in form',
            }
        }
        self.assertEqualR(res, expect_result)

        data['account'] = ''
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'value of account: "" should not be empty value',
            }
        }
        self.assertEqualR(res, expect_result)

    def test_email(self):
        data = {
            "account": config.user_test_account,
            "passwd": config.user_test_password,
            "repasswd": config.user_test_password,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'email not in form',
            }
        }
        self.assertEqualR(res, expect_result)

        data['email'] = ''
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'value of email: "" should not be empty value',
            }
        }
        self.assertEqualR(res, expect_result)


    def test_passwd(self):
        data = {
            'email': config.user_test_email,
            'account': config.user_test_account,
            'rpasswd': config.user_test_password,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'passwd not in form',
            }
        }
        self.assertEqualR(res, expect_result)

        data['passwd'] = ''
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'value of passwd: "" should not be empty value',
            }
        }
        self.assertEqualR(res, expect_result)

    def test_repasswd(self):
        data = {
            'email': config.user_test_email,
            'account': config.user_test_account,
            'passwd': config.user_test_password,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'repasswd not in form',
            }
        }
        self.assertEqualR(res, expect_result)

        data['repasswd'] = ''
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'value of repasswd: "" should not be empty value',
            }
        }
        self.assertEqualR(res, expect_result)

    def test_passwd_and_repasswd(self):
        data = {
            'email': config.user_test_email,
            'account': config.user_test_account,
            'passwd': config.user_test_password,
            'repasswd': config.user_test_password + str(datetime.datetime.now()),
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'Confirm Two Password',
            }
        }
        self.assertEqualR(res, expect_result)

    def test_user_signup(self):
        ### if exist test account remove it
        data = {
            "account": config.user_test_account,
            "passwd": config.user_test_password,
        }
        res = requests.post("%s/api/users/signin/"%(config.base_url), data=data)
        res.connection.close()
        if res.status_code == 200:
            admin_info = common.get_user_info({'account': config.user_admin_account, 'passwd': config.user_admin_password})
            test_info = common.get_user_info({'account': config.user_test_account, 'passwd': config.user_test_password})
            delete_url = '%s/api/users/%s/'%(config.base_url, test_info['id'])
            data = {
                'token': admin_info['token']
            }
            res = requests.delete(delete_url, data=data)
            res.connection.close()

        ### sign 'test'
        data = {
            'email': config.user_test_email,
            'account': config.user_test_account,
            'passwd': config.user_test_password,
            'repasswd': config.user_test_password,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 200,
            "body": {
                "msg": '',
            }
        }
        self.assertEqualR(res, expect_result)
        ### sign 'test' account again
        data = {
            'email': config.user_test_email + str(datetime.datetime.now()),
            'account': config.user_test_account,
            'passwd': config.user_test_password,
            'repasswd': config.user_test_password,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'Account Exist',
            }
        }
        self.assertEqualR(res, expect_result)
        ### sign 'test' email again
        data = {
            'email': config.user_test_email,
            'account': config.user_test_account + str(datetime.datetime.now()),
            'passwd': config.user_test_password,
            'repasswd': config.user_test_password,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'Email Exist',
            }
        }
        self.assertEqualR(res, expect_result)
        ### 'test' delete 'test'
        admin_info = common.get_user_info({'account': config.user_admin_account, 'passwd': config.user_admin_password})
        test_info = common.get_user_info({'account': config.user_test_account, 'passwd': config.user_test_password})
        delete_url = '%s/api/users/%s/'%(config.base_url, test_info['id'])
        data = {
            'token': test_info['token']
        }
        res = requests.delete(delete_url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": 'Permission Denied',
            }
        }
        self.assertEqualR(res, expect_result)
        ### 'admin' delete 'test'
        admin_info = common.get_user_info({'account': config.user_admin_account, 'passwd': config.user_admin_password})
        test_info = common.get_user_info({'account': config.user_test_account, 'passwd': config.user_test_password})
        delete_url = '%s/api/users/%s/'%(config.base_url, test_info['id'])
        data = {
            'token': admin_info['token']
        }
        res = requests.delete(delete_url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 200,
            "body": {
                "msg": {
                    'id': str(test_info['id'])
                },
            }
        }
        self.assertEqualR(res, expect_result)
        ### 'test' signup again
        data = {
            'email': config.user_test_email,
            'account': config.user_test_account,
            'passwd': config.user_test_password,
            'repasswd': config.user_test_password,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 200,
            "body": {
                "msg": '',
            }
        }
        self.assertEqualR(res, expect_result)
