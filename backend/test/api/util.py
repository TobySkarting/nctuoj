import requests
import json

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
