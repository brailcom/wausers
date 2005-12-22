### project.py --- Project auditors

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
import roundup.init
import roundup.instance
import roundup.password

import os
import re

def _audit_project (db, c, nodeid, newvalues):
    name = newvalues.get ('project')
    if not name:
        raise Reject ("Project name not given")
    if not re.match ('^[a-z]+$', name):
        raise Reject ("Only lowercase English letters allowed in the project name")

def _make_project (db, c, nodeid, newvalues):
    name = newvalues['project']
    # Create project directory
    project_directory = os.path.join (os.path.dirname (db.config.HOME), name)
    try:
        os.mkdir (project_directory)
    except OSError:
        return "Project name <em>%s</em> is already taken" % (name,)
    # Create the project
    try:
        # Create project directory
        template = 'waassistant'
        template_directory = os.path.dirname (project_directory)
        templates = roundup.init.listTemplates (template_directory)
        if not templates.has_key (template):
            raise Exception ("Template `waassistant' unavailable")
        roundup.init.install (project_directory, templates[template]['path'])
        # Update config file
        url = os.path.dirname (os.path.dirname (db.config.TRACKER_WEB)) + '/' + name + '/'
        config_file = os.path.join (project_directory, 'config.ini')
        config_file_tmp = config_file + '.tmp'
        os.rename (config_file, config_file_tmp)
        infile, outfile = open (config_file_tmp), open (config_file, 'w')
        for line in infile:
            if re.match ('^#?web =', line):
                line = 'web = %s\n' % (url,)
            elif re.match ('name =', line):
                line = 'name = %s\n' % (name,)
            outfile.write (line)
        infile.close (), outfile.close ()
        os.remove (config_file_tmp)
        # Initialize project
        f = open (os.path.join (os.path.join (db.config.TRACKER_HOME, 'db'), 'backend_name'))
        backend = f.read ()
        f.close ()
        try:
            tracker = roundup.instance.open (project_directory)
            if tracker.exists ():
                tracker.nuke ()
        except:
            pass
        roundup.init.write_select_db (project_directory, backend)
        tracker = roundup.instance.open (project_directory)
        tracker.init (roundup.password.Password ('dummypassword'))
    except Exception, e:
        try:
            os.rmdir (project_directory)
        except:
            pass
        raise Reject ("Project creation failed: %s" % (e,))

def create_project (db, c, nodeid, newvalues):
    _audit_project (db, c, nodeid, newvalues)
    _make_project (db, c, nodeid, newvalues)

def create_admin_user (db, c, nodeid, olddata):
    # This has to be a reactor, because login refers to the project
    db.login.create (user=c.get (nodeid, 'user'), project=nodeid, login='admin')
    db.commit ()

def remove_logins (db, c, nodeid, newvalues):
    for id in db.login.find (project=nodeid):
        db.login.retire (id)

def delete_project (db, c, nodeid, olddata):
    name = c.get (nodeid, 'project')
    project_directory = os.path.join (os.path.dirname (db.config.HOME), name)
    try:
        # Remove database
        roundup.instance.open (project_directory).nuke ()
        # Remove project directory
        for root, dirs, files in os.walk (project_directory, topdown=False):
            for name in files:
                os.remove (os.path.join (root, name))
            for name in dirs:
                os.rmdir (os.path.join (root, name))
        os.rmdir (project_directory)
    except:
        pass

def init (db):
    db.project.audit ('create', create_project)
    db.project.react ('create', create_admin_user)
    db.project.audit ('retire', remove_logins)
    db.project.react ('retire', delete_project)
