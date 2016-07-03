/*
 * Crossover filter effect.
*/


(SynthDef (\XOver, {
	|inbus = 128,
	outbus = 0,
	amp = 1.00,
	dryAmp = 1.00,
	wetAmp = 1.00,
	dryPan = 0.00,
	lpPan = 0.75,
	hpPan = -0.75,
	crossover = 500,
	res = 0.0,
	lfoFreq = 1.00,
	lfoHpRatio = 1.00,
	lfoPan = 0.0|
	var drysig = In.ar(inbus, 1);
	var rq = 1/(res.linlin(0, 1, 1, 50));
	var lplfo = LFCub.kr(lfoFreq);
	var hplfo = LFCub.kr(lfoFreq*lfoHpRatio, pi/2);
	var lppan = lpPan + (hplfo * lfoPan);
	var hppan = hpPan + (lplfo * lfoPan);
	var lpsig = RLPF.ar(drysig, crossover, rq) * lplfo;
	var hpsig = RHPF.ar(drysig, crossover, rq) * hplfo;
	var wetsig, outsig;
	wetsig = Pan2.ar(lpsig, lppan);
	wetsig = wetsig + Pan2.ar(hpsig, hppan);
	wetsig = wetsig * wetAmp;
	drysig = Pan2.ar(drysig, dryPan)*dryAmp;
	outsig = (wetsig+drysig)*amp;
	Out.ar(0, outsig);
}).load)



