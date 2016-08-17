

(SynthDef (\XOver, {|
	inbus = 128,
	lpOutbus = 128,      // lowpass filter output bus
	hpOutbus = 128,      // highpass filter output bus
	dryOutbus = 128,     // dry signal output bus

	xbus = 1024,            // external control input bus
	xoverLfoOutbus=1023,    // crossover LFO output bus  (LFO 1)
	lpModLfoOutbus=1023,    // lowpass amp LFO output bus (LFO 2)
	hpModLfoOutbus=1023,    // highpass amp LFO output bus 90 degree phase shifted (LFO 3)

	xScale = 1.0,           // external control signal scale (0..4)
	xBias = 0.0,            // external control bias (-4..+4)

	lfoFreq = 1.0,          // Reference LFO frequency in Hertz.
	                        //   All other LFO frequencies are relative to this.

    crossover = 500,        // crossover freq in Hertz.
    minCrossover = 200,     // min/max crossover frequency  
    maxCrossover = 16000,
	xoverLfoRatio = 1.0,    // crossover LFO frequency relative to lfoFreq  (LFO 1)
	xoverLfoDepth = 0.0,    // LFO -> crossover freq (0..1)
	xoverX = 0.0,           // external -> crossover freq (0..1)

	res = 0.5,              // resonace (0..1)

	lpMode = 1.0,           // 0 -> bandpass, 1 -> lowpass
	lpMix = 1.0,            // lowpass filter static gain (0..2)
	lpMixLfo = 0.0,         // LFO -> lowpass mix (0..1)
	lpMixX = 0.0,           // external -> lowpass mix (0..1)
	lpLfoRatio = 1.0,       // lowpass LFO freq ratio

	hpMode = 1.0,           // 0 -> band-reject, 1 -> highpass
	hpMix = 1.0,            //   highpass LFO is 90 degrees
	hpMixLfo = 0.0,         //   relative to lowpass
	hpMixX = 0.0,
	hpLfoRatio = 1.0,

	dryMix = 0.0,           // dry signal gain (0..2)
	amp = 1.0|              // Overall gain (applies to lowpass, highpass and dry), (0..2)

	var dry = In.ar(inbus);
	var x = In.kr(xbus) * xScale + xBias;
	var posX = (x * 0.5 + 0.5).max(0).min(1);   // positive only version of external signal
	                                             // assumens -1 <= x <= +1.
	var lfo1Freq = lfoFreq * xoverLfoRatio;
	var lfo1Raw = LFCub.kr(lfo1Freq);
	var lfo1 = 1 + (lfo1Raw * xoverLfoDepth);
	var xxover = 1 + (x * xoverX);
	var crossoverFrequency = Lag2.kr((crossover * lfo1 * xxover), 0.01).max(minCrossover).min(maxCrossover);
	var rq = res.linexp(0,1, 1, 0.01);
	var lfo2Raw = LFCub.kr(lfoFreq*lpLfoRatio);
	var lfo2 = 1 + ((lfo2Raw * 0.5 + 0.5) * lpMixLfo);
	var xlp = 1 + (posX * lpMixX);
	var lpAmp = lpMix * lfo2 * xlp;
	var lp = RLPF.ar(dry, crossoverFrequency, rq);
    var bp = Resonz.ar(dry, crossoverFrequency, rq)*2;
	var filter1 = XFade2.ar(bp, lp, lpMode.linlin(0, 1, -1, 1)) * lpAmp;
	var lfo3Raw = LFCub.kr(lfoFreq*hpLfoRatio,pi/2);
	var lfo3 = 1 + ((lfo3Raw * 0.5 + 0.5) * hpMixLfo);
	var xhp = 1 + (posX * hpMixX);
	var hpAmp = hpMix * lfo3 * xhp;
	var hp = RHPF.ar(dry, crossoverFrequency, rq);
	var filter2 = XFade2.ar(bp, hp, hpMode.linlin(0, 1, -1, 1)) * hpAmp;
	Out.ar(dryOutbus, dry*amp);
	Out.ar(lpOutbus, filter1*amp);
	Out.ar(hpOutbus, filter2*amp);
	Out.kr(xoverLfoOutbus, lfo1Raw);
	Out.kr(lpModLfoOutbus, lfo2Raw);
	Out.kr(hpModLfoOutbus, lfo3Raw);
}).load)