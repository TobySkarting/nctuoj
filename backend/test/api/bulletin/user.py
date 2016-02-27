#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
from util import TestCase
import config
import common

class TestApiBulletinUser(TestCase):
    url = '%s/api/groups/1/bulletins/'%(config.base_url)
    urls = '%s/api/groups/1/bulletins/'%(config.base_url)
    another_url = '%s/api/groups/2/bulletins/'%(config.base_url)
    another_urls = '%s/api/groups/2/bulletins/'%(config.base_url)
    user_token = common.get_user_info({'account': config.user_test_account, 'passwd': config.user_test_password})['token']


    def test_user_get_bulletins(self):
        data = {
            "token": self.user_token,
        }
        res = requests.get(self.urls, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_user_post_bulletin(self):
        data = {
            "token": self.user_token,
            "title": "user test post",
        }

        pass
    def test_user_put_bulletin(self):
        pass
    def test_user_delete_bulletin(self):
        pass
    def test_user_post_another_bulletin(self):
        pass
    def test_user_put_another_bulletin(self):
        pass
    def test_user_delete_another_bulletin(self):
        pass

