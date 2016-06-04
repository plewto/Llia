### Synth Orgn

Orgn is an FM combo organ using 3 carrier/modulator pairs.

[m1]-->[c1]---------+
                    |
[m2]-->[c2]---------+----> 
                    |
[m3]-->[c3]-->[X]---+
               ^
               |
   [ADSR]------+

The c/m pairs are identical except pair 3 has an ADSR envelope while the
other two pairs have a fixed gate envelope.

**Parameters

-    amp         - Main amplitude (linear), default 0.05.
-    vfreq       - Vibrato frequency in Hertz, default 5.
-    vsens       - Vibrato sensitivity, normalized+, default 0.3.
-    vdelay      - Vibrato onset delay in seconds, default 2.0.++
-    vdepth      - Programed vibrato depth, normalized, default 0.++
-    vibrato     - Manual vibrato depth, normalized, default 0.++
-    chorus      - Chorus depth, normalized, default 0. +++
-    chorusDelay - Chorus onset delay in seconds, default 1.
-    c1          - Carrier frequency 1, default 0.5.
-    m1          - Modulator frequency 1, default 0.5.
-    mod1        - Modulation depth 1, normalized, default 1.
-    amp1        - Carrier amplitude 1 (linear), default 1.
-    c2          - Carrier frequency 2, default 0.5. 
-    m2          - Modulator frequency 2, default 0.5.
-    mod2        - Modulation depth 2, normalized, default 1.
-    amp2        - Carrier amplitude 2 (linear), default 1.
-    c3          - Carrier frequency 3, default 0.5. 
-    m3          - Modulator frequency 3, default 0.5.
-    mod3        - Modulation depth 3, normalized, default 1.
-    amp3        - Carrier amplitude 3 (linear), default 1.
-    attack3     - Carrier 3 attack tine, seconds, default 0.
-    decay3      - Carrier 3 decay time, seconds, default 0.
-    sustain3    - Carrier 3 sustain level, seconds, default 1.
-    release3    - Carrier 3 release time, seconds, default 0.
-    brightness  - Overall modulation depth, normalized, default 1.++++

+ **Normalized** values have a range between 0.0 and 1.0 inclusive.

++ There are two sources of **vibrato** depth; programed and manual.  The
   programed depth is fully applied after vdelay seconds. The manual
   vibrato is provided for external control, usually by a MIDI modulation wheel.

   The total vibrato depth at any one time is the sum of vdepth+vibrato. 

+++ The **chorus** effect is produced by adding small frequency
      offsets to FM pairs c2/m2 and c3/m3 over the duration of chorusDelay.

++++ The **brightness** parameter scales all modulation depth values.  It
     is provided as a convenience parameter for use with external control,
     such as a MIDI pedel.


      