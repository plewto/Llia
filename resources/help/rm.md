### lliascript rm command

rm(name, param=ALL, sid=None)

Removes bus, buffer, synth of MIDI source map.


**ARGS**

-    name - String, the name of the entity to be removed.  There is no error
     if name does not exists.  name may indicate an audio bus, control bus,
     buffer, synth, or a MIDI map source.  The special public audio buses
     are "protected" and can not be removed (see abus).  If name is one of
     "velocity", "aftertouch", "pitchwheel", "keynumber", a MIDI controller
     number, or a MIDI controller name, the indicated control mapping is
     removed.

-    param - Optional String, the specific parameter to be removed.  param
     is only used if name is one of the listed controllers above.  If param
     is ALL or "ALL" the all parameter maps for name are removed, otherwise
     only the specific parameter is effected.

-    sid, optional synth_id (See synth_is help).  sid is used only if name
     is one of the listed controllers above and indicates exactly which
     synth is to be effected.  If not specified sid defaults to the current
     synth. 