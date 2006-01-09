### waauth.py --- User authentication

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

import roundup.instance


if False:
    import os
    def _global_user_name (tracker_home):
        tracker = roundup.instance.open (tracker_home)
        client = tracker.Client (tracker, None, os.environ)
        client.determine_user ()
        return client.user

def _validate_login (project, login, password, tracker_home):
    tracker = roundup.instance.open (tracker_home)
    db = tracker.open ()
    try:
        project_id = db.project.lookup (project)
    except KeyError:
        return False
    for login_id in db.login.find (project=project_id):
        if db.login.get (login_id, 'login') == login:
            user_id = db.login.get (login_id, 'user')
            db_password = db.user.get (user_id, 'password')
            if password == db_password or password == str (db_password):
                return True
            else:
                return False
    return False

def authenticate (project, requested_user_name, password, tracker_home):
    if requested_user_name == 'anonymous':
        return True
    return _validate_login (project, requested_user_name, password, tracker_home)

def _modify_user (project, login, user, tracker_home, action):
    tracker = roundup.instance.open (tracker_home)
    db = tracker.open ()
    try:
        project_id = db.project.lookup (project)
    except KeyError:
        return "No such project: %s" % (project,)
    try:
        user_id = db.user.lookup (user)
    except KeyError:
        return "No user `%s'" % (user,)
    db.setCurrentUser ('admin')
    action (db, project_id, user_id, login)
    db.commit ()
    return None

def add_user (project, login, user, tracker_home):
    def action (db, project_id, user_id, login):
        db.login.create (project=project_id, user=user_id, login=login)
    return _modify_user (project, login, user, tracker_home, action)

def check_user (user, tracker_home):
    tracker = roundup.instance.open (tracker_home)
    db = tracker.open ()
    try:
        user_id = db.user.lookup (user)
    except KeyError:
        return False
    return True

def remove_user (project, login, user, tracker_home):
    def action (db, project_id, user_id, login):
        for id in db.login.find (user=user_id, project=project_id):
            if db.login.get (id, 'login') == login:
                db.login.retire (id)
                break
        else:
           return "No corresponding login entry found"
    return _modify_user (project, login, user, tracker_home, action)
