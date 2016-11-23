/*
 *
*/


(SynthDef (\FM2,
	{|gate = 1
		amp = 0.2
		doneAction = 2
		xbus = 1023
		outbus = 0
		freq = 440
		keynumber = 60
		velocity = 1.0
		detune = 1.0
		port = 0.0
		xPitch = 0.0
		xModDepth = 0.0
		xScale = 1.0
		xBias = 0.0
		lfoFreq = 5.0
		lfoDelay = 0.0
		vsens = 0.1        // vibrato sensitivity
		vdepth = 0.0       // programed vibrato depth
		vibrato = 0.0      // manual vibrato depth
		// Carrier (op1)
		op1Enable = 1      // 0 -> mute  1 -> enable
		op1Ratio = 1.0
		op1Bias = 0.0
		op1Amp = 1.0       // linear amplitude
		op1Attack = 0.0
		op1Decay1 = 0.0
		op1Decay2 = 0.0
		op1Release = 0.0
		op1Breakpoint = 1.0
		op1Sustain = 1.0
		op1GateHold = 0    // 0 -> no   1 -> yes
		op1Keybreak = 60   // MIDI key number
		op1LeftScale = 0   // db/octave left of keybreak
		op1RightScale = 0  // db/octave right of keybreak
		op1Lfo = 0.0
		op1Velocity = 0.0
		// EFX  Flanger and pitch-shifter
		efxMix = 0.0             // -1-> flanger   +1 -> pitch-shifter
		efxAmp = 0.0
		efxAttack = 0.0
		efxDecay1 = 0.0
		efxDecay2 = 0.0
		efxRelease = 0.0
		efxBreakpoint = 1.0
		efxSustain = 1.0
		efxGateHold = 0
		efxLfoRatio = 1.0        // relative to primary LFO frequency
		flangerDelay = 0.02      // (0.00 .. 0.05)
		flangerLfoDepth = 0.0    // efxLFO -> flanger delay-time
		flangerFeedback = 0.0    // (-1..+1)
		// Pitchshifter
		psRatio = 2.0            // (0..4)
		psPDispersion = 0.0      // (0..1)
		psTDispersion = 0.0      // (0..1)
		psLfoDepth = 0.0         // efxLfo -> pitch-shift amp
		// Modulator (op2)
		op2Enable = 1
		op2Ratio = 1.0
		op2Bias = 0.0
		op2Amp = 1.0       // linear modulation depth, range(0..10)
		op2AmpRange = 1    // powers of 10 (10,100,1000,10000)
		op2Attack = 0.0
		op2Decay1 = 0.0
		op2Decay2 = 0.0
		op2Release = 0.0
		op2Breakpoint = 1.0
		op2Sustain = 1.0
		op2GateHold = 0
		op2Keybreak = 60
		op2LeftScale = 0
		op2RightScale = 0
		op2Lfo = 0.0
		op2Velocity = 0.0,
		op2Feedback=0|
		// External control signal
		var x = In.kr(xbus) * xScale + xBias;
		var xPitch_signal = x * xPitch;
		var xmod_signal = x * xModDepth;
		var hold_time = op1Release;
		var lfo_env = EnvGen.kr(Env([0,0,1,0],[lfoDelay,lfoDelay,hold_time],\lin,2),gate);
		var lfo_raw = LFCub.kr(lfoFreq);
		var vibrato_signal = (vibrato + (vdepth*lfo_env)).max(0).min(1)*vsens*lfo_raw;
		var lfo = lfo_raw * lfo_env;
		var xlfo = LFCub.kr(lfoFreq*efxLfoRatio);
		// Carrier envelope (exponential contour)
		var env_floor = 0.05;
		var op1_gate = Select.kr(op1GateHold, [gate, Trig1.kr(gate, (op1Attack + op1Decay1 + op1Decay2))]);
		var env1 = EnvGen.kr(Env([env_floor,1,op1Breakpoint.max(env_floor),op1Sustain.max(env_floor), env_floor],
			[op1Attack,op1Decay1,op1Decay2,op1Release],-4,3),
			op1_gate,doneAction: doneAction)-env_floor;
		// Modulator envelope (linear)
		var op2_gate = Select.kr(op2GateHold, [gate, Trig1.kr(gate, (op2Attack + op2Decay1 + op2Decay2))]);
		var env2 = EnvGen.kr(Env([0,1,op2Breakpoint,op1Sustain, 0],
			[op2Attack, op2Decay1, op2Decay2, op2Release],\lin,3),
			op2_gate, 1,0,1,0);
		// Efx envelope (linear)
		var efx_gate = Select.kr(efxGateHold, [gate, Trig1.kr(gate, (efxAttack + efxDecay1 + efxDecay2))]);
		var env3 = EnvGen.kr(Env([0,1,efxBreakpoint,efxSustain,0],
			[efxAttack,efxDecay1,efxDecay2,efxRelease],\lin,3),
			efx_gate,1,0,1,0);
		// Operator frequencies
		var f = Lag2.kr(freq, port)*detune*(1+vibrato_signal)*(1 + xPitch_signal);
		var f2 = f * op2Ratio + op2Bias;
		var f1 = f * op1Ratio + op1Bias;
		// Keyscales
		var op1_left_octave = ((op1Keybreak - keynumber)/12).max(0);
		var op1_right_octave = ((keynumber - op1Keybreak)/12).max(0);
		var op1_keyscale = dbamp((op1_left_octave * op1LeftScale) + (op1_right_octave * op1RightScale));
		var op2_left_octave = ((op2Keybreak - keynumber)/12).max(0);
		var op2_right_octave = ((keynumber - op2Keybreak)/12).max(0);
		var op2_keyscale = dbamp((op2_left_octave * op2LeftScale) + (op2_right_octave * op2RightScale));
		// velocity amp scale
		var op1_velocity_scale = LinXFade2.kr(1, velocity, op1Velocity.linlin(0,1,-1,1));
		var op2_velocity_scale = LinXFade2.kr(1, velocity, op2Velocity.linlin(0,1,-1,1));
		// lfo amp scale
		var op1_lfo_scale = XFade2.kr(1, lfo, op1Lfo.linlin(0,1,-1,1));
		var op2_lfo_scale = XFade2.kr(1, lfo, op2Lfo.linlin(0,1,-1,1));
		// Operator amplitudes
		var op1_amp = op1Amp * op1_velocity_scale * op1_lfo_scale * op1_keyscale;
		var op2_amp = op2Amp * op2_velocity_scale * op2_lfo_scale * (1 + xmod_signal) * op2_keyscale;
		var op2 = SinOscFB.ar(f2, op2Feedback) * op2_amp; // * env2;
		// efx
		var maxDelay = 0.05;
		var flngrIn = op2 + (LocalIn.ar(1)*flangerFeedback);
		var flngrDelay = (flangerDelay + (xlfo*maxDelay*flangerLfoDepth*0.05)).abs.min(maxDelay);
		var flngrOut = DelayL.ar(flngrIn,maxDelay,flngrDelay);
		var psAmpMod = LinXFade2.kr(1,(xlfo+1)/2,psLfoDepth.linlin(0,1,-1,1));
		var psOut = PitchShift.ar(flngrIn,0.2,psRatio,psPDispersion,psTDispersion)*psAmpMod;
		var efx = XFade2.ar(flngrOut,psOut,efxMix)*efxAmp*env3;
		var op1 = SinOsc.ar(f1 + HPF.ar((op2*env2+efx)*f1*op2AmpRange,30)) * op1_amp * env1;
		LocalOut.ar(flngrOut);
		Out.ar(outbus, HPF.ar(op1*amp, 30));

}).load)


