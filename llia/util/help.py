# llia.util.help
#

from __future__ import print_function

import urlparse, urllib, os, os.path, webbrowser

from llia.constants import HELP_PATH, HELP_EXT


def path_to_url(path):
    u = urlparse.urljoin('file:', urllib.pathname2url(path))
    return u

def help_file_url(topic):
    pth = os.path.join(HELP_PATH, topic) + "." + HELP_EXT
    pth = os.path.abspath(pth)
    flg = os.path.exists(pth)
    if not os.path.exists(pth) and topic[:3] != "ls_":
        return help_file_url("ls_"+topic)
    else:
        u = path_to_url(pth)
        return path_to_url(pth)

def open_help(topic):
    url = help_file_url(topic)
    webbrowser.open(url)

def help_topics(target=""):
    EXT = "."+HELP_EXT
    acc = []
    for f in os.listdir(HELP_PATH):
        fn,ext = os.path.splitext(f)
        if ext == EXT and target in fn:
            acc.append(fn)
    acc.sort()
    return acc
