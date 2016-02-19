import requests
import json
import unittest
class TestCase(unittest.TestCase):
    def assertEqualR(self, r, data={}, json_equal=True):
        self.assertEqual(r.status_code, int(data['status_code']))
        body = r.text
        if json_equal: body = json.loads(body)
        self.assertEqual(body, data['body'])

def test(name, url, data, expect_result = None):
    result = requests.post(url, data=data)
    print("Test: ", name)
    print("URL: ", url)
    print("data: ", data)
    print("Result: ", result, result.text)
    if expect_result is not None:
        print("Expect Result: <%s>"%expect_result['status_code'], expect_result['text'])
        assert(result.status_code == expect_result['status_code'])
        assert(json.loads(result.text) == expect_result['text'])
    return result
