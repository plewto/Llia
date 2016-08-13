/*
 * Saw3, A 3 oscillator subtractive synth.
 *
 * Parameters:
 * freq            - Main frequency in Hertz.
 * detune          - Pitchwheel detune ratio.
 * gate            - Envelop gate signal.
 * doneAction      -
 * outbus          - Main output bus number.
 * amp             - Main linear amplitude.
 * port            - Portamento time.
 *
 *                   Envelope 1 -> modulation.
 * env1Attack      -
 * env1Decay       -
 * env1Sustain     -
 * env1Release     -
 *
 *                   Envelope 2 -> main amplitude envelope.
 * env2Attack      -
 * env2Decay       -
 * env2Sustain     -
 * env2Release     -
 *
 *                   Vibrato
 * vfreq           - Vibrato frequency in Hertz.
 * vsens           - Vibrato sensitivity.
 * vdelay          - Vibrato onset delay in seconds.
 * vdepth          - Programmed vibrato depth.
 * vibrato         - Manual vibrato depth.
 *
 *                   LFO
 * lfoFreq         - LFO frequency in Hertz.
 * lfoDelay        - LFO onset delay in seconds
 * lfoDepth        - LFO output amplitude.
 *
 *                   OSC1 (filtered sawtooth)
 * osc1Freq        - OSC1 frequency ratio.
 * osc1Wave        - OSC1 waveshape, [0.0,1.0].
 * osc1Wave_env1   - OSC1 waveshape mod by env1.
 * osc1Wave_lfo    - OSC1 waveshape mod by lfo.
 * osc1Amp         - OSC1 linear amplitude.
 * osc1Amp_env1    - OSC1 amplitude mod by env1.
 *
 *                   OSC2 (pulse)
 * osc2Freq        - OSC2 frequency ratio.
 * osc2Wave        - OSC2 pulse width [0.0, 1.0].
 * osc2Wave_env1   - OSC2 PWM from env1.
 * osc2Wave_lfo    - OSC2 PWM from lfo.
 * osc2Amp         - OSC2 linear amplitude.
 * osc2Amp_env1    - OSC2 amplitude mod by env1.
 *
 *                   OSC3 (Sync Saw)
 * osc3Freq        - OSC3 frequency ratio.
 * osc3Bias        - OSC3 frequency bias in Hertz.
 * osc3Wave        - OSC3 sync frequency [0.0, 1.0].
 * osc3Wave_env1   - OSC3 sync freq mod by env1.
 * osc3Wave_lfo    - OSC3 sync freq mod by lfo.
 * osc3WaveLag     - OSC3 sync freq mod lag time >= 0.
 * osc3Amp         - OSC3 linear amplitude.
 * osc3Amp_env1    - OSC3 amplitude mod by env1.
 *
 *                   Noise (filtered and ring modulated with OSC3)
 * noiseFreq       - Noise filter frequency ratio.
 * noiseBW         - Noise filter width [0.0, 1.0].
 * noiseAmp        - Noise linear amplitude.
 * noiseAmp_env1   - Noise amplitude mod by env1.
 *
 *                   Filters, dual low and band pass.
 * filterFreq      - Filter frequency in Hertz.
 * filterKeytrack  - Filter keyboard track (ratio)
 * filterFreq_env1 - Filter freq mod by env1 in Hertz.
 * filterFreq_lfo  - Filter freq mod by lfo in Hertz.
 * filterRes       - Filter resonance, [0.0, 1.0].
 * filterRes_env1  - Resonance mod by env1.
 * filterRes_lfo   - Resonance mod by lfo.
 * filterMix       - Filter mode mix [-1=lowpass, +1=bandpass].
 * filterMix_lfo   - Filter mix mod by lfo.
 * filterMix_env1  - Filter mix mod by env1.
 * bandpassOffset  - Bandpass filter frequency offset (ratio)
 * bandpassLag     - Bandpass frequency mod lag time.
 *
 *

*/


