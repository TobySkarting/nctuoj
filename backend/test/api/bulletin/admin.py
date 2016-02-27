#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
from util import TestCase
import config
import common

class TestApiBulletinAdmin(TestCase):
    url = '%s/api/groups/1/bulletins/'%(config.base_url)
    urls = '%s/api/groups/1/bulletins/'%(config.base_url)
    another_url = '%s/api/groups/2/bulletins/'%(config.base_url)
    another_urls = '%s/api/groups/2/bulletins/'%(config.base_url)
    admin_token = common.get_user_info({'account': config.user_admin_account, 'passwd': config.user_admin_password})['token']

    def test_admin_get_bulletins(self):
        data = {
            "token": self.admin_token,
        }
        res = requests.get(self.urls, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_admin_post_bulletin(self):
        data = {
            "token": self.admin_token,
            "title": "admin test post",
            "content": "admin test content",
        }
        res = requests.post(self.urls, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, data=data)

    def test_admin_put_bulletin(self):
        pass
    def test_admin_delete_bulletin(self):
        pass
    def test_admin_post_another_bulletin(self):
        pass
    def test_admin_put_another_bulletin(self):
        pass
    def test_admin_delete_another_bulletin(self):
        pass
