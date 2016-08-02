
(SynthDef (\MASA, {|freq = 440,
	detune = 1.0,
	gate = 1.0,
	doneAction = 2,
	outbus = 0,
	amp = 0.1,
	xbus = 1024,    // external control bus "x"
	xBias = 1.0,    // bias added to x-bus value
	xScale = 0.5,   // x-bus scale factor
	xToFreq = 0.0,  // pitch modulation from x-bus (0,1)
	vfreq = 5.0,    // vibrato frequency
	vdelay = 0.0,   // vibrato onset delay >= 0
	vsens = 0.01,   // vibrato sensitivity (0,1)
	vdepth = 0.0,   // programed vibrato depth (0,1)
	vibrato = 0.0,  // manual vibrato depth (0,1)
	attack = 0.01,  // percussive envelope attack time
	decay = 0.20,   // percussive envelope decay time
	a1 = 1.00,      // Partial amplitudes
	a2 = 0.00,      // scaled to (0,1)
	a3 = 0.00,
	a4 = 0.00,
	a5 = 0.00,
	a6 = 0.00,
	a7 = 0.00,
	a8 = 0.00,
	a9 = 0.00,
	x1 = 0.00,      // x bus modulatin of
	x2 = 0.00,      // partial amplitude, (0,1)
	x3 = 0.00,
	x4 = 0.00,
	x5 = 0.00,
	x6 = 0.00,
	x7 = 0.00,
	x8 = 0.00,
	x9 = 0.00,
	p1 = 0.00,      // percussive envelope application
	p2 = 0.00,      // to partial amplitude.
	p3 = 0.00,      // 0 -> no percussion
	p4 = 0.00,      // 1 -> 100% percussion
	p5 = 0.00,
	p6 = 0.00,
	p7 = 0.00,
	p8 = 0.00,
	p9 = 0.00|
	var holdenv = EnvGen.kr(Env.adsr(0,0,1,decay),gate, doneAction: doneAction);
	var penv = EnvGen.kr(Env.perc(attack, decay),gate, doneAction: 0);
	var x = In.kr(xbus) + xBias * xScale;
	var vibenv = EnvGen.kr(Env([0.001, 0.001, 1.0, 1.0],[vdelay, vdelay, decay], \linear, 2), gate, doneAction: 0);
	var vibsig = LFPar.kr(vfreq)* 0.2*vsens* ((vdepth*vibenv)+vibrato);
	var xfreq = xToFreq * x;
	var f0 = (freq*detune) * (1+vibsig) * (1+xfreq);
	var rArray = [0.5, 1.5, 1.0, 2, 3, 4, 5, 6, 8]*f0;
	var aArray = [a1,a2,a3,a4,a5,a6,a7,a8,a9].lincurve(0,1,0,1,2);
	var xArray = XFade2.kr(1, x, [x1,x2,x3,x4,x5,x6,x7,x8,x9].linlin(0,1,-1,1));
	var pArray = XFade2.kr(1, penv, [p1,p2,p3,p4,p5,p6,p7,p8,p9].linlin(0,1,-1,1));
	var tones = Mix.ar(SinOsc.ar(rArray,0,aArray*xArray*pArray));
	Out.ar(outbus, tones*gate*amp);
}).load
)

