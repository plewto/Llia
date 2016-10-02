(SynthDef(\PitchShifter, {
	|inbus = 8,
	outbus1 = 0
	outbus2 = 1
	pitchRatio = 1.0     // 0..4
	pitchDispersion = 0.0  // normalized 0..1 --> 0..1
	timeDispersion = 0.0   // normalized 0..1 --> 0..0.2
	delay = 0.1
	feedback = 0
	dryAmp = 1.0
	psAmp = 1.0
	delayAmp = 0.0
	dryPan = 0.0
	psPan = 0.0
	delayPan = 0.0|
	var dry = In.ar(inbus);
	var fb = LocalIn.ar(1)*feedback;
	var psIn = dry+fb;
	var windowSize = 0.2;
	var pratio = pitchRatio.min(4).max(0);
	var pdispersion = pitchDispersion.min(1).max(0);

	var tdispersion = timeDispersion.linlin(0,1,0,windowSize).min(windowSize).max(0);
	var psOut = PitchShift.ar(psIn,windowSize,pratio,pdispersion,tdispersion);
	var maxDelay = 1.0;

	var dtime = delay.abs.min(maxDelay);
	var delayOut = DelayC.ar(psOut,maxDelay,dtime);
	var outsig = Pan2.ar(dry*dryAmp,dryPan) + Pan2.ar(psOut*psAmp,psPan) + Pan2.ar(delayOut*delayAmp,delayPan);
	LocalOut.ar(delayOut);
	Out.ar([outbus1,outbus2],outsig);
}).load)


