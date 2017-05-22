/*
** Comb
*/

(SynthDef (\Comb, {
	|outbus = 0
	inbus = 8
	delayScale = 0.01
	delay = 0.50
	phase = -1
	wet = 1.0
	amp = 1.0|
	var dry = In.ar(inbus);
	var maxDelay = 0.1;
	var delayTime = max(min((delay*delayScale),maxDelay), 0);
	var wetAmp = phase*wet;
	var wetSig = DelayC.ar(dry,maxDelay,delayTime,wetAmp);
	var outSig = dry+wetSig;
	Out.ar(outbus,outSig*amp);
}).load)
