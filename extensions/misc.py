### misc.py --- Miscellaneous functions for use in page templates

## Copyright (C) 2005 Brailcom, o.p.s.
##
## Author: Milan Zamazal <pdm@brailcom.org>
##
## COPYRIGHT NOTICE
##
## This program is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by the Free
## Software Foundation; either version 2 of the License, or (at your option)
## any later version.
##
## This program is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
## FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
## more details.
##
## You should have received a copy of the GNU General Public License along with
## this program; if not, write to the Free Software Foundation, Inc.,
## 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import re

def transform_message (db, message):
    match = re.match ('^([A-Za-z]+) ([0-9]+) (created|has been retired)$', message)
    if match:
        classname = match.group (1).lower ()
        id = match.group (2)
        try:
            class_ = getattr (db, classname)
            name = class_.get (id, class_.getkey ())
        except:
            name = None
        if name:
            message = match.group (1) + ' ' + name + ' ' + match.group (3)
    return message

def init (instance):
    instance.registerUtil ('transform_message', transform_message)
