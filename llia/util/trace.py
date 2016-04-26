# llia.util.trace
#

from __future__ import print_function
enable = True
depth = 0

stack = []

def clear():
    global stack, depth
    stack = []
    depth = 0

def enter(msg):
    global stack, depth
    if enable:
        pad = " "*4*depth
        print("%s[%2d] --> %s" % (pad, depth, msg))
        stack.append(msg)
        depth += 1

def exit(msg=""):
    global stack, depth
    if enable:
        msg = msg or stack.pop()
        depth -= 1
        pad = " "*4*depth
        print("%s[%2d] <-- %s" % (pad, depth, msg))

def mark(msg):
    if enable:
        d = depth-1
        pad = " "*4*d
        print("%s[%2d] --- MARK: %s" % (pad, d, msg))
