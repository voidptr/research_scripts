#!/usr/bin/python

## configtest.py

import sys
import os

## this incantation is super fucking annoying
sys.path.append( os.path.normpath( os.path.join( sys.path[0], "../" ) ) )
import config as cf


#print sys.path


print "Module"
print "------"
print "local_lib_path: " + cf.Config.local_lib_path
print "path_to_self: " + cf.Config.path_to_self
print "lib_path: " + cf.Config.lib_path

print
print "Script (me)"
print "-----------"
print "script_name : " + cf.Config.Script.script_name
print "path_to_self : " + cf.Config.Script.path_to_self
print "cwd (current working directory) : " +  cf.Config.Script.cwd
