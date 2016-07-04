/*
 * Crossover filter effect.
*/



(SynthDef (\XOver,
	{|inbus = 128,
		outbus = 0,
		amp = 1.00,
		dryAmp = 1.00,
		wetAmp = 1.00,
		crossover = 500,    // Hz
		res = 0.0,          // (0,1)
		lfoFreq = 1.00,     // Hz
		lfoPhase = 1.00,    // domain (0,1), range(0, pi/2)
		ringmod = 0.00,     // (0,1)
		rev = 0.00,         // (0,1)
		room = 0.5,         // reverb room size (0, 1)
		dryPan = 0.00,
		lpPan = 0.00,
		hpPan = 0.00,
		lfoPan = 0.00|      // (0,1)
		var drysig = In.ar(inbus, 1);
		var rq = (1/res.linlin(0, 1, 1, 50)).clip(1/50, 1);
		var lfo1 = LFCub.kr(lfoFreq);
		var lfo2 = LFCub.kr(lfoFreq, lfoPhase.linlin(0, 1, 0, pi/2));
		var lp = RLPF.ar(drysig, crossover, rq);
		var hp = RHPF.ar(drysig, crossover, rq);
		var rm = lp*hp;
		var wet1 = XFade2.ar(lp, rm, ringmod.linlin(0, 1, -1, 1))*lfo1;
		var wet2 = FreeVerb.ar(hp*lfo2, rev, room);
		var lppos = lpPan+(lfo2*lfoPan);
		var hppos = hpPan+(-1*lfo1*lfoPan);
		var wetsig = (Pan2.ar(wet1, lppos)+Pan2.ar(wet2, hppos))*wetAmp;
		var outsig = (wetsig + (Pan2.ar(drysig, dryPan)*dryAmp))*amp;
		Out.ar(outbus, outsig);
}).load)

