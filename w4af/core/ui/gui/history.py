"""
history.py

Copyright 2007 Andres Riancho

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
import pickle
import msgpack
import operator
import os


class HistorySuggestion(object):
    """Handles the history of any text, providing suggestions.

    :param filename: Name of the file where the info is stored

    It's also responsible of loading and saving the info in a file.
    """
    def __init__(self, filename):
        # Where the history items will be stored
        self.filename = filename

        # dict: {text:points}
        self.history = {}

        if os.access(filename, os.R_OK):
            #
            # First we try to read using msgpack, which is the default
            # serialization algorithm we want to use
            #
            try:
                with open(filename, 'rb') as f:
                    self.history = msgpack.load(f, raw=False)
            except:
                #
                # The history file might still be in pickle format, we read
                # it and migrate to msgpack
                #
                try:
                    with open(filename, 'rb') as f:
                        self.history = pickle.load(f)
                except:
                    #
                    # Well... the file is completely broken, just write an
                    # empty string to it using msgpack to have a nicer run
                    # the next time the user executes the GUI
                    #
                    self.history = {}
                    with open(filename, 'wb') as f:
                        msgpack.dump({}, f)
                else:
                    #
                    # We were able to read using pickle, migrate the file to
                    # msgpack to prevent deserialization issues
                    # https://github.com/andresriancho/w3af/issues/17807
                    #
                    with open(filename, 'wb') as f:
                        msgpack.dump(self.history, f)

    def get_texts(self):
        """Provides the texts, ordered by relevance.

        :return: a generator with the texts
        """
        info = sorted(
            list(self.history.items()), key=operator.itemgetter(1), reverse=True)
        return [k for k, v in info]

    def insert(self, newtext):
        """Inserts new text to the history."""
        self.history[newtext] = self.history.get(newtext, 0) + 1

    def save(self):
        """Saves the history information."""
        fileh = open(self.filename, "wb")
        pickle.dump(self.history, fileh)
        fileh.close()


if __name__ == "__main__":
    import random
    import string
    import time

    QUANT = 5000
    LENGTH = 50
    print("Testing History with %d elements" % QUANT)

    arch = "test_history.pickle"
    if os.access(arch, os.F_OK):
        os.remove(arch)
    his = HistorySuggestion(arch)

    texts = ["".join(random.choice(
        string.ascii_letters) for x in range(LENGTH)) for y in range(QUANT)]

    print("Storing the elements:", end=' ')
    tini = time.time()
    for txt in texts:
        his.insert(txt)
    print("%.1f mseg/element" % ((time.time() - tini) * 1000 / QUANT))

    print("Saving to disk:", end=' ')
    tini = time.time()
    his.save()
    print("%.1f mseg" % ((time.time() - tini) * 1000))

    print("Loading from disk:", end=' ')
    tini = time.time()
    HistorySuggestion(arch)
    print("%.1f mseg" % ((time.time() - tini) * 1000))

    os.remove(arch)
