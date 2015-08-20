import tornado.web
import urllib
import math
class Pagination(tornado.web.UIModule):
    def render(self, page):
        for x in page['get']:
            if not page['get'][x]:
                page['get'][x] = ""
        page['urls'] = {}
        start = max(1, int(page['current']) - 5)
        end = min(int(page['current']) + 5, int(page['total'])) + 1
        _prev = max(1, int(page['current']) - 1)
        _next = min(int(page['current'])+1, int(page['total']))
        for x in range(start, end):
            page['get']['page'] = x
            page['urls'][x] = page['url'] + '?' + urllib.parse.urlencode(page['get'])
        page['range'] = (start, end)
        page['get']['page'] = _prev
        page['urls']['prev'] = page['url'] + '?' + urllib.parse.urlencode(page['get'])
        page['get']['page'] = _next
        page['urls']['next'] = page['url'] + '?' + urllib.parse.urlencode(page['get'])
        return self.render_string('./template/modules/pagination.html', page=page)

