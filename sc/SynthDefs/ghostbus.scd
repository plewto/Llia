/*
 * Ghostbus copies current value of a control bus to 
 * another bus with possible modifications.
 */


(SynthDef (\Ghostbus, {|
	inbus = 1024,
	outbus = 1023,
	delay = 0.25,
	feedback = 0.0,
	lag = 0.0,
	scale = 1.0,
	bias = 0.0|
	var maxDelay = 1.0;
	var x = In.kr(inbus);
	var fb = LocalIn.kr(1)*feedback;
	var delayTime = delay.abs.min(maxDelay);
	var delayOut = DelayL.kr(x+fb,maxDelay, delayTime);
	var lagOut = Lag2.kr(delayOut, lag.linlin(0.0, 1.0, 0.0, 1.0));
	var sigOut = lagOut * scale + bias;
	LocalOut.kr(delayOut);
	Out.kr(outbus, sigOut);
}).load)



