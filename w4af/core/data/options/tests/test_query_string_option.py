"""
test_query_string_option.py

Copyright 2018 Andres Riancho

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

from w4af.core.controllers.exceptions import BaseFrameworkException
from w4af.core.data.options.opt_factory import opt_factory
from w4af.core.data.options.option_types import QUERY_STRING


class TestQueryStringOption(unittest.TestCase):

    def test_valid_qs(self):
        value = 'abc=1&def=2'
        opt = opt_factory('name', value, 'desc', QUERY_STRING, 'help', 'tab')

        self.assertEqual(opt.get_value_for_profile(), value)

        qs_instance = opt.get_value()

        self.assertIn(b'abc', qs_instance)
        self.assertIn(b'def', qs_instance)

        self.assertEqual(qs_instance[b'abc'], [b'1'])
        self.assertEqual(qs_instance[b'def'], [b'2'])

    def test_empty_qs(self):
        value = ''
        opt = opt_factory('name', value, 'desc', QUERY_STRING, 'help', 'tab')

        self.assertEqual(opt.get_value_for_profile(), value)

        qs_instance = opt.get_value()
        self.assertEqual(len(qs_instance), 0)

    def test_invalid_qs(self):
        value = 1
        self.assertRaises(BaseFrameworkException, opt_factory, 'name', value,
                          'desc', QUERY_STRING, 'help', 'tab')
