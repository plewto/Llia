

(SynthDef (\Chronos, {
	|inbus1 = 8
	inbus2 = 9
	outbus1 = 0
	outbus2 = 1
	xbus = 1024
	gate = 1
	// Delay 1
	d1InMixDry1 = 1.0        // inbus1 -> delay 1
	d1InMixDry2 = 0.0        // inbus2 -> delay 1
	d1Feedback = 0.0       // delay1 -> delay 1
	d1XFeedback = 0.0      // delay2 -> delay 1
	d1DelayTime = 0.1
	d1Lowpass = 20000
	d1Highpass = 20
	d1LfoFreq = 1
	d1InternalMod = 0        // LFO1 -> delay1 time
	d1ExternalMod = 0        // xbus -> delay1 time
	d1Gatted = 0             // 0 -> disable   1 -> gatted
	d1WetAmp = 1.0           // delay1 output amp
	d1Pan = 0.75
	// Delay 2
	d2InMixDry1 = 0.0
	d2InMixDry2 = 1.0
	d2Feedback = 0.0
	d2XFeedback = 0.0
	d2DelayTime = 1
	d2Lowpass = 20000
	d2Highpass = 20
	d2LfoFreq = 1
	d2LfoPhase = 0          // LFO2 initial phase (0..1)
	d2InternalMod = 0       // LFO2 -> delay2 time
	d2ExternalMod = 0       // xbus -> LFO2 time
	d2Gatted = 0
	d2WetAmp = 1.0
	d2Pan = -0.75
	// Dry signal
	dry1Amp = 1.0
	dry1Pan = 0.0
	dry2Amp = 1.0
	dry2Pan = 0.0
	xScale = 1.0
	xBias = 0.0|
	var dry1 = In.ar(inbus1);
	var dry2 = In.ar(inbus2);
	var x = In.kr(xbus)*xScale+xBias;
	var fb = LocalIn.ar(2);
	var fb1 = fb[0];
	var fb2 = fb[1];
	var maxDelay = 2.0;
	var lfo1 = LFCub.kr(d1LfoFreq)*0.5;
	var d1In = (dry1*d1InMixDry1) + (dry2*d1InMixDry2) + (fb1*d1Feedback) + (fb2*d2XFeedback);
	var d1Time = (d1DelayTime + (lfo1*d1InternalMod) + (x*d1ExternalMod)).abs.min(maxDelay);
	var d1Out = DelayC.ar(d1In,maxDelay,d1Time);
	var lp1 = d1Lowpass.min(20000).max(20);
	var hp1 = d1Highpass.min(20000).max(20);
	var eq1 = LPF.ar(HPF.ar(d1Out,hp1),lp1);
	var gate1 = XFade2.kr(gate,1,d1Gatted.linlin(0,1,1,-1));
	var d1Outsig = Pan2.ar(gate1*d1WetAmp*eq1, d1Pan);
	var lfo2 = LFCub.kr(d2LfoFreq,d2LfoPhase)*0.5;
	var d2In =  (dry1*d2InMixDry1) + (dry2*d2InMixDry2) + (fb2*d2Feedback) + (fb1*d2XFeedback);
	var d2Time = (d2DelayTime + (lfo2*d2InternalMod) + (x*d2ExternalMod)).abs.min(maxDelay);
	var d2Out = DelayC.ar(d2In,maxDelay,d2Time);
	var lp2 = d2Lowpass.min(20000).max(20);
	var hp2 = d2Highpass.min(20000).max(20);
	var eq2 = LPF.ar(HPF.ar(d2Out,hp2),lp2);
	var gate2 = XFade2.kr(gate,1,d2Gatted.linlin(0,1,1,-1));
	var d2Outsig = Pan2.ar(gate2*d2WetAmp*eq2, d2Pan);
	var dryOut = Pan2.ar(dry1*dry1Amp,dry1Pan) + Pan2.ar(dry2*dry2Amp,dry2Pan);
	var out1 = dryOut[0] + d1Outsig[0] + d2Outsig[0];
	var out2 = dryOut[1] + d2Outsig[1] + d2Outsig[1];
	LocalOut.ar([d1Out,d2Out]);
	Out.ar(outbus1,out1);
	Out.ar(outbus2,out2);
}).load)


