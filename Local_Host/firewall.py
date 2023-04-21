#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 03:25:29 2023

@author: ericwei
"""

import http.server
import urllib.parse
import requests

class FirewallProxy(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.allowed_ips = ['127.0.0.1', '192.168.1.100']  # Replace with the IP addresses you want to allow
        super().__init__(*args, **kwargs)

    def do_GET(self):
        client_ip = self.client_address[0]
        if client_ip not in self.allowed_ips:
            self.send_error(403)  # Forbidden
            return

        self.send_response(200)
        self.end_headers()

        target_url = urllib.parse.urljoin('http://127.0.0.1:5000', self.path[1:])
        response = requests.get(target_url)
        self.wfile.write(response.content)

if __name__ == '__main__':
    port = 1005  # Set a fixed port number, or use input("Enter the port number: ") to get it from the user
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, FirewallProxy)
    print(f"Firewall is running on port {port}")
    httpd.serve_forever()

