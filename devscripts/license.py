#!/usr/bin/env python3

import os

stub = """

#
#    Tessera, an Open Source Bug Tracking / Ticketing system.
#    Mathew Robinson & Mark Chandler (c) 2016
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""

def update_licenses(directory):
    for entry in os.listdir("./"):
        if os.isfile(entry) and entry.endswith(".py"):
            with open(entry, "r+") as f:
                content = f.read()
                f.seek(0, 0)
                f.write(stub + content)
        if os.isdir(entry):
            update_licenses(entry)

if __name__ == "__main__":
    update_licenses("./")
