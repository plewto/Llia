(SynthDef(\XOver, {
	|inbus = 16
	outbus1 = 0
	outbus2 = 0
	xbus = 1024
	lfo1aOutbus = 1023
	lfo1bOutbus = 1023
	lfo2Outbus = 1023
	xscale= 1.0
	xbias = 0.0
	lfoFreq = 1.0        // common LFO frequency
	lfoEnable = 1        // 0-> do not apply LFO to filter output
	lfo2Ratio = 1.0      // xover lfo ratio
	lfo2Wave = 0.0       // varsaw -1 = saw 0 = tri +1 = saw
	res = 0              // filter resonace
	xover = 500          // static crossover frequency
	lfoToXover = 0.0     // xLFO -> xover
	externToXover = 0.0
	minXover = 100
	maxXover = 20000

	filterBMix = 0.0     // 0 = Highpass, 1 = bandpass
	filterBRatio = 1.0   // freq ratio filterB:filterA
	filterBLag = 0.0

	dryAmp = 0.0
	filterAAmp = 1.0
	filterBAmp = 1.0
	dryPan = 0.0
	filterAPan = 0.0
	filterBPan = 0.0
	amp = 1.0|           // main output amp
	var dry = In.ar(inbus);
	var x = In.kr(xbus)*xscale+xbias;
	var lfo1a = LFCub.kr(lfoFreq);
	var lfo1b = LFCub.kr(lfoFreq,0.25);
	var lfo2Raw = (VarSaw.kr(lfoFreq*lfo2Ratio,0,lfo2Wave,1,1)*0.5);
	var lfo2 = lfo2Raw * lfoToXover;
	var lpfreq = (xover + (((x*externToXover) + lfo2) * 20000)).min(maxXover).max(minXover);
	var hpfreq = (Lag2.kr(lpfreq,filterBLag)*filterBRatio).min(20000).max(50);
	var rq = LinExp.kr(res,0,1,1,0.01);
	var lfoBleed = 1-lfoEnable;
	var filterA = RLPF.ar(dry,lpfreq,rq) * ((lfo1a*lfoEnable) + lfoBleed);
	var bpf =  Resonz.ar(dry, hpfreq, rq)*2;
	var hpf = RHPF.ar(dry,hpfreq,rq);
	var filterB = XFade2.ar(bpf,hpf,filterBMix.linlin(0,1,-1,1)) * ((lfo1b * lfoEnable) + lfoBleed);
	var out1;
	var out2;
	filterA = Pan2.ar(filterA, filterAPan)*filterAAmp;
	filterB = Pan2.ar(filterB, filterBPan)*filterBAmp;
	dry = Pan2.ar(dry,dryPan)*dryAmp;
	out1 = (filterA[0]+filterB[0]+dry[0])*amp;
	out2 = (filterA[1]+filterB[1]+dry[1])*amp;
	Out.ar(outbus1, out1);
	Out.ar(outbus2, out2);
	Out.kr(lfo1aOutbus,lfo1a);
	Out.kr(lfo1bOutbus, lfo1b);
	Out.kr(lfo2Outbus,lfo2);

}).load)












	