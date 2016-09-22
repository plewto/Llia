/*
 * Ghostbus copies current value of a control bus to
 * another bus with possible modifications.
 */


// (SynthDef (\Ghostbus, {|
// 	inbus = 1024,
// 	outbus = 1023,
// 	delay = 0.25,
// 	feedback = 0.0,
// 	lag = 0.0,
// 	scale = 1.0,
// 	bias = 0.0|
// 	var maxDelay = 1.0;
// 	var x = In.kr(inbus);
// 	var fb = LocalIn.kr(1)*feedback;
// 	var delayTime = delay.abs.min(maxDelay);
// 	var delayOut = DelayL.kr(x+fb,maxDelay, delayTime);
// 	var lagOut = Lag2.kr(delayOut, lag.linlin(0.0, 1.0, 0.0, 1.0));
// 	var sigOut = lagOut * scale + bias;
// 	LocalOut.kr(delayOut);
// 	Out.kr(outbus, sigOut);
// }).load)


(SynthDef (\Ghostbus, {
	|inbusA = 1024
	inbusB = 1024
	inbusC = 1024
	inbusD = 1024
	outbus = 1023
	scaleA = 1.0
	biasA = 0.0
	muteA = 0        // 0 -> enable   1 -> mute
	scaleB = 1.0
	biasB = 0.0
	muteB = 0
	scaleC = 1.0
	biasC = 0.0
	muteC = 0
	scaleD = 1.0
	biasD = 0.0
	muteD = 0
	delay = 0
	lag = 0.0
	masterScale = 1.0
	masterBias = 0.0
	masterMute = 0|
	var maxDelay = 1.0;
	var signalArray  = In.kr([inbusA,inbusB,inbusC,inbusD],1);
	var muteArray = linlin([muteA,muteB,muteC,muteD],0,1,1,0).max(0).min(1);
	var scaleArray = [scaleA,scaleB,scaleC,scaleD];
	var biasArray = [biasA,biasB,biasC,biasD];
	var sig = Mix.kr(signalArray*muteArray*scaleArray+biasArray);
	var delayOut = DelayN.kr(sig,maxDelay, delay.min(maxDelay).max(0));
	var sigout = Lag2.kr(delayOut, lag) * masterScale * masterMute.linlin(0,1,1,0) + masterBias;
	Out.kr(outbus, sigout);
}).load)



