# llia.gui.llhelp
# 2016.05.22
#
# Generic terminal based help system.

from __future__ import print_function

import os
import os.path as path

from llia.constants import HELP_PATH, HELP_EXT

def help_topics():
    acc = []
    for f in sorted(os.listdir(HELP_PATH)):
        fqp = os.path.join(HELP_PATH, f)
        if path.isfile(fqp):
            acc.append(path.splitext(f)[0])
    return acc
    
def read_help_file(topic):
    fqp = os.path.join(HELP_PATH, str(topic)+"."+HELP_EXT)
    try:
        with open(fqp, 'r') as input:
            text = input.read()
            return text
    except IOError:
        print("WARNING: Can not read help file '%s'" % fqp)
        return "No help for %s" % topic
        
def print_topic(topic):
    text = read_help_file(topic)
    print(text)
