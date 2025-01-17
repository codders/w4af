"""
multi_in.py

Copyright 2017 Andres Riancho

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
from acora import AcoraBuilder
from w4af.core.data.constants.encodings import DEFAULT_ENCODING
from w4af.core.data.misc.encoding import smart_unicode


class MultiIn(object):
    def __init__(self, keywords_or_assoc):
        """
        :param keywords_or_assoc: A list with all the strings that we want
        to match against one or more strings using the "query" function.

        This list might be:
            [str_1, str_2 ... , str_N]

        Or something like:
            [(str_1, obj1) , (str_2, obj2) ... , (str_N, objN)].

        In the first case, if a match is found this class will return:
            [str_N,]

        In the second case we'll return
            [[str_N, objN],]
        """
        self._keywords_or_assoc = keywords_or_assoc
        self._translator = dict()
        self._acora = self._build()

    def _build(self):
        builder = AcoraBuilder()

        for idx, item in enumerate(self._keywords_or_assoc):

            if isinstance(item, tuple):
                keyword = item[0]
                keyword = keyword.encode(DEFAULT_ENCODING)

                if keyword in self._translator:
                    raise ValueError('Duplicated keyword "%s"' % keyword)

                self._translator[keyword] = item[1:]

                builder.add(keyword)
            elif isinstance(item, str):
                keyword = item.encode(DEFAULT_ENCODING)
                builder.add(keyword)
            elif isinstance(item, bytes):
                builder.add(item)
            else:
                raise ValueError('Can NOT build MultiIn with provided values.')

        return builder.build()

    def query(self, target_str):
        """
        Run through all the keywords and identify them in target_str

        :param target_str: The target string where the keywords need to be match
        :yield: The matches (see __init__)
        """
        target_was_string = False
        if isinstance(target_str, str):
            target_was_string = True
            target_str = target_str.encode(DEFAULT_ENCODING)

        def unwrap(output):
            if target_was_string:
                if isinstance(output, bytes):
                    return output.decode("utf-8")
                elif isinstance(output, list):
                    return [ unwrap(a) for a in output ]
                return output

        seen = set()

        for match, position in self._acora.finditer(target_str):
            if match in seen:
                continue

            seen.add(match)
            extra_data = self._translator.get(match, None)

            if extra_data is None:
                yield unwrap(match)
            else:
                all_data = [match]
                all_data.extend(extra_data)
                yield unwrap(all_data)
