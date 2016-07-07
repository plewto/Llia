(SynthDef (\XOver, {
	|inbus=128,
	outbus = 0,
	res = 0.5,
	crossover = 500,
	lfoCrossover = 0,  // 0, 1
	lfoCrossoverRatio = 1.0,
	lfoFreq = 1.0,
	lpMode = 1.0,   // 0 = Bandpass, 1=Lowpass
	lpMod = 1.0,    // 0 - None   1 - 100%
	lpAmp = 1.0,
	hpMode = 1.0,
	hpMod = 1.0,
	hpAmp = 1.0,
	spread = 0.0,
	lfoPanMod = 0.0,
	lfoPanRatio = 2.0,
	dryAmp = 1.0,
	dryPan = 0.0,
	amp = 1.0|     // overall amp
	var lfo1 = LFCub.kr(lfoFreq, 0);           // lp
	var lfo2 = LFCub.kr(lfoFreq, pi/2);        // hp
	var lfo3 = LFTri.kr(lfoFreq*lfoPanRatio);  // pan
	var lfo4amp = lfoCrossover.linlin(0, 1, 0, 2000);
	var lfo4 = LFTri.kr(lfoFreq*lfoCrossoverRatio)+1*lfo4amp;
	var lpmod = XFade2.kr(1,lfo1,lpMod.linlin(0, 1, -1, 1))*lpAmp;
	var hpmod = XFade2.kr(1,lfo2,hpMod.linlin(0, 1, -1, 1))*hpAmp;
	var lppan = spread + (lfoPanMod * lfo3);
	var hppan = (-1 * spread) + (lfoPanMod * -1 * lfo3);
	var drysig = In.ar(inbus, 1);
	var rq = res.linexp(0, 1, 1, 0.05);
	var ffreq = (crossover+lfo4).clip(100, 16000);
	var bp1 = BPF.ar(drysig, (ffreq*0.75).clip(100, 16000), rq, 2);
	var bp2 = BPF.ar(drysig, (ffreq*1.50).clip(100, 16000), rq, 2);
	var lp1 = RLPF.ar(drysig, ffreq, rq);
	var hp1 = RHPF.ar(drysig, ffreq, rq);
	var lp = XFade2.ar(bp1, lp1, lpMode.linlin(0, 1, -1, 1));
	var hp = XFade2.ar(bp2, hp1,  hpMode.linlin(0, 1, -1, 1));
	var outsig;
	drysig = Pan2.ar(drysig, dryPan)*dryAmp;
	lp = Pan2.ar(lp*lpmod, lppan)*lpAmp;
	hp = Pan2.ar(hp*hpmod, hppan)*hpAmp;
	outsig = (drysig + lp + hp) * amp;
	Out.ar(outbus, outsig);
}).load
)
