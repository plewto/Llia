(SynthDef (\Saw3,
    {|freq=440, 
		detune=1.0, 
		gate=1, 
		doneAction=2, 
		outbus=0, 
		amp=0.1,
		pan=0.0,
		env1Attack = 0.01,  			// env1, modulation env
		env1Decay = 1.0,
		env1Sustain = 0.7,
		env1Release = 6.0,
		env2Attack = 0.01,				// env2, main out
		env2Decay = 1.0,
		env2Sustain = 0.7,
		env2Release = 6.0,
		lfoFreq=5.0,					// LFO  Vibrato
		vibrato=0.0, 
		vSens=0.1, 
		vFreq=7.0, 
		vDepth=0.0, 
		vDelay=1.0, 
		port=0.0,
        // Osc1
		osc1Freq = 1.0,
		osc1Wave = 1.0,
		osc1WaveLFO = 0.0,
		osc1WaveEnv2 = 0.0,
		osc1Mix = 1.0,
		// Osc2
		osc2Freq=0.7500, 
		osc2Wave=0.5,
		osc2WaveLFO=0.0, 
		osc2WaveEnv1=0.0,
		osc2Mix = 1.0,
		// Osc3
		osc3Freq=0.5
		osc3Bias = 0,
		osc3Wave = 0.0,
		osc3WaveLFO=0.0,
		osc3WaveEnv1=0.0,
		osc3Mix=1.00,
		// Noise and Ring Modulator
		nseWidth=0.3, 
		nseMix=0.0,
		ringModMix = 1.0,
		// Filters
		filterFreq=1.0, 
		filterTrack=1.0, 
		filterEnv1=1.0, 
		filterLFO=0.0,
		filterRes=0.6, 
		bpLag=0.9, 
		bpShift=(-1.0), 
		filterMix=0.0|
		var env2 = EnvGen.kr(Env.adsr(env2Attack, env2Decay, env2Sustain, env2Release,
			curve: \exp, bias: 0.001), gate,1,0,1,doneAction);
		
		var env1 = EnvGen.kr(Env.adsr(env1Attack, env1Decay, env1Sustain, env1Release,
			curve: \linear, bias: 0.000),gate,1,0,1, 0);
		
		var vibEnv = EnvGen.kr(Env([0.001, 0.001, 1.0, 1.0],
	                    		[vDelay, vDelay, env2Release],
			\linear, 2),gate, doneAction: 0);
		// LFO
		var lfo1 = LFCub.kr(lfoFreq);
		var lfov = 1+LFCub.kr(vFreq, 0, (vSens*(vibrato+(vDepth*vibEnv)).clip(0,1)));
		var f = Lag2.kr(freq, port)*detune;
		// osc1
		// var f1 = f*osc1Freq;
		// var flp1 = (f1 * (osc1Wave + 
		// 	(osc1WaveLFO * lfo1) + 
		// 	(osc1WaveEnv2 * env2)).linexp(0,1,1, 24)).clip(100, 16000);
		// var osc1 = LPF.ar(Saw.ar(f1*lfov),flp1);

		// osc1
		var f1 = f*osc1Freq;
		var fbr1 = f1 * (osc1Wave + (osc1WaveLFO * lfo1) + (osc1WaveEnv2 * env2)).linlin(0.0, 1.0, 16, 1);
		var osc1 = BRF.ar(Saw.ar(f1*lfov), fbr1);
		
		// osc2
		var pw = (osc2Wave.linlin(0.0, 1.0, 0.0, 1.0) +
			(0.5*osc2WaveLFO*lfo1) +
			(0.5*osc2WaveEnv1*env1)).linlin(0.0, 1.0, 0.5, 0.99).clip(0.5, 0.99);
		var osc2 = Pulse.ar(f*osc2Freq*lfov, pw);

		// osc3
		var f3 = f*osc3Freq+osc3Bias*lfov;
		var w3 = (osc3Wave + (osc3WaveLFO * lfo1) + (osc3WaveEnv1 * env1)).linlin(0,1,1,16);
		var syncFreq3 = (f3*w3).max(f3).min(160000);
		var osc3 = SyncSaw.ar(f3,syncFreq3);

		
		// noise
		var noiseRQ = nseWidth.linlin(0.0, 1.0, 5, 50)/(f1);
		var noiseAGC = nseWidth.linexp(0.0, 1.0, 400, 40);
		var noiseCarrier = BPF.ar(WhiteNoise.ar(), f1*lfov, noiseRQ,noiseAGC);
		var noise = noiseCarrier * osc1;
		// Ring modulator
		var rmod = osc2*osc3;
		// Filters
		var filterIn = (osc1*osc1Mix) + 
		(osc2*osc2Mix) + 
		(osc3*osc3Mix) + 
		(noise*nseMix) + 
		(rmod*ringModMix);
		var ffreq = (filterFreq.linexp(0.0, 1.0, 100, 16000)
			+ (filterTrack*freq)
			+ (filterEnv1.linexp(0.0, 1.0, 1.0, 16000)*env1)
			+ (filterLFO.linexp(0.0, 1.0, 1.0, 16000)*lfo1)).clip(100, 16000);
		var lpgain = filterRes.linlin(0.0, 1.0, 0.5, 3.99);
		var lpsig = MoogFF.ar(filterIn, ffreq, lpgain);
		var bprq = filterRes.linlin(0.0, 1.0, 1, 0.1);
		//var bpfreq = (Lag2.kr(ffreq, bpLag)+bpShift.linlin(-1.0, 1.0, -3000, 3000)).clip(100, 16000);
		var bpfreq = Lag2.kr(ffreq+bpShift.linlin(-1.0, 1.0, -3000, 3000), bpLag).clip(100, 16000);
		var bpsig = BPF.ar(filterIn, Lag2.kr(bpfreq, bpLag), bprq);
		var filterOut = XFade2.ar(lpsig, bpsig, filterMix.clip(-1,1));
		var outsig = Pan2.ar(filterOut*env2*amp,pan);
		Out.ar(outbus, outsig);
}).load;
)
