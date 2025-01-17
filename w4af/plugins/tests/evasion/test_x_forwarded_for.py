"""
test_x_forwarded_for.py

Copyright 2013 Andres Riancho

This file is part of w4af, https://w4af.net/ .

w4af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w4af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w4af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import unittest

from w4af.core.data.parsers.doc.url import URL
from w4af.core.data.url.HTTPRequest import HTTPRequest
from w4af.core.data.dc.headers import Headers
from w4af.plugins.evasion.x_forwarded_for import x_forwarded_for


class TestXForwardedFor(unittest.TestCase):
    
    def test_no_modification(self):
        xff = x_forwarded_for()

        u = URL('http://www.w4af.com/')
        headers = Headers([('X-Forwarded-For', '127.0.0.1')])
        r = HTTPRequest(u, headers=headers)
        
        modified_request = xff.modify_request( r )
        modified_headers = modified_request.get_headers()
        
        self.assertIn('X-forwarded-for', modified_headers)
        self.assertEqual(modified_headers['X-forwarded-for'],
                         '127.0.0.1', modified_headers)

    def test_add_header(self):
        xff = x_forwarded_for()

        u = URL('http://www.w4af.com/')
        r = HTTPRequest(u)
        
        modified_request = xff.modify_request(r)
        modified_headers = modified_request.get_headers()
        
        self.assertIn('X-forwarded-for', modified_headers)
        self.assertEqual(modified_headers['X-forwarded-for'],
                         '164.29.7.190', modified_headers)
