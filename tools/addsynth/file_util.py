# tools/file_util

from os import listdir,makedirs
from os.path import exists,join
import shutil

def default_test(s,pat):
    """
    Default predicate for use with replace_lines
    """
    return s.lower().startswith(pat.lower())


def replace_lines(filename, target, payload=[], test=default_test):
    """
    Replace lines in file matching template.
    ARGS:
      filename - String, 
      target   - String, target in file to be replaced.
      payload  - list, matching target is replaced with elements
                 in payload.  Each payload element is placed on a 
                 new line.   If it is desired to have target remain 
                 in the file, it must be placed in the payload list.
      test     - A predicate function which test target lines
                 fn(str, pat)
                     str - line to be tested
                     pat - pattern to match.
                 The default test checks that str starts with pat
                 (case insensitive).
    """
    fobj = open(filename,'r')
    lines = fobj.readlines()
    fobj.close()
    dst = open(filename,'w')
    for line in lines:
        if test(line,target):
            for p in payload:
                dst.write("%s\n" % p)
        else:
            dst.write("%s" % line)
    dst.close()

def copy_files(src,dst):
    """
    Copy contents of source directory to destination.
    src - Source directory. 
    dst - Destination directory.
    
    Create destination directory as needed.
    """
    print "copy_files '%s' -> '%s'" % (src, dst)
    if not exists(dst):
        makedirs(dst)
    for f in listdir(src):
        shutil.copy(join(src,f),dst)
            

def new_file(filename):
    '''
    Creates a new empty file.
    '''
    fobj = open(filename,'w')
    fobj.close()
