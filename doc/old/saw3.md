### Synth Saw3

A 3 Oscillator subtractive synth with dual filters.

[osc1]------------------->|       |
                          |       |----+--->[lowpass]--->|M|
[osc2]------------------->|       |    |                 |I|-->[x]--> out
                          | MIXER |    +--->[bandpass]-->|X|   
[osc3]----------------+-->|       |
                      |   |       |    
[noise]-->[filter]-->[X]->|       |

Each oscillator waveform may be modulated by either an LFO or ADSR envelope.

OSC1 - Sawtooth with integrated bandpass filter.
OSC2 - Pulse with Pulse Width Modulation.
OSC3 - Sawtooth with hard sync.

**Parameters

-    amp             - Linear amplitude, default 0.1.
-    port            - Portamento time, default 0.0.
-    env1Attack      - Env1 attack time, default 0.0.   +
-    env1Decay       - Env1 decay time, default 0.0.    +
-    env1Sustain     - Env1 sustain level, default 1.0. +
-    env1Release     - Env1 release time, default 0.0.  +
-    env2Attack      - Env2, attack time, default 0.0.  ++
-    env2Decay       - Env2 decay time, default 0.0.    ++
-    env2Sustain     - Env2 sustain level, default 1.0. ++
-    env2Release     - Env2 release time, default 0.0. ++
-    vfreq           - Vibrato frequency in Hertz, default 5.0.
-    vsens           - Vibrato sensitivity, 0 <= s <= 1, default 0.1.
-    vdelay          - Vibrato onset delay time in seconds, default 0.0. 
-    vdepth          - Programed vibrato depth.  The minimum, vibrato depth
                       after vdelay seconds.  Default 0.0.
-    vibrato         - Manual vibrato depth for use with external MIDI
                       controller.  Final vibrato depth is the sum
		       vdepth (after vdelay) and vibrato.  Default 0.
-    lfoFreq         - LFO frequency in Hertz, default 5.0.
-    lfoDelay        - LFO onset delay time in seconds, default 0.0.
-    lfoDepth        - LFO amplitude after lfoDelay seconds, default 1.0.
-    osc1Freq        - OSC1 relative frequency, default 0.5. 
-    osc1Wave        - OSC1 waveshape, 0 <= wave <= 1.  OSC1 output is a
                       bandpass filtered sawtooth, default 0.5.
-    osc1Wave_env1   - ENV1 modulation of OSC1 wave, -1 <= mod <= +1,
                       default 0.0.
-    osc1Wave_lfo    - LFO modulation of OSC1 wave, default 0.0.
-    osc1Amp         - OSC1 linear amplitude, default 1.0.
-    osc1Amp_env1    - OSC1 amplitude modulation by ENV1, default 0.0.
-    osc2Freq        - OSC2 relative frequency, default 1.0.
-    osc2Wave        - OSC2 fixed pulse width, 0 <= w <= 1, default 0.5.
-    osc2Wave_env1   - OSC2 PWM by ENV1, -1 <= mod <= +1, default 0.0.
-    osc2Wave_lfo    - OSC2 PWM by LFO, default 0.0.
-    osc2Amp         - OSC2 linear amplitude, default 1.0.
-    osc2Amp_env1    - OSC2 amplitude mod by ENV1, default 0.0.
-    osc3Freq        - OSC3 frequency ratio, default 0.5.
-    osc3Bias        - OSC3 fixed frequency offset, default 0.
-    osc3Wave        - OSC3 sync frequency, 0 <= w <= 1, default 0.5.
-    osc3Wave_env1   - OSC3 sync frequency modulation by ENV1, default 0.0.
-    osc3Wave_lfo    - OSC3 sync frequency modulation by LFO, default 0.0.
-    osc3WaveLag     - OSC3 wave modulation lag time, default 0.0.
-    osc3Amp         - OSC3 linear amplitude, default 1.0.
-    osc3Amp_env1    - OSC3 amplitude modulation by ENV1, default 0.0.
-    noiseFreq       - Relative noise frequency.   The noise signal is
                       produced by bandpass filtered noise ring modulated
		       with OSC3.  The noiseFreq parameter sets the
		       filter's center frequency, default 1.0.
-    noiseBW         - Noise filter bandwidth, 0 <= bw <= 1, default 0.5.
-    noiseAmp        - Linear noise amplitude, default 0.
-    noiseAmp_env1   - Noise amplitude modulation by ENV1, default 0.
-    filterFreq      - Common filter fixed frequency in Hertz, default 10000 +++
-    filterKeytrack  - Common filter key track, default 0.
-    filterFreq_env1 - Common filter frequency modulation by ENV1 in Hertz,
                       default 0.
-    filterFreq_lfo  - Common filter frequency modulation by LFO in Hertz,
                       default 0.
-    filterRes       - Common filter resonance, 0 <= res <= 1, default 0.
-    filterRes_env1  - Common resonance modulation by ENV1, default 0.
-    filterRes_lfo   - Common resonance modulation by LFO, default 0.
-    filterMix       - Mix between low pass and band pass filters,
                       -1 --> Low pass, +1 --> highpass, default 0
-    filterMix_env1  - Filter mix modulation by ENV1, default 0
-    filterMix_lfo   - Filter mix modulation by LFO, default 0
-    bandpassOffset  - Bandpass filter frequency scaling factor, default 1.
-    bandpassLag     - Bandpass filter modulation lag time, default 0


+ **ENV1** - General envelope for filter and waveform modulation.
++ **ENV2** - Main amplitude envelope.