(
SynthDef (\Flngr, {
	|inbus = 128,
	outbus = 0,
	delaybus = 1024,    // external delay time control.
	mixbus = 1024,      // external mix level.
	lfoOutbus = 1023,   // internal LFO -> control bus
	delay = 0.5,        // mean delay time, normalized
	xmodDepth = 0.0,    // external delay time scale.
	imodDepth = 0.5,    // internal LFO modulation depth, normalized.
	imodFreq = 1.0,     // internal LFO frequency, Hz
	feedback = 0.5,     // -1,+1
	feedbackLowpass = 10000, // feedback filter cutoff, Hz
	feedbackHighpass = 10,   //
	efxMix = 0.5,       // wet/dry mix  0-> dry, 1-> wet
	xmixScale = 0.0,    // external mix level scale
	amp = 1.00|         // overall linear amplitude.
	var drysig = In.ar(inbus, 1);
	var xmix = In.kr(mixbus, 1);
	var fb = HPF.ar(LPF.ar(LocalIn.ar(1), feedbackLowpass),
		feedbackHighpass)*(feedback.max(-1).min(1));
	var maxDelay = 0.01;
	var meanDelay = maxDelay/2;
	var delayScale = meanDelay/2;
	var lfo = LFTri.kr(imodFreq);
	var dt1 = delay.linlin(0, 1, -1*delayScale, delayScale);
	var dt2 = lfo.linlin(-1, 1, -1*delayScale, delayScale) * imodDepth;
	var dt3 = In.kr(delaybus, 1).linlin(-1, 1, -1*delayScale, delayScale) * xmodDepth;
	var delayTime = (meanDelay + dt1 + dt2 + dt3).max(0).min(maxDelay);
	var delayIn = drysig + fb;
	var delayOut = DelayC.ar(delayIn, maxDelay, delayTime);
	var wetsig = delayOut;
	var efxLevel = (efxMix + (xmix*xmixScale)).linlin(0, 1, -1, 1);
	var outsig = XFade2.ar(drysig, wetsig, efxLevel);
	LocalOut.ar(delayOut);
	Out.ar(outbus, outsig*amp);
	Out.kr(lfoOutbus, lfo);
}).load;
)


