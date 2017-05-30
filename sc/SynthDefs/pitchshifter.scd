/*
** Pitchshifter with delay.
** Updated 28-May-2017.
** New version is backwards compatible with previous version.
*/


// (SynthDef(\PitchShifter, {
// 	|inbus = 8,
// 	outbus1 = 0
// 	outbus2 = 1
// 	pitchRatio = 1.0     // 0..4
// 	pitchDispersion = 0.0  // normalized 0..1 --> 0..1
// 	timeDispersion = 0.0   // normalized 0..1 --> 0..0.2
// 	delay = 0.1
// 	feedback = 0
// 	dryAmp = 1.0
// 	psAmp = 1.0
// 	delayAmp = 0.0
// 	dryPan = 0.0
// 	psPan = 0.0
// 	delayPan = 0.0|
// 	var dry = In.ar(inbus);
// 	var fb = LocalIn.ar(1)*feedback;
// 	var psIn = dry+fb;
// 	var windowSize = 0.2;
// 	var pratio = pitchRatio.min(4).max(0);
// 	var pdispersion = pitchDispersion.min(1).max(0);
// 	var tdispersion = timeDispersion.linlin(0,1,0,windowSize).min(windowSize).max(0);
// 	var psOut = PitchShift.ar(psIn,windowSize,pratio,pdispersion,tdispersion);
// 	var maxDelay = 1.0;
// 	var dtime = delay.abs.min(maxDelay);
// 	var delayOut = DelayC.ar(psOut,maxDelay,dtime);
// 	var outsig = Pan2.ar(dry*dryAmp,dryPan) + Pan2.ar(psOut*psAmp,psPan) + Pan2.ar(delayOut*delayAmp,delayPan);
// 	LocalOut.ar(delayOut);
// 	Out.ar([outbus1,outbus2],outsig);
// }).load)


(SynthDef(\PitchShifter, {
	|inbus = 8,
	outbus1 = 0
	outbus2 = 1
	pitchRatio = 1.0        // 0..4
	pitchDispersion = 0.0   // normalized 0..1 --> 0..1
	timeDispersion = 0.0    // normalized 0..1 --> 0..0.2
	delay = 0.1             // 0..1
	feedback = 0            // -1..+1
	lowpass = 16000         // feedback lowpass cutoff in Hz.
	delayInSelect = 0       // 0 -> pitch shifter, 1 -> dry signal
	feedbackDestination = 0 // 0 -> pitch shifter, 1 -> delay
	delayMod = 0            // LFO -> delay time   0..1
	lfoFreq = 1.0           // LFO frequency in Hz.
	dryAmp = 1.0            // 0..2
	psAmp = 1.0             // 0..2
	delayAmp = 0.0          // 0..2
	dryPan = 0.0            // -1..+1
	psPan = 0.0             // -1..+1
	delayPan = 0.0|         // -1..+1
	var windowSize = 0.2;
	var maxDelay = 1.0;
	var dry = In.ar(inbus);
	var fb = LPF.ar(LocalIn.ar(1)*feedback,lowpass.max(100).min(16000));
	var fbPS = fb*feedbackDestination.linlin(0,1,1,0);
	var fbDly = fb*feedbackDestination;
	var psIn = dry+fbPS;
	var pratio = pitchRatio.min(4).max(0);
	var pdispersion = pitchDispersion.min(1).max(0);
	var tdispersion = timeDispersion.linlin(0,1,0,windowSize).min(windowSize).max(0);
	var psOut = PitchShift.ar(psIn,windowSize,pratio,pdispersion,tdispersion);
	var dtime = delay.abs.min(maxDelay);
	var lfo = LFTri.kr(lfoFreq,0,dtime*delayMod*0.5);
	var dlyIn = Select.ar(delayInSelect, [psOut,dry])+fbDly;
	var delayOut = DelayC.ar(dlyIn,maxDelay,(dtime+lfo).max(0).min(maxDelay));
	var outsig = Pan2.ar(dry*dryAmp,dryPan) + Pan2.ar(psOut*psAmp,psPan) + Pan2.ar(delayOut*delayAmp,delayPan);
	LocalOut.ar(delayOut);
	Out.ar([outbus1,outbus2],outsig);
}).load)














