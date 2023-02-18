"""
test_plugins.py

Copyright 2023 Arthur Taylor

This file is part of w4af, https://w4af.net/ .

w4af is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import pytest

from w4af.core.ui.console.console_ui import ConsoleUI
from w4af.core.ui.console.tests.helper import ConsoleTestHelper


@pytest.mark.smoke
class TestPluginsConsoleUI(ConsoleTestHelper):
    """
    Plugins configuration test for the console UI.
    """
    def test_enable_all_plugins(self):
        commands_to_run = ['plugins audit all',
                           'plugins list audit enabled',
                           'exit']

        self.console = ConsoleUI(commands=commands_to_run, do_upd=False)
        self.console.sh()

        assert_result, msg = self.all_expected_substring_in_output("blind_sqli")
        self.assertTrue(assert_result, msg)

