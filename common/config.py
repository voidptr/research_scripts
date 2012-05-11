#########################
# path to root library
#########################

import os
import sys

class Config:
        
    local_lib_path = "../" ##### THIS IS THE MOST IMPORTANT BIT

    path_to_self =  os.path.split( os.path.abspath( __file__ ) )[0]
    lib_path = os.path.abspath( os.path.join( path_to_self, local_lib_path ) )

    class Script:
        script_name = sys.argv[0]
        path_to_self = os.path.split(os.path.abspath( script_name ))[0]
        cwd = os.getcwd()

def addpath( localpath ):
    
    path_to_add = os.path.normpath( os.path.join( Config.Script.path_to_self, localpath ) )

    if path_to_add not in sys.path:
        sys.path.append( path_to_add )

def getpath( localpath ):
    return os.path.abspath( os.path.join( Config.lib_path, localpath ) )

