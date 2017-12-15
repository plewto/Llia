# llia.performance_edit
# 2016.04.26
#
# Defines editor and pretty printer functions for Performances.
#

from llia.generic import is_list
from llia.performance import Performance

def smap (source, param,
          curve = None, modifier = None,
          range_ = None, limits = None):
    curve = curve or "linear"
    if modifier is None:
        if curve == "step":
            modifier = 8
        else:
            modifier = 1
    range_ = range_ or (0.0, 1.0)
    limits = limits or range_
    return (source, param, curve, modifier, range_, limits)

ccmap = smap


# NOTE: smaps and ccmaps arguments must be list (not tuple)
#
def performance(transpose = 0,
                key_range = [0, 127],
                bend = [200, "detune"],
                smaps = [],
                ccmaps = []):
    transpose = int(transpose)
    low, high = key_range
    low, high = int(min(low, high)), int(max(low, high))
    key_range = low, high
    if is_list(bend):
        bend_range , bend_param = bend
        bend_range = int(abs(bend_range))
        bend_param = str(bend_param)
    else:
        bend_range = int(abs(bend)) or 200
        bend_param = "detune"
    perf = Performance()
    perf.transpose = transpose
    perf.key_range(key_range)
    perf.bend_range = bend_range
    perf.bend_parameter = bend_param
    def get_source_mapper(source):
        try:
            sm ={"velocity" : perf.velocity_maps,
                 "aftertouch" : perf.aftertouch_maps,
                 "pitchwheel" : perf.pitchwheel_maps,
                 "keynumber" : perf.keynumber_maps}[source.lower()]
            return sm
        except KeyError:
            msg = "Invalid parameter map source: '%s'" % source
            raise KeyError(msg)
    for s in smaps:
        source, param, curve, mod, range_, limits = s
        sm = get_source_mapper(source)
        sm.add_parameter(param, curve, mod, range_, limits)
    cm = perf.controller_maps
    for cc in ccmaps:
        ctrl, param, curve, mod, range_, limits = cc
        cm.add_parameter(ctrl, param, curve, mod, range_, limits)
    return perf

def performance_pp(perf, tab=0):
    pad = " "*tab
    pad2 = pad + " "*12
    acc = "%sperformance = performance(transpose = %d,\n" % (pad, perf.transpose)
    acc += "%skey_range = %s,\n" % (pad2, perf.key_range())
    acc += "%sbend = (%s, '%s'),\n" % (pad2, perf.bend_range, perf.bend_parameter)
    acc += "%ssmaps = [" % pad2
    pad3 = ""
    for smaps in (perf.velocity_maps, perf.aftertouch_maps,
                  perf.keynumber_maps, perf.pitchwheel_maps):
        for k in smaps.keys():
            pm = smaps[k]
            src, param, curve = pm.source, pm.parameter, pm.curve_type
            mod, rng, lmt = pm.curve_modifier, pm.range_, pm.limits
            acc += "%ssmap('%s', '%s', '%s', %s, %s, %s),\n" % (pad3, src, param, curve, mod, rng, lmt)
            pad3 = pad3 or (pad + " "*38)
    if acc[-1] == '\n':
        acc = acc[:-2]
    acc += "],\n"
    acc += "%sccmaps = [" % pad2
    pad3 = ""
    for ctrl in perf.controller_maps.keys():
        smaps = perf.controller_maps[ctrl]
        for k in smaps.keys():
            pm = smaps[k]
            src, param, curve = pm.source, pm.parameter, pm.curve_type
            mod, rng, lmt = pm.curve_modifier, pm.range_, pm.limits
            acc += "%sccmap(%s, '%s', '%s', %s, %s, %s),\n" % (pad3, src, param, curve, mod, rng, lmt)
            pad3 = pad3 or (pad + " "*22)
    if acc[-1] == '\n':
        acc = acc[:-2]
    acc += "])\n"
    return acc
