### Efx DirtyBurger

DirtyBurger is a delay line effect with a dirty feedback path.


**Parameters

-   delayTime - Delay time in seconds.  0 <= time <= 1.5, default 0.125.
-   gain      - Feedback gain, default 1.0. + 
-   threshold - Feedback clipping threshold, default 1.0. +
-   lowcut    - Feedback lowpass cutoff in Hertz, default 10000.
-   highcut   - Feedback highpass cutoff in Hertz, default 100.
-   feedback  - Feedback amount, 0 <= fb <= 1, default 0.8. +
-   flutter   - Random variation in delay time, 0 <= f <= 1, default 0.1.
-   wow       - Periodic variation of delay time, 0 <= w <= 1, default 0.1.
-   wowFreq   - Frequency of wow signal in Hertz, default 1.0.
-   wetAmp    - Linear amplitude of wet signal, default 0.5.
-   dryAmp    - Linear amplitude of dry signal, default 1.0.
-   wetPan    - Pan position of wet signal, -1 <= p <= +1, default 0.25.
-   dryPan    - Pan position of dry signal, -1 <= p <= +1, default -0.25.
-   volume    - Overall linear amplitude, default 1.0 ++

+ threshold, gain and feedback together with eq lowcut and highcut values
interact to form delay feedback signal.  The feedback signal is first
amplified by gain and then clipped to threshold.  This signal is next
equalized and then multiplied by the feedback amount.

++ The volume parameter is intended for use with MIDI volume controller.


