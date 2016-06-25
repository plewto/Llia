# llia.generic
# 2016.01.08
#

"""
Defines application wide generic functions.
"""
from __future__ import print_function
from zlib import crc32

from llia.thirdparty.simplegeneric import generic

@generic
def name(obj):
    str(obj)

@generic
def clone(obj):
    return obj

@generic
def dump(obj, tab=0, verbosity=0):
    pad=' '*4*tab
    print("%s%s" % (pad, obj))


# Type predicates
#

@generic
def is_string(obj):
    return False

@is_string.when_type(str)
def _is_string(obj):
    return True

@generic
def is_keytable(obj):
    return False

@generic
def is_parameter_map(obj):
    return False

@generic
def is_source_mapper(obj):
    return False

@generic
def is_cc_mapper(obj):
    return False
    
@generic
def is_control(obj):
    return False

@generic
def is_program(obj):
    return False

@generic
def is_performance(obj):
    return False

@generic
def is_bank(obj):
    return False

@generic
def is_instrument(obj):
    return False

# @generic
# def is_pigwindow(obj):
#     return False

@generic
def is_subeditor(obj):
    return False

@generic
def is_synth_control(obj):
    return False

@generic
def is_controller_name_map(obj):
    return False

# @generic
# def is_seq(obj):
#     return False

# @is_seq.when_type(list)
# def _is_seq_list(obj):
#     return True

# @is_seq.when_type(tuple)
# def _is_seq_tuple(obj):
#     return True


@generic
def is_list(obj):
    return isinstance(obj, (list, tuple))

@generic
def is_int(obj):
    return False

@is_int.when_type(int)
def _is_int(obj):
    return True

@generic
def serialize(obj):
    if obj is None:
        return ["None"]
    else:
        msg = "Generic function serialize not implemented for %s"
        msg = msg % type(obj)
        raise NotImplementedError(msg)

@generic
def hash_(obj):
    return crc32(str(obj).lower())