(SynthDef (\Saw3,
    {|freq = 440,
		detune = 1,
		gate = 1,
		doneAction = 2,
		outbus = 0,
		xbus = 1024, 					// external control bus
		amp = 0.07,
		port = 0.0,
		// ENV1  modulation
		env1Attack = 0.01,
		env1Decay = 1.00,
		env1Sustain = 1.00,
		env1Release = 0.01,
		// ENV2 amp env
		env2Attack = 0.01,
		env2Decay = 1.00,
		env2Sustain = 1.00,
		env2Release = 0.01,
		// vlfo -> vibrato
		vfreq = 5.0,
		vsens = 0.1,
		vdelay = 0.0,
		vdepth = 0.0,
		vibrato = 0.0,
		// LFO -> waveshape, filter
		lfoFreq = 5.0,
		lfoDelay = 0.0,
		lfoDepth = 1.0,
		// OSC1 Sawtooth with bandpass
		osc1Freq = 0.5,
		osc1Wave = 0.5,
		osc1Wave_env1 = 0.0,
		osc1Wave_lfo = 0.0,
		osc1Amp = 1.0,
		osc1Amp_env1 = 0.0,
		// OSC2 Pulse
		osc2Freq = 1.50,
		osc2Wave = 0.5,
		osc2Wave_env1 = 0.0,
		osc2Wave_lfo = 0.0,
		osc2Amp = 1.0,
		osc2Amp_env1 = 0.0,
		// OSC3 Sync saw
		osc3Freq = 1.00,
		osc3Bias = 0.00,
		osc3Wave = 0.00,
		osc3Wave_env1 = 0.0,
		osc3Wave_lfo = 0.0,
		osc3WaveLag = 0.0,
		osc3Amp = 1.0,
		osc3Amp_env1 = 0,
		// Noise (ring modulated with osc 3)
		noiseFreq = 1.0,
		noiseBW = 0.5,
		noiseAmp = 0.0,
		noiseAmp_env1 = 0.0,
		// Common filter parameters
		filterFreq = 10000,
		filterKeytrack = 0,
		filterFreq_env1 = 0,
		filterFreq_lfo = 0,
		filterRes = 0.0,
		filterRes_env1 = 0.0,
		filterRes_lfo = 0.0,
		filterMix = 0.0,					// -1.0, ..., +1.0
		filterMix_lfo = 0.0,
		filterMix_env1 = 0.0,
		bandpassOffset = 1.0,				// as scale factor 0 < v
		bandpassLag = 0.0,
		xToPitch = 0.0,					    // external signal -> pitch (0..1)
		xToFilterFreq = 0.0|                // external -> filter (0..1)
		var x,xpitch,xfilter;
		var env1, env2;
		var vibenv, vamp, vsig;
		var lfoenv, lfoamp, lfo;
		var f0, f1, f2, f3;
		var w1, w2, w3;
		var a1, a2, a3;
		var osc1, osc2, osc3;
		var fnse, nseRQ, nseAGC, nseCarrier, nse, nseAmp;
		var fltin, fltout, fltmix;
		var ffreq, res, lpgain, lpsig, bpfreq, bprq, bpsig;
		var outsig;
		x = In.kr(xbus, 1);
		env1 = EnvGen.kr(Env.adsr(env1Attack, env1Decay, env1Sustain, env1Release,
			curve: \linear, bias: 0.001), gate, 1, 0, 1, 0);
		env1 = env1 * env1;
		env2 = EnvGen.kr(Env.adsr(env2Attack, env2Decay, env2Sustain, env2Release,
			curve: \linear, bias: 0.001), gate, 1, 0, 1, doneAction);
		env2 = env2 * env2;
		vibenv = EnvGen.kr(Env([0.001, 0.001, 1.0, 1.0],[vdelay, vdelay, env2Release],
			\linear, 2), gate, doneAction: 0);

		vamp = vsens * (vibrato + (vdepth * vibenv));
		vsig = 1 + LFCub.kr(vfreq, 0, vamp);

		lfoenv = EnvGen.kr(Env([0.001, 0.001, 1.0, 1.0],[lfoDelay, lfoDelay, env2Release],
			\linear, 2), gate, doneAction: 0);

		lfoamp = lfoDepth * lfoenv;
		lfo = LFCub.kr(lfoFreq, 0, lfoamp);

		xpitch = 1 + (x*xToPitch);
		f0 = Lag2.kr(freq*detune, port) * vsig * xpitch;

		// OSC1  bandpass sawtooth.
		f1 = (f0*osc1Freq).max(0);
		w1 = osc1Wave + (lfo * osc1Wave_lfo) + (env1 * osc1Wave_env1);
		w1 = w1.linexp(0.0, 1.0, 1, 16).max(1);
		w1 = (w1*f1).clip(f1, 16*f1);
		a1 = osc1Amp + (osc1Amp_env1 * env1);
		a1 = (1.4*a1).min(1.4).max(0);
		osc1 = BRF.ar(Saw.ar(f1), w1);

		// OSC2 pulse wave
		f2 = (f0*osc2Freq).max(0);
		w2 = osc2Wave + (lfo * osc2Wave_lfo) + (env1 * osc2Wave_env1);
		w2 = w2.max(0).min(1);
		a2 = osc2Amp + (osc2Amp_env1 * env1);
		a2 = a2.min(1).max(0);
		osc2 = Pulse.ar(f2, w2);

		// OSC3 Sync saw
		f3 = (f0*osc3Freq+osc3Bias).max(0).min(12000);
		w3 = osc3Wave + ((1 + (0.5*lfo)) * 0.5 * osc3Wave_lfo) + (env1 * osc3Wave_env1);
		w3 = w3.abs.linlin(0, 1, 1, 16);
		w3 = w3*f3.max(f3+1);
		w3 = Lag2.kr(w3, osc3WaveLag).min(11999);
		a3 = osc3Amp + (osc3Amp_env1 * env1);
		a3 = (0.5*a3).min(1).max(0);
		osc3 = SyncSaw.ar(f3, w3);

		// Noise (ring modulated with OSC3)
		fnse = (f0*noiseFreq).max(1).min(12000);
		nseRQ = noiseBW.linlin(0.0, 1.0, 5, 50)/fnse;
		nseAGC = noiseBW.linexp(0.0, 1.0, 400, 40);
		nseCarrier = BPF.ar(WhiteNoise.ar(), fnse, nseRQ, nseAGC);
		nseAmp = noiseAmp + (noiseAmp_env1 * env1);
		nseAmp = (nseAmp/2).min(1).max(0);
		nse = ring1(nseCarrier,osc3);

		// Filters
		fltin = (osc1*a1) + (osc2*a2) + (osc3*a3) + (nse*nseAmp);
		xfilter = 1 + (x * xToFilterFreq);
		ffreq = filterFreq + (filterKeytrack * f0);
		ffreq = ffreq + (filterFreq_env1 * env1);
		ffreq = ffreq + (filterFreq_lfo * lfo);
		ffreq = ffreq * xfilter;
		ffreq = ffreq.clip(100, 12000);
		res = filterRes;
		res = res + (filterRes_lfo * lfo);
		res = res + (filterRes_env1 * env1);
		res = res.clip(0, 1);
		lpgain = res.linlin(0.0, 1.0, 0.5, 3.99);
		bprq = res.linlin(0.0, 1.0, 1.0, 0.1);
		bpfreq = bandpassOffset.clip(0.5, 16) * ffreq;
		bpfreq = Lag2.kr(bpfreq.clip(100, 12000), bandpassLag);
		lpsig = MoogFF.ar(fltin, ffreq, lpgain);
		bpsig = BPF.ar(fltin, bpfreq, bprq);
		fltmix = filterMix;
		fltmix = fltmix + (filterMix_lfo * lfo);
		fltmix = fltmix + (filterMix_env1 * env1);
		fltmix = fltmix.clip(-1, 1);
		fltout = XFade2.ar(lpsig, bpsig, fltmix);
		outsig = fltout*env2*amp;
		Out.ar(outbus, outsig);
	}).load;
)

