### user.py --- User auditors

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

from roundup.exceptions import Reject

import re

def audit_user (db, c, nodeid, newvalues):
    if newvalues.get ('username') not in ('admin', 'anonymous',):
        newvalues['roles'] = 'User'
    username = newvalues.get ('username')
    if not username:
        Reject ("Username may not be empty")
    if not re.match ('^[a-z]+$', username):
        Reject ("Only lowercase English letters allowed in username")

def audit_password (db, c, nodeid, newvalues):
    if newvalues and not newvalues.get ('password', 'dummy'):
        del newvalues['password']

def init (db):
    db.user.audit ('create', audit_user)
    db.user.audit ('set', audit_password)
