### login.py --- Special login functions

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


import urllib

import roundup.cgi.actions
import roundup.cgi.exceptions


class Login_Action (roundup.cgi.actions.LoginAction):
    
    def handle (self):
        roundup.cgi.actions.LoginAction.handle (self)
        try:
            redirect = self.form['__login_redirect'].value
        except:
            redirect = None
        if redirect:
            raise roundup.cgi.exceptions.Redirect, redirect


def redirlogin (db, request):
    try:
        redirect = request.form['__login_redirect'].value
        project = request.form['__login_project'].value
    except:
        redirect = project = None
    if redirect and project:
        project_url = db.config.TRACKER_WEB[:db.config.TRACKER_WEB[:-1].rfind('/')+1] + project + '/'
        userid = db.getuid ()
        for id in db.login.find (project=db.project.lookup (project), user=userid):
            login = db.login.get (id, 'login')
            if login != 'admin':
                break
        password = str (db.user.get (userid, 'password'))
        raise roundup.cgi.exceptions.Redirect (
            '%s?@action=login&__login_name=%s&__login_password=%s&__login_redirect=%s' %
            (project_url,
             urllib.quote_plus (login),
             urllib.quote_plus (password),
             urllib.quote_plus (redirect),))        
    return ''


def init (instance):
    instance.registerAction ('login', Login_Action)
    instance.registerUtil ('redirlogin', redirlogin)
