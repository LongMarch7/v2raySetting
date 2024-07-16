#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import hashlib
import os
import urllib.request
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
        if self.path == "/url":
            page = self.create_page('v2ray url')
            self.send_page(page)
        elif self.path == "/ssinfo":
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
