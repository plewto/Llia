/*
 * A simple 2-operator FM synth  [2]-->[1],
 * mostly used to work out details for a larger FM instrument.
 *
 * Features:
 *
 *     External control signal -> pitch, modulation depth
 *
 *     ADDSR envelopes for both operators
 *     Envelopes have a gate hold feature, when enabled envelope will cycle
 *        through all stages even if gate is lifted.
 *
 *    Simple LFO for vibrato, tremollo (carrier), modulation depth
 *
 *    Operator amplitude keyscale
 *
 *    Velocity
 *
 *    Simple FM feedback on op2
 *
 *  Accidental LFO mod effect:
 *  op?Lfo = 0.00 --> no modulation
 *         = 0.50 --> 100% modulation
 *         = 1.00 --> 100% modulation at twice the frequency
 *        values between 0.5 and 1.0 are asymmetric with increasing
 *        amounts of the 2f component.
 *
 *  op2AmpRange - (1,10,100,1000, 10000) scaling factor for op2 amp
 *                A nice chorusing effect can be produced by setting:
 *                  op1Ratio = 0
 *                  opBias -> chorus frequency
 *                  op2Ratio -> whatever
 *                  op2Amp > 1
 *                  op2AmpRange >= 100
 *                Care should be taken because if not op1 is not modulated
 *                it is directly outputting subsonic signal.
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

		// Modulator (op2)
		op2Enable = 1
		op2Ratio = 1.0
		op2Bias = 0.0
		op2Amp = 1.0       // linear modulation depth, range(0..10)?
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


		var hold_time = op1Release;     // for more complex instrument set hold_time to max carrier release time
		var lfo_env = EnvGen.kr(Env([0,0,1,0],[lfoDelay,lfoDelay,hold_time],\lin,2),gate);
		var lfo_raw = LFCub.kr(lfoFreq);
		var vibrato_signal = (vibrato + (vdepth*lfo_env)).max(0).min(1)*vsens*lfo_raw;
		var lfo = lfo_raw * lfo_env;

		// Carrier envelope has exponential contour
		var env_floor = 0.05;
		var op1_gate = Select.kr(op1GateHold, [gate, Trig1.kr(gate, (op1Attack + op1Decay1 + op1Decay2))]);

		var env1 = EnvGen.kr(Env([env_floor,1,op1Breakpoint.max(env_floor),op1Sustain.max(env_floor), env_floor],
			[op1Attack, op1Decay1, op1Decay2, op1Release], \exp, 3),
			op1_gate, 1,0,1,0)-env_floor;

		// Modulator envelope is linear
		var op2_gate = Select.kr(op2GateHold, [gate, Trig1.kr(gate, (op2Attack + op2Decay1 + op2Decay2))]);
		var env2 = EnvGen.kr(Env([0,1,op2Breakpoint,op1Sustain, 0],
			[op2Attack, op2Decay1, op2Decay2, op2Release],\lin,3),
			op2_gate, 1,0,1,0);

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
		var op2 = SinOscFB.ar(f2, op2Feedback) * op2_amp * env2;
		var op1 = SinOsc.ar(f1 + HPF.ar(op2*f1*op2AmpRange,30)) * op1_amp * env1;

		// Voice hold envelope
		Linen.kr(gate, 0.01, 1, hold_time, doneAction);

		Out.ar(outbus, HPF.ar(op1*amp, 30));

}).load)


