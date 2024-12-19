#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import hashlib
import os
import urllib.request
import urllib.parse
import sys
import re

class CacheHandler(http.server.BaseHTTPRequestHandler):
    Page = '''\
        <html>
        <body>
        <div style='white-space: pre-line;'>
            {url}
        </div>
        </body>
        </html>
        '''

    start = '''\
            <html>
            <body>
            <div style='white-space: pre-line;'>
            '''
    end = '''\
            </div>
            </body>
            </html>
            '''
    def do_GET(self):
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        user_id = query_components.get('id', [None])[0]
        user_pw = query_components.get('pw', [None])[0]
        print(f"id:{user_id}, pw:{user_pw}")
        if user_id != "id666" or user_pw!="pw888":
            return  self.send_page("拒绝访问")
        if "/url" in self.path:
            page = self.create_page('v2ray url')
            self.send_page(page)
        elif "/ssinfo" in self.path:
            page = self.create_page('v2ray ssinfo')
            self.send_page(page)

    def send_page(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))

    def create_page(self, cmd):
        page = self.start + self.get_url(cmd) + self.end
        return page

    def get_url(self, cmd):
        with os.popen(cmd, 'r') as f:
            text = f.read()
            url = re.sub(r'\033\[\d{1,2}m', "", text)
            return url

def run():
    server_address = ('', 80)
    httpd = http.server.HTTPServer(server_address, CacheHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
