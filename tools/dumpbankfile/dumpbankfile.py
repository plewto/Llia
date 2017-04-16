#
# Diagnostic tool dump conents of Llia bank file.

from __future__ import print_function
import json,pprint,sys


def read_llia_bank(filename):
    jobj = ""
    with open(filename, 'r') as input:
        jobj = json.load(input)
    return jobj

def pp_llia_bank(filename):
    jobj = read_llia_bank(filename)
    pp = pprint.PrettyPrinter()
    id,tail = jobj
    data = tail['data']
    print("File id is    : '%s'" % id)
    for k in sorted(tail.keys()):
        if k != 'data' and k != 'parameters':
            print("    [%-12s] -> %s" % (k,tail[k]))
    print("    [%-12s]" % "parameters")
    for param in tail["parameters"]:
        print(" "*12, param)
    for slot in range(tail['count']):
        prog = data[slot]
        print("---------------------------------- slot[%3d]" % slot)
        if prog == "X":
            print("X")
        else:
            pid = prog[0]
            print(pid)
            print("format     ->  %s"  % prog[1])
            print("name       -> '%s'" % prog[2])
            print("remarks    -> '%s'" % prog[3])
            print("data count ->  %s"  % prog[4])
            print("data:")
            counter = 4
            print(' '*4, end='')
            for i in range(prog[4]):
                print("%s, " % prog[i+5], end='')
                counter += len(str(prog[i+5]))
                if counter > 50:
                    print()
                    print(' '*4, end='')
                    counter = 4
            print()
            performance = prog[-1]
            pp.pprint(performance)
    
    # pp.pprint(tail)

if __name__ == "__main__":
    fname = sys.argv[1]
    print("Dumping Llia bank file '%s' " % fname)
    pp_llia_bank(fname)
    
    
