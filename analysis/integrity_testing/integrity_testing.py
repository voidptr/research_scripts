############ Test the Integrity ###########

import glob
import os

import config ## some basic shit that I don't want to do myself

## aggregate the contents of the tasks.dat file
def test( directories, files_glob, expected=None ):

    passed = True
    for d in directories:
        if not os.path.exists( d ):
            print "Directory does not exist: %s" % d
            passed = False
        else:
            for file_glob in files_glob:
                files = glob.glob( os.path.join( d, file_glob ) )
                if len(files) == 0:
                    print "Files not found: %s" % os.path.join( d, file_glob )
                    passed = False
                for f in files:
                    if not os.path.exists( f ) :
                        print "File does not exist %s/%s" % (d, f)
                        passed = False

                    if expected: ## test the expected count
                        cmd = "cat"
                        if f[-3:] == ".gz":
                            cmd = "zcat -c -f"

                        lines = os.popen("%s %s | wc -l" % (cmd, f)).read()
                        if int(lines) != expected:
                            print "%s/%s line count does not match expected: %s vs %s" % ( d, f, int(lines), expected )
                            passed = False
    return passed
