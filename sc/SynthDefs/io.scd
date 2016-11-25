
(SynthDef(\Io, {
	|outbus = 0
	xbus = 1024
	freq = 440
	keynumber = 69
	amp = 0.07
	detune = 1.0
	gate = 1
	velocity = 0.5
	doneAction = 2
	// Vibrato LFO
	vfreq = 7.0
	vlock = 0 		    // 0|1  1 -> lock vfreq to sub harmonic of f0
	vnoise = 0.3        // noise component to vibrato signal
	vdelay = 1.0
	vsens = 0.1
	vdepth = 0.0		// programed vibrato depth
	vibrato = 0.0		// manual vibrato depth
	xPitch = 0.0        // external control -> pitch
	tremRatio = 1.0     // tremolo LFO ratio to vfreq
	// Chiff & Noise
	noiseRatio = 1      // noise freq ratio
	chiffAttack = 0.03
	chiffDecay = 0.2
	chiffAmp = 0.05
	chiffVelocity = 0.5
	noiseAmp = 1.0     	   // Noise envelope piggyback on op1
	// Blip envelope
	blipAttack = 0.03
	blipDecay = 0.1
	blipDepth = 0.0
	blipVelocity = 0.0
	// OP4 (Modulator)
	op4Ratio = 1.0
	op4Feedback = 0.0
	op4LFO = 0.0
	// OP1 (Carrier)
	op1Formant = 300		// Carrier freq either formant or ratio
	op1Ratio = 1.0		    //
	op1Mode = 0		        // 0|1  0 -> ratio 1 -> formant
	op1Velocity = 0.0		//
	op1Tremolo = 0.0		// LFO -> amp
	op1ModDepth = 1.0		// OP4 -> OP1 modulation depth
	op1Attack = 0.05		//
	op1Decay = 0.30		    //
	op1Sustain = 0.5		//
	op1Release = 0.1		//
	op1ModLag = 0.0		    // env mod depth lag time
	op1BreakKey = 60        // MIDI key number
	op1LeftKeyScale = 0		// left key scale in db/octave
	op1RightKeyScale = 0	//
	op1Amp = 1.0		    // linear amp
	op1X = 0.0              // external -> mod depth
	// OP2 (Carrier)
	op2Formant = 300
	op2Ratio = 1.0
	op2Mode = 0
	op2Velocity = 0.0
	op2Tremolo = 0.0
	op2ModDepth = 1.0
	op2Attack = 0.05
	op2Decay = 0.30
	op2Sustain = 0.5
	op2Release = 0.1
	op2ModLag = 0.0
	op2BreakKey = 60
	op2LeftKeyScale = 0
	op2RightKeyScale = 0
	op2Amp = 1.0
	op2X = 0.0
	// OP3 (Carrier)
	op3Formant = 300
	op3Ratio = 1.0
	op3Mode = 0
	op3Velocity = 0.0
	op3Tremolo = 0.0
	op3ModDepth = 1.0
	op3Attack = 0.05
	op3Decay = 0.30
	op3Sustain = 0.5
	op3Release = 0.1
	op3ModLag = 0.0
	op3BreakKey = 60
	op3LeftKeyScale = 0
	op3RightKeyScale = 0
	op3Amp = 1.0
	op3X = 0.0|
	var x = In.kr(xbus,1);
	var holdTime = max(op1Release,max(op2Release,op3Release));
	/* LFOs */
	var venv = EnvGen.kr(Env([0,0,1,1],[vdelay,vdelay,holdTime],\lin,3),gate,doneAction: doneAction);
	var vf = Select.kr(vlock,[vfreq,freq/((freq/vfreq).round)]);
	var vamp = (venv*vdepth) + vibrato;
	var vlfo = ((x + xPitch) + (PinkNoise.kr(vnoise).linlin(0,1,0,4)+LFCub.kr(vf))) * vsens.linlin(0,1,0,0.1) * vamp;  // vibrato LFO
	var tlfo = (LFCub.kr(vf*tremRatio,1.667)+1*0.5)*venv;                          // tremolo & mod LFO
	/* Envelopes */
	var envs = EnvGen.kr(Env.adsr([op1Attack,op2Attack,op3Attack],
		[op1Decay,op2Decay,op3Decay],
		[op1Sustain,op2Sustain,op3Sustain],
		[op1Release,op2Release,op3Release]),gate);

	var blipEnv = EnvGen.kr(Env.adsr(blipAttack,blipDecay,0,0),gate,LinXFade2.kr(1,velocity,blipVelocity.linlin(0,1,-1,1)));
	var f0 = freq*detune*(1+vlfo)*(1+LinXFade2.kr(0,blipEnv,blipDepth.linlin(0,1,-1,1)));
	/* Chiff and Noise */
	var noiseRq = 0.1;
	var noiseRatios = [1.0,1.5,2.0,3.0,4.0,6.0];
	var rawNoise = Mix.ar(BPF.ar(WhiteNoise.ar(),noiseRatios*freq*detune*noiseRatio,noiseRq));
	var chiffAttackScale = BrownNoise.kr().abs*1.1;          // Randomize chiff envelope
	var chiffDecayScale = BrownNoise.kr().abs*1.1;
	var chiffHP = 10 + Lag2.kr((BrownNoise.kr().abs*800));  // Randomize chiff high pass
	var chiffEnv = EnvGen.kr(Env.adsr(chiffAttack*chiffAttackScale,chiffDecay*chiffDecayScale,0,0),gate);
	var chiffSig = HPF.ar(rawNoise,chiffHP)*chiffAmp*chiffEnv*LinXFade2.kr(1,velocity,chiffVelocity.linlin(0,1,-1,1))*0.30;
	var nseAmp = noiseAmp*LinXFade2.kr(1,tlfo,op1Tremolo.linlin(0,1,-1,0))*LinXFade2.kr(1,velocity,op1Velocity.linlin(0,1,-1,1))*0.3;
	var noiseSig = rawNoise*nseAmp*envs[0];
	/* modulator OP4 */
	var op4 = HPF.ar(SinOscFB.ar(f0*op4Ratio,op4Feedback),30)*LinXFade2.kr(1,tlfo,op4LFO.linlin(0,1,-1,1));
	/* carriers OP1, OP2, OP3 */
	var ff = [op1Formant/f0, op2Formant/f0, op3Formant/f0].floor*f0;
	var rf = [op1Ratio, op2Ratio, op3Ratio]*f0;
	var cfreqs = Select.kr([op1Mode,op2Mode,op3Mode],[rf,ff]);   // carrier frequencies
	var modDepths = [op1ModDepth,op2ModDepth,op3ModDepth];
	var modsigs = [op4,op4,op4]*modDepths*cfreqs*Lag2.kr(envs,[op1ModLag,op2ModLag,op3ModLag])*(1+[x*op1X,x*op2X,x*op3X]);
	/* Key scales */
	var refKeys = [op1BreakKey,op2BreakKey,op3BreakKey];
	var leftKeyOctaves = (refKeys-keynumber).max(0)/12;
	var rightKeyOctaves = (keynumber-refKeys).max(0)/12;
	var keyScales = dbamp((leftKeyOctaves*[op1LeftKeyScale,op2LeftKeyScale,op3LeftKeyScale])+
		(rightKeyOctaves*[op1RightKeyScale,op2RightKeyScale,op3RightKeyScale]));
	var velScales = LinXFade2.kr(1,velocity,[op1Velocity,op2Velocity,op3Velocity].linlin(0,1,-1,1));
	var tremScales = LinXFade2.kr(1,tlfo,[op1Tremolo,op2Tremolo,op3Tremolo].linlin(0,1,-1,1));
	var carriers = SinOsc.ar(cfreqs+modsigs)*envs*velScales*tremScales*keyScales*[op1Amp,op2Amp,op3Amp];
	var outSig = (Mix.ar(carriers)*0.333)+chiffSig+noiseSig;
	Out.ar(outbus,outSig*amp);

}).load)



