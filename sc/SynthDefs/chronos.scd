

(SynthDef (\Chronos, {
	|inbus1 = 8
	inbus2 = 9
	outbus1 = 0
	outbus2 = 1
	xbus = 1024
	lfoCommonFreq = 1
	// Delay 1
	d1Dry1In = 1    // dry 1 -> delay 1
	d1Dry2In = 0
	d1DelayTime = 0.1
	d1LfoRatio = 1
	d1LfoModDepth = 0
	d1ExternalModDepth = 0
	d1Feedback = 0
	d1Lowpass = 20000
	d1Highpass = 20
	// Delay 2
	d2Dry1In = 0   // dry 1 -> delay 2
	d2Dry2In = 1
	d2Delay1In = 0 // delay 1 -> delay 2
	d2DelayTime = 0.2
	d2LfoRatio = 1
	d2LfoModDepth = 0
	d2ExternalModDepth = 0
	d2Feedback = 0
	d2Lowpass = 20000
	d2Highpass = 20
	// Output mixer
	dry1Amp = 1
	dry2Amp = 1
	d1Amp = 1
	d2Amp = 1
	dry1Pan = 0.0
	dry2Pan = 0.0
	d1Pan = 0.0
	d2Pan = 0.0|
	var dry1 = In.ar(inbus1);
	var dry2 = In.ar(inbus2);
	var x = In.kr(xbus).linlin(-1,1,-0.005,0.005);
	var fb = LocalIn.ar(2);
	var maxdelay = 2;
	// Delay 1
	var d1Insig = (dry1*d1Dry1In) + (dry2*d1Dry2In) + (d1Feedback * fb[0]);
	var lfo1 = LFCub.kr(lfoCommonFreq*d1LfoRatio,0.0,0.01)*d1LfoModDepth;
	var d1x = x*d1ExternalModDepth;
	var d1Time = (d1DelayTime+lfo1+d1x).abs.min(maxdelay);
	var d1 = DelayC.ar(d1Insig,maxdelay,d1Time);
	var delay1 = LPF.ar(HPF.ar(d1,d1Highpass.max(40)),d1Lowpass.max(40));

	// Delay 2
	var d2Insig = (dry1*d2Dry1In)+(dry2*d2Dry2In)+(delay1*d2Delay1In)+(d2Feedback*fb[1]);
	var lfo2 = LFCub.kr(lfoCommonFreq*d2LfoRatio,0.5,0.01)*d2LfoModDepth;
	var d2x = x*d2ExternalModDepth;
	var d2Time = (d2DelayTime+lfo2+d2x).abs.min(maxdelay);
	var d2 = DelayC.ar(d2Insig,maxdelay,d2Time);
	var delay2 = LPF.ar(HPF.ar(d2,d2Highpass.max(40)),d2Lowpass.max(40));

	// Output mix
	var dry1Out = Pan2.ar(dry1*dry1Amp,dry1Pan);
	var dry2Out = Pan2.ar(dry2*dry2Amp,dry2Pan);
	var dly1Out = Pan2.ar(delay1*d1Amp, d1Pan);
	var dly2Out = Pan2.ar(delay2*d2Amp,d2Pan);
	var out0 = dry1Out[0]+dry2Out[0]+dly1Out[0]+dly2Out[0];
	var out1 = dry1Out[1]+dry2Out[1]+dly1Out[1]+dly2Out[1];
	LocalOut.ar([delay1,delay2]);
	Out.ar(outbus1, out0);
	Out.ar(outbus2, out1);

}).load);


