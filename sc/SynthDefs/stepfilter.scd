/*
 * StepFilter effect.
 * 
*/

(SynthDef (\StepFilter,
	{|inbus = 128,
		outbus = 0,
		volume = 1,
		pan = 0.0,
		wet = 0.0,
		sub1 = 0.000,   // 0.50
		sub2 = 0.000,   // 0.75
		n1 = 1.000,
		n2 = 0.000,
		n3 = 0.000,
		n4 = 0.000,
		n5 = 0.000,
		n6 = 0.000,
		shFreq = 1.000,    // Sample and Hold
		sh = 1.000,
		clkFreq = 1.000,
		minFreq = 100,
		maxFreq = 2000,
		rq = 1.0,
		lag = 0.1|
		var shsig;
		var fary, pary, aary, pamp, pls, ffreq;
		var insig, outsig;
		pamp = sub1+sub2+n1+n2+n3+n4+n5+n6+sh;
		fary = [0.50, 0.75, 1,2,3,4,5,6]*clkFreq;
		pary = [0];
		aary = [sub1, sub2, n1,n2,n3,n4,n5,n6];
		shsig = (Latch.kr(BrownNoise.kr(), LFPulse.kr(shFreq))*sh).abs;
		pls = Mix.kr(LFPulse.kr(fary,pary,0.5,aary)) + shsig;
		pls = Lag2.kr(pls.linlin(0, pamp, 0 ,1), lag);
		ffreq = pls.linexp(0, 1, minFreq, maxFreq).clip(10, 12000);
		insig = In.ar(inbus, 1);
		rq = rq.clip(0.1, 1.0);
		outsig = BPF.ar(BPF.ar(insig, ffreq, rq), ffreq, rq);
		outsig = XFade2.ar(insig, outsig, wet);
		outsig = Pan2.ar(outsig*volume, pan);
		Out.ar(outbus, outsig);
}).load;
)

