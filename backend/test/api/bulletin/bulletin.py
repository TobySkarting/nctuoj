#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
from util import TestCase
import config
import common

class TestApiBulletin(TestCase):
    url = '%s/api/groups/1/bulletins/'%(config.base_url)
    urls = '%s/api/groups/1/bulletins/'%(config.base_url)
    another_url = '%s/api/groups/2/bulletins/'%(config.base_url)
    another_urls = '%s/api/groups/2/bulletins/'%(config.base_url)
    admin_token = common.get_user_info({'account': config.user_admin_account, 'passwd': config.user_admin_password})['token']
    user_token = common.get_user_info({'account': config.user_test_account, 'passwd': config.user_test_password})['token']

    def test_admin_get_bulletins(self):
        print(self.admin_token)
        data = {
            "token": self.admin_token,
        }
        res = requests.get(self.urls, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    """
    def test_admin_post_bulletin(self):
        data = {
            "token": self.admin_token,
            "title": "test post",
            "content": "test content",
        }
        res = requests.post(self.urls, data=data)
        res.connection.close()
        print(res.status_code, res.text)
    """



    def test_user_post_bulletin(self):
        pass
    def test_admin_put_bulletin(self):
        pass
    def test_user_put_bulletin(self):
        pass
    def test_admin_delete_bulletin(self):
        pass
    def test_user_delete_bulletin(self):
        pass
    def test_admin_post_another_bulletin(self):
        pass
    def test_user_post_another_bulletin(self):
        pass
    def test_admin_put_another_bulletin(self):
        pass
    def test_user_put_another_bulletin(self):
        pass
    def test_admin_delete_another_bulletin(self):
        pass
    def test_user_delete_another_bulletin(self):
        pass

