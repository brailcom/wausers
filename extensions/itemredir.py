### itemredir.py --- Changes to standard redirections after editing items

## Copyright (C) 2006 Brailcom, o.p.s.
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

import roundup.cgi.actions
import roundup.cgi.client
import roundup.cgi.exceptions


class New_Item_Action (roundup.cgi.actions.NewItemAction):

    def handle (self):
        try:
            roundup.cgi.actions.NewItemAction.handle (self)
        except roundup.cgi.exceptions.Redirect, e:
            if self.classname == 'project':
                raise roundup.cgi.exceptions.Redirect, '%shome' % (self.base,)
            else:
                raise e

class Retire_Action (roundup.cgi.actions.RetireAction):

    def handle (self):
        roundup.cgi.actions.RetireAction.handle (self)
        if self.classname == 'project':
            raise roundup.cgi.exceptions.Redirect, '%shome' % (self.base,)

    def hasPermission (self, permission, classname=roundup.cgi.actions.RetireAction._marker, itemid=None):
        if itemid is None:
            itemid = self.nodeid
        return roundup.cgi.actions.RetireAction.hasPermission (self, permission, classname, itemid)


def init (instance):
    instance.registerAction ('new', New_Item_Action)
    instance.registerAction ('retire', Retire_Action)
