#!/usr/bin/env python
#-*- coding:utf-8 -*-

import BaseHTTPServer
import hashlib
import os
import urllib2
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

class CacheHandler(BaseHTTPServer.BaseHTTPRequestHandler):
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
        if self.path == "/url":
            page = self.create_page(r'v2ray url')
            self.send_page(page)
        elif self.path == "/ssinfo":
            page = self.create_page(r'v2ray ssinfo')
            self.send_page(page)

    def send_page(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def create_page(self, cmd):
        page = self.start + self.get_url(cmd) + self.end
        return page

    def get_url(self, cmd):
        with os.popen(cmd, 'r') as f:
            text = f.read().decode('utf8')
            url=re.sub(r'\033\[\d{1,2}m', "", text)
            return url

def run():
    server_address = ('', 80)
    httpd = BaseHTTPServer.HTTPServer(server_address, CacheHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
