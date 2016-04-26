(
s = Server.local.boot;
)

(SynthDef (\ORGN,
	{|freq = 440,
		detune = 1.0,
		gate = 1,
		doneAction = 2,
		outbus = 0,
		pan = 0.0,         // ISSUE: Varify that pan is working
		amp = 0.01,
		lfoFreq = 5.0,     // Hz
		lfoDelay = 0.0,    // seconds
		lfoDepth = 1.0,    // normalized
		lfoPhase = 0.25,   // normalized
		vibrato = 0.0,     // normalized
		vsens = 0.0,       // normalized
		chorus = 0,        // normalized
		chorusDelay = 0,   // seconds

		// Stack "A"
		tremoloA = 0.0,    // normalized
		modDepthA = 1.0,   // normalized FM modulation depth
		mixA = 1,          // amp A (linear)
		// Stack "B"
		detuneB = 1,       // 1/2, 1, 3/2, 2
		ratioB = 2,        // 1/2, 1, 2, 3
		tremoloB = 0.0,    // normalized
		modDepthB = 1.0,   // normalized FM modulation depth
		sustainB = 1.0,    // [0...1]
		decayB = 0.1,      // seconds
		mixB = 1|          // amp B (linear)

		var lfoEnv = EnvGen.kr(Env([0.001, 0.001, 1.0, 1.0],
			[lfoDelay, lfoDelay, 0.5], \linear, 2), gate, doneAction: 0);
		var chorusEnv = EnvGen.kr(Env([0.001, 0.001, 1.0, 1.0],
			[chorusDelay, chorusDelay, 0.5], \linear, 2), gate, doneAction: 0);
		var chorusBias = chorus.linlin(0,1,0,5) * chorusEnv;
		var f0 = freq * detune;
		var fac = f0;
		var fam = (f0*2)-chorusBias;
		var fbm = f0*detuneB;
		var fbc = fbm*ratioB+chorusBias;

		var lfo1 = LFCub.kr(lfoFreq,0);
		var lfo2 = LFCub.kr(lfoFreq, lfoPhase);
		var lfo3 = lfo2*lfo2;
		var lfoamp = lfoEnv*lfoDepth+vibrato;
		var vib = lfo1*vsens*lfoamp+1;
		var trem1 = lfo2*lfoamp;
		var trem2 = lfo3*lfoamp;

		// Stack A
		var tremA = linlin(tremoloA,0,1,-1, 1);
		var modA = SinOsc.ar(fam*vib) * fac * linlin(modDepthA, 0, 1, 0, 4) *
		    (1 + LinXFade2.kr(1.0, 1+trem1, tremA));
		var carA = SinOsc.ar(fac*vib+modA);

		// Stack B
		var tremB = linlin(tremoloB, 0, 1, -1, 1);
		var modB = SinOsc.ar(fbm*vib) * fbc* linlin(modDepthB, 0, 1, 0, 4) *
		    (1 + LinXFade2.kr(1.0, 1+trem2, tremB));
		var carB = SinOsc.ar(fbc*vib+modB);
		var envB = EnvGen.kr(Env.adsr(0, decayB, sustainB, 0.0001, 1.0,
			\exp, 0.001), gate, 1,0, 1, doneAction);
		var mixed = (carA * mixA * gate) + (carB * envB * mixB);
		var outsig = Pan2.ar(mixed, pan)*amp;

		Out.ar(outbus, outsig);
}).load;
)


(
m.free;
m = Poly1.new(\ORGN);
m.netAddress.postln;
)


