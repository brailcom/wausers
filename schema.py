### schema.py --- WAservice database schema

## Copyright (C) 2005, 2006 Brailcom, o.p.s.
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

# Class automatically gets these properties:
#   creation = Date()
#   activity = Date()
#   creator = Link('user')
#   actor = Link('user')

# IssueClass automatically gets these properties in addition to the Class ones:
#   title = String()
#   messages = Multilink("msg")
#   files = Multilink("file")
#   nosy = Multilink("user")
#   superseder = Multilink("issue")

# FileClass automatically gets this property in addition to the Class ones:
#   content = String()    [saved to disk in <tracker home>/db/files/]

## Tables

# Global users
user = Class (db, 'user',
              username=String (),
              password=Password (),
              address=String(),
              roles=String (),  # comma-separated string of Role names
              realname=String (),
              phone=String (),
              organisation=String (),
              alternate_addresses=String (),
              timezone=String (),
              )
user.setkey ('username')

# Projects
project = Class (db, 'project',
                 project=String (),
                 user=Link ('user'),
                 )
project.setkey ('project')

# Project logins
login = Class (db, 'login',
               project=Link ('project'),
               user=Link ('user'),
               login=String (),
               )

## Permissions
# Defined roles: Admin, User, Anonymous

# General access
for role in 'Admin', 'User', 'Anonymous':
    db.security.addPermissionToRole (role, 'Web Access')
# Users -- creation
db.security.addPermissionToRole ('Admin', 'Create', 'user')
properties=('username', 'password', 'address', 'realname', 'phone', 'organisation', 'alternate_addresses',)
db.security.addPermission (name='Create', klass='user', properties=properties)
# this doesn't seem to work reliably, access is granted to all properties
db.security.addPermissionToRole ('Anonymous', 'Create', classname='user', properties=properties)
# Users -- editing
properties = ('password', 'address', 'realname', 'phone', 'organisation', 'alternate_addresses',)
def permission_view_user (db, userid, itemid):
    return userid == itemid
def permission_edit_user (db, userid, itemid):
    return userid == itemid
db.security.addPermission (name='View', klass='user', check=permission_view_user)
db.security.addPermissionToRole ('User', 'View', classname='user', check=permission_view_user)
db.security.addPermission (name='Edit', klass='user', properties=properties,
                           check=permission_edit_user)
db.security.addPermissionToRole ('User', 'Edit', classname='user', properties=properties,
                                 check=permission_edit_user)
# Projects
db.security.addPermissionToRole ('User', 'Create', classname='project')
def permission_project (db, userid, itemid):
    return db.project.get (itemid, 'user') == userid
db.security.addPermission (name='View', klass='project', check=permission_project)
db.security.addPermissionToRole ('User', 'View', classname='project', check=permission_project)
db.security.addPermission (name='Edit', klass='project', properties=(), check=permission_project)
db.security.addPermissionToRole ('User', 'Edit', classname='project', properties=(), check=permission_project)
# Logins
def permission_view_login (db, userid, itemid):
    return (db.login.get (itemid, 'user') == userid or
            db.project.get (db.login.get (itemid, 'project'), 'user') == userid)
db.security.addPermission (name='View', klass='login', check=permission_view_login)
db.security.addPermissionToRole ('User', 'View', classname='login', check=permission_view_login)
