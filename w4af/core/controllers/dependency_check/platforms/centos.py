"""
centos.py

Copyright 2014 Andres Riancho

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
import distro

from .fedora import Fedora
from ..requirements import CORE, GUI


class CentOS(Fedora):
    SYSTEM_NAME = 'CentOS'
    PKG_MANAGER_CMD = 'sudo yum install'
    PIP_CMD = 'pip-python'

    CORE_SYSTEM_PACKAGES = ['python-pip','npm', 'python-devel', 'python-setuptools',
                            'libsqlite3x-devel', 'gcc-c++', 'gcc', 'make',
                            'git', 'libxml2-devel', 'libxslt-devel',
                            'pyOpenSSL', 'openssl-devel', 'libcom_err-devel',
                            'libcom_err', 'libffi-devel']

    GUI_SYSTEM_PACKAGES = CORE_SYSTEM_PACKAGES[:]
    GUI_SYSTEM_PACKAGES.extend(['graphviz', 'gtksourceview2', 'pygtksourceview',
                                'pywebkitgtk'])

    SYSTEM_PACKAGES = {CORE: CORE_SYSTEM_PACKAGES,
                       GUI: GUI_SYSTEM_PACKAGES}

    @staticmethod
    def is_current_platform():
        return 'redhat' in distro.id()
