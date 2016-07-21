### Efx StepFilter

*** ISSUE: Fix me, this version is out of date.

StepFilter is a bandpass filter with "stair-step" control signal.

The filter frequency control signal is a combinationn of 8 pulse waves and
an independent sample and hold.

The pulse signals are harmonically related with frequency ratios:
1/2, 3/4, 1, 2, 3, 4, 5, and 6.

**Parameters**

-    inbus   - Audio input bus (1 channel)              
-    outbus  - Audio output bus (2 channels), default 0
-    volume  - Linear amplitude, default 1.0 +
-    pan     - Output pan position (-1, +1), default 0.0           
-    wet     - Wet/dry signal mix (-1=Dry, +1=Wet), default +1           
-    sub1    - Pulse 1/2 amp, default 0            
-    sub2    - Pulse 3/4 amp, default 0            
-    n1      - Pulse 1 amp, default 1          
-    n2      - Pulse 2 amp, default 0           
-    n3      - Pulse 3 amp, default 0           
-    n4      - Pulse 4 amp, default 0           
-    n5      - Pulse 5 amp, default 0           
-    n6      - Pulse 6 amp, default 0           
-    shFreq  - Sample and Hold clock rate in Hertz, default 1
-    sh      - Sample and Hold amp, default 0
-    clkFreq - Primary clock rate in Hertz, default 1
-    minFreq - Minimum filter frequencuy in Hertz, default 100
-    maxFreq - Maximum filter frequency in Hertz, default 2000
-    rq      - Filter 1/q parameter, 0.1 <= rq <= 1, default 1.0
-    lag     - Filter control sigal lag time, 0 <= lag <= 1, default 0.1

+  The volume parameter is intended for use with MIDI volume controller.