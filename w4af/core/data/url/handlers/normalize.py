"""
normalize.py

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
import urllib.request, urllib.error, urllib.parse


class NormalizeHandler(urllib.request.BaseHandler):
    """
    Make sure that the HTTP request has some "required" headers.
    """

    handler_order = urllib.request.HTTPErrorProcessor.handler_order - 1

    def http_request(self, request):
        #
        # FIXME: What if the user doesn't want to add these headers?
        #
        if not request.has_header('Host'):
            request.add_unredirected_header('Host', request.host)

        if not request.has_header('Accept-encoding'):
            request.add_unredirected_header('Accept-Encoding', 'identity')

        return request
    
    https_request = http_request
