(SynthDef (\LFO1, {
	|outbus = 1024
	sineout = 1024
	sawout = 1024
	pulseout = 1024
	gate = 1
	lfoFreq = 1.0
	sineAmp = 1.0
	sineRatio = 1.0
	sawAmp = 1.0
	sawRatio = 1.0
	sawWidth = 0.0
	pulseAmp = 1.0
	pulseRatio = 1.0
	pulseWidth = 0.5
	lfoDelay = 0.0
	lfoHold = 0.5
	lfoBleed = 0.0
	lfoScale = 1.0
	lfoBias = 0|
	var env1 = EnvGen.kr(Env([0,0,1,1,0],[lfoDelay,lfoDelay,lfoHold,lfoHold],
		\lin, 2) ,gate, doneAction: 0);
	var env = XFade2.kr(env1,1,lfoBleed.linlin(0,1,-1,1));
	var sine = LFCub.kr(lfoFreq*sineRatio);
	var saw = VarSaw.kr(lfoFreq*sawRatio,0,sawWidth);
	var pulse = Pulse.kr(lfoFreq*pulseRatio,pulseWidth);
	var mixed = ((sine*sineAmp)+(saw*sawAmp)+(pulse*pulseAmp))*env;
	Out.kr(sineout,sine);
	Out.kr(sawout,saw);
	Out.kr(pulseout,pulse);
	Out.kr(outbus,mixed*lfoScale+lfoBias);
}).load
)



