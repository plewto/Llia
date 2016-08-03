/*
 * Orgn
 *
 * Bare bones FM synth
 *
 *    [m2]-->[c1]------------+
 *                           |
 *    [m4]-->[c3]------------+----> out
 *
*/


(SynthDef (\Orgn,
	{|freq = 440,
		detune = 1.0,
		gate = 1,
		doneAction = 2,
		outbus = 0,
		xbus = 1024,
		amp = 0.05,
		vfreq = 5.0,
		vdelay = 0.0,
		vdepth = 0.0,
		vibrato = 0.0,
		chorus = 0.0,
		chorusDelay = 2.0,
		r1 = 1.00,
		r2 = 1.00,
		r3 = 2.00,
		r4 = 4.00,
		amp1 = 1.00,
		amp2 = 1.00,
		amp3 = 1.00,
		amp4 = 1.00,
		enable1 = 1.0,
		enable2 = 1.0,
		enable3 = 1.0,
		enable4 = 1.0,
		cattack = 0.0,
		cdecay = 0.0,
		csustain = 1.0,
		crelease = 0.0,
		mattack = 2.0,
		mdecay = 0.0,
		msustain = 1.0,
		mrelease = 4.0,
		modulationDepth = 1.0,
		xToModulationDepth = 0.0,
		xToPitch = 0.0|
		var release = crelease.max(mrelease);
		var venv = EnvGen.kr(Env([0, 0, 1, 0], [vdelay, vdelay, release],\lin,2),gate);
		var chorusenv = EnvGen.kr(Env([0,0,1, 0],[chorusDelay,chorusDelay,release],\lin,2),gate);
		var cenv = EnvGen.kr(Env.adsr(cattack,cdecay,csustain,crelease),gate, doneAction: doneAction);
		var menv = EnvGen.kr(Env.adsr(mattack,mdecay,msustain,mrelease), gate);
		var xsig = In.kr(xbus);
		var vsens = 0.02;
		var vibamp = (vibrato + (vdepth*venv)).clip(0,1) * vsens;
		var vibsig = LFCub.kr(vfreq,0, vibamp);
		var modBias = chorus.linlin(0,1,0,6) * chorusenv;
		var f0 = (freq*detune) * (1+vibsig) * (1 + (xToPitch * xsig));
		var f1 = f0 * r1;
		var f2 = f0 * r2 + modBias;
		var f3 = f0 * r3;
		var f4 = f0 * r4 - modBias;
		var fmDepth = modulationDepth * (1 + (xToModulationDepth * xsig));
		var op2Amp = f1 * amp2.linlin(0,1,0,8) * fmDepth;
		var op4Amp = f3 * amp4.linlin(0,1,0,8) * fmDepth;
		var sine2 = SinOsc.ar(f2);
		var op2 = sine2 * op2Amp * menv;
		var op1 = SinOsc.ar(f1+op2) * amp1 * cenv;
		var sine4 = SinOsc.ar(f4);
		var op4 = sine4 * op4Amp * menv;
		var op3 = SinOsc.ar(f3+op4) * amp3 * cenv;
		var outsig = op1 + op3;
		Out.ar(outbus, outsig*amp);
}).load;)

