/*
** A Simple echo effect
*/



(SynthDef (\Echo1,
    {|inbus=100,
		outbus = 0,
		delayTime = 0.100,
		maxDelayTime = 1.000,
		feedback = 0.0,
		efxmix = 0.0|
		var drysig, fb, delayIn, wetsig, outsig;
		fb = LocalIn.ar(2);
		drysig = In.ar(inbus, 2);
		delayIn = drysig + fb;
		wetsig = DelayC.ar(delayIn, maxDelayTime, delayTime);
		LocalOut(wetsig);
		outsig = XFade2.ar(drysig, wetsig, efxmix);
		Out.ar(outbus, outsig);
	}).load;
)
