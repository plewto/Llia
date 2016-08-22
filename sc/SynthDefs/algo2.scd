
(SynthDef (\Algo2,
	{|gate = 1
		doneAction = 2
		xbus = 1023        // external control bus
		outbus1 = 0        // op1 output bus
		outbus4 = 0        // op4 output bus
		outbus7 = 0        // op7 output bus
		freq = 440
		keynumber = 69     // MIDI key number
		detune = 1.00
		port = 0.00
		x_pitch = 0.00     // x bus -> main freq
		x_scale = 1.0
		x_bias = 0.0
		// LFO
		lfo_freq= 1.00      // Hertz
		lfo_ratio = 2.00    // 2nd LFO freq relative to lfo_freq
		lfo_mix = 1.00,     // 2nd LFO amp (0..1)
		lfo_delay = 0.00    // LFO onset delay in seconds
		lfo_depth = 0.00    // LFO (modulation not vibrato) amplitude (0..1)
		vsens = 0.01        // vibrato sensitivity (0..1)
		vdepth = 0.00,      // programmed vibrato depth (0..1)
		vibrato = 0.00      // manual vibrato depth (0..1)
		// Envelopes
		// Env A
		enva_attack = 0.0      // Carrier envelope A
		enva_decay1 = 0.0
		enva_decay2 = 0.0
		enva_release = 0.0
		enva_breakpoint = 1.0
		enva_sustain = 1.0

		envb_attack = 0.0      // Carrier envelope B
		envb_decay1 = 0.0
		envb_decay2 = 0.0
		envb_release = 0.0
		envb_breakpoint = 1.0
		envb_sustain = 1.0

		envc_attack = 0.0      // General envelope C
		envc_decay1 = 0.0
		envc_decay2 = 0.0
		envc_release = 0.0
		envc_breakpoint = 1.0
		envc_sustain = 1.0

		envd_attack = 0.0      // general envelope D
		envd_decay1 = 0.0
		envd_decay2 = 0.0
		envd_releaseease = 0.0
		envd_breakpoint = 1.0
		envs_sustain = 1.0

		// OP1 (Carrier)
		op1_ratio = 1.0,            // op1 frequency ratio
		op1_amp = 1.00              // op1 linear amplitude
		op1_enable = 1.0            // op1 enable 0 -> off,  1 -> on
		op1_x_amp = 0.00            // op1 x -> amp  (0..1)
		op1_break_key = 60          // op1 key break point (MIDI keynumber)
		op1_left_scale = 6          // op1 left key scale, db/octave
		op1_right_scale = -3        // op1 right key scale db/octave
		op1_lfo_amp = 0.0           // op1 lfo -> amp
		op1_env_select = 0.0        // 0 -> envA ADDSR  1 -> envA ADDR
		//                          // 2 -> envB ADDSR  3 -> envB ADDR

		// OP4 (Carrier)
	    op4_ratio = 1.00
		op4_amp = 1.00
		op4_enable = 1
		op4_x_amp = 0.00
		op4_break_key = 60
		op4_left_scale = 0
		op4_right_scale = 0
		op4_lfo_amp = 0.0
		op4_env_select = 0.0

		// OP7 (Carrier)
	    op7_ratio = 1.00
		op7_amp = 1.00
		op7_enable = 1
		op7_x_amp = 0.00
		op7_break_key = 60
		op7_left_scale = 0
		op7_right_scale = 0
		op7_lfo_amp = 0.0
		op7_env_select = 0

		// OP2 (Modulator)
	    op2_ratio = 1.00
		op2_bias = 0.00
		op2_amp = 1.00
		op2_enable = 1
		op2_x_amp = 0.00
		op2_break_key = 60
		op2_left_scale = 0
		op2_right_scale = 0
		op2_lfo_amp = 0.0
		op2_env_select = 0.0        // 0 -> envC ADDSR  1 -> envC ADDR
		//                          // 2 -> envD ADDSR  3 -> envD ADDR
		//                          // 4 -> envC ADDSR  5 -> envC ADDR (inverted)
		//                          // 6 -> envC ADDSR  7 -> envC ADDR (inverted)

		// OP3 (Modulator)
	    op3_ratio = 1.00
		op3_bias = 0.00
		op3_amp = 1.00
		op3_enable = 1
		op3_x_amp = 0.00
		op3_break_key = 60
		op3_left_scale = 0
		op3_right_scale = 0
		op3_lfo_amp = 0.0
		op3_env_select = 0

		// OP5 (Modulator)
	    op5_ratio = 1.00
		op5_bias = 0.00
		op5_amp = 1.00
		op5_enable = 1.0
		op5_x_amp = 0.00
		op5_break_key = 60
		op5_left_scale = 0
		op5_right_scale = 0
		op5_lfo_amp = 0.0
		op5_env_select = 0

		// OP6 (Modulator)
	    op6_ratio = 1.00
		op6_bias = 0.00
		op6_amp = 1.00
		op6_enable = 1
		op6_x_amp = 0.00
		op6_break_key = 60
		op6_left_scale = 0
		op6_right_scale = 0
		op6_lfo_amp = 0.0
		op6_feedback = 0.0
		op6_env_feedback = 0.0
		op6_lfo_feedback = 0.0
		op6_x_feedback = 0.00
		op6_env_select = 0


		// OP8 (Modulator)
	    op8_ratio = 1.00
		op8_bias = 0.00
		op8_amp = 1.00
		op8_enable = 1
		op8_x_amp = 0.00
		op8_break_key = 60
		op8_left_scale = 0
		op8_right_scale = 0
		op8_lfo_amp = 0.0
		op8_feedback = 0.0
		op8_env_feedback = 0.0
		op8_lfo_feedback = 0.0
		op8_x_feedback = 0.00
		op8_env_select = 0

		|
		var hp_cutoff = 10;
		var hold_time = enva_release.max(envb_release).max(envc_release).max(envd_releaseease);
		var lfo_env = EnvGen.kr(Env([0,0,1,0],[lfo_delay,lfo_delay,hold_time],\lin,2),gate);
		var lfo = LFCub.kr([lfo_freq, lfo_freq*lfo_ratio],0,[1,lfo_mix]);
		var vibrato_amp = (vibrato + (lfo_env*vdepth)).min(1).max(0);
		var vlfo = 1+(vsens.linlin(0,1,0,0.1) * vibrato_amp * lfo[0]); // vibrato LFO
		var mlfo = lfo_depth * lfo_env * Mix.kr(lfo);   // modulation LFO

		// Envelopes
		var env_floor = 0.05;
		var env_a_addsr = EnvGen.kr(Env(
			[env_floor, 1.0, enva_breakpoint.max(env_floor), enva_sustain.max(env_floor), env_floor],
			[enva_attack, enva_decay1, enva_decay2, enva_release],\exp, 3),
			gate, 1, 0, 1, 0)-env_floor;
		var env_a_addr = EnvGen.kr(Env(
			[env_floor, 1.0, enva_breakpoint.max(env_floor), enva_sustain.max(env_floor), env_floor],
			[enva_attack, enva_decay1, enva_decay2, enva_release],\exp, 4),
			gate, 1, 0, 1, 0)-env_floor;
		var env_b_addsr = EnvGen.kr(Env(
			[env_floor, 1.0, envb_breakpoint.max(env_floor), envb_sustain.max(env_floor), env_floor],
			[envb_attack, envb_decay1, envb_decay2, envb_release],\exp, 3),
			gate, 1, 0, 1, 0);
		var env_b_addr = EnvGen.kr(Env(
			[env_floor, 1.0, envb_breakpoint.max(env_floor), envb_sustain.max(env_floor), env_floor],
			[envb_attack, envb_decay1, envb_decay2, envb_release],\exp, 4),
			gate, 1, 0, 1, 0);

		var env_c_addsr = EnvGen.kr(Env(
			[0.0, 1.0, envc_breakpoint, envc_sustain, 0.0],
			[envc_attack, envc_decay1, envc_decay2, envc_release],\lin, 3),
			gate, 1, 0, 1, 0);
		var env_c_addr = EnvGen.kr(Env(
			[0.0, 1.0, envc_breakpoint, envc_sustain, 0.0],
			[envc_attack, envc_decay1, envc_decay2, envc_release],\lin, 4),
			gate, 1, 0, 1, 0);

		var env_d_addsr = EnvGen.kr(Env(
			[0.0, 1.0, envd_breakpoint, envs_sustain, 0.0],
			[envd_attack, envd_decay1, envd_decay2, envd_releaseease],\lin, 3),
			gate, 1, 0, 1, 0);
		var env_d_addr = EnvGen.kr(Env(
			[0.0, 1.0, envd_breakpoint, envs_sustain, 0.0],
			[envd_attack, envd_decay1, envd_decay2, envd_releaseease],\lin, 4),
			gate, 1, 0, 1, 0);
		var carrier_envelopes = [env_a_addsr, env_a_addr, env_b_addsr, env_b_addr];
		var modulator_envelopes = [env_c_addsr, env_c_addr, env_d_addsr, env_d_addr,
			1-env_c_addsr, 1-env_c_addr, 1-env_d_addsr, 1-env_d_addr];
		var env1 = Select.kr(op1_env_select, carrier_envelopes);
		var env4 = Select.kr(op4_env_select, carrier_envelopes);
		var env7 = Select.kr(op7_env_select, carrier_envelopes);
		var env3 = Select.kr(op3_env_select, modulator_envelopes);
		var env2 = Select.kr(op2_env_select, modulator_envelopes);
		var env5 = Select.kr(op5_env_select, modulator_envelopes);
		var env6 = Select.kr(op6_env_select, modulator_envelopes);
		var env8 = Select.kr(op8_env_select, modulator_envelopes);



		var x = In.kr(xbus)*x_scale+x_bias;
		var x_to_pitch = 1 + (x * x_pitch);
		// Operator frequencies
		var f0 = Lag2.kr(freq*detune, port) * vlfo * x_to_pitch;
		var f1 = (f0 * op1_ratio).abs;
		var f2 = (f0 * op2_ratio + op2_bias).abs;
		var f3 = (f0 * op3_ratio + op3_bias).abs;
		var f4 = (f0 * op4_ratio).abs;
		var f5 = (f0 * op5_ratio + op5_bias).abs;
		var f6 = (f0 * op6_ratio + op6_bias).abs;
		var f7 = (f0 * op7_ratio).abs;
		var f8 = (f0 * op8_ratio + op8_bias).abs;

		// Keyscale
		var octave_right1 = ((keynumber - op1_break_key)/12).max(0);
		var octave_left1 = ((op1_break_key-keynumber)/12).max(0);
		var ascale1 = dbamp((octave_left1 * op1_left_scale) +
			(octave_right1 * op1_right_scale));
		var octave_right2 = ((keynumber - op2_break_key)/12).max(0);
		var octave_left2 = ((op2_break_key-keynumber)/12).max(0);
		var ascale2 = dbamp((octave_left2 * op2_left_scale) +
			(octave_right2 * op2_right_scale));
		var octave_right3 = ((keynumber - op3_break_key)/12).max(0);
		var octave_left3 = ((op3_break_key-keynumber)/12).max(0);
		var ascale3 = dbamp((octave_left3 * op3_left_scale) +
			(octave_right3 * op3_right_scale));
		var octave_right4 = ((keynumber - op4_break_key)/12).max(0);
		var octave_left4 = ((op4_break_key-keynumber)/12).max(0);
		var ascale4 = dbamp((octave_left4 * op4_left_scale) +
			(octave_right4 * op4_right_scale));
		var octave_right5 = ((keynumber - op5_break_key)/12).max(0);
		var octave_left5 = ((op5_break_key-keynumber)/12).max(0);
		var ascale5 = dbamp((octave_left5 * op5_left_scale) +
			(octave_right5 * op5_right_scale));
		var octave_right6 = ((keynumber - op6_break_key)/12).max(0);
		var octave_left6 = ((op6_break_key-keynumber)/12).max(0);
		var ascale6 = dbamp((octave_left6 * op6_left_scale) +
			(octave_right6 * op6_right_scale));
		var octave_right7 = ((keynumber - op7_break_key)/12).max(0);
		var octave_left7 = ((op7_break_key-keynumber)/12).max(0);
		var ascale7 = dbamp((octave_left7 * op7_left_scale) +
			(octave_right7 * op7_right_scale));
		var octave_right8 = ((keynumber - op8_break_key)/12).max(0);
		var octave_left8 = ((op8_break_key-keynumber)/12).max(0);
		var ascale8 = dbamp((octave_left8 * op8_left_scale) +
			(octave_right8 * op8_right_scale));
		// Operator amplitudes
		var a1 = (op1_amp * op1_enable) * (1 + (x * op1_x_amp)) *
		(1 + (mlfo * 0.5 * op1_lfo_amp)) * ascale1 * env1 * env1;
		var a4 = (op4_amp * op4_enable) * (1 + (x * op4_x_amp)) *
		(1 + (mlfo * 0.5 * op4_lfo_amp)) * ascale4 * env4 * env4;
		var a7 = (op7_amp * op7_enable) * (1 + (x * op7_x_amp)) *
		(1 + (mlfo * 0.5 * op7_lfo_amp)) * ascale7 * env4 * env4;
		var a3 = (op3_amp * op3_enable) * (1 + (x * op3_x_amp)) *
		(1 + (mlfo * op3_lfo_amp)) * f2 * ascale3 * env3;
		var a2 = (op2_amp * op2_enable) * (1 + (x * op2_x_amp)) *
		(1 + (mlfo * op2_lfo_amp)) * f1 * ascale2 * env2;
		var a5 = (op5_amp * op5_enable) * (1 + (x * op5_x_amp)) *
		(1 + (mlfo * op5_lfo_amp)) * f4 * ascale5 * env5;
		var a6 = (op6_amp * op6_enable) * (1 + (x * op6_x_amp)) *
		(1 + (mlfo * op6_lfo_amp)) * ascale6 * env6;  // Note not scaled by f4!
		var a8 = (op8_amp * op8_enable) * (1 + (x * op8_x_amp)) *
		(1 + (mlfo * op8_lfo_amp)) * f7 * ascale8 * env8;

		var op3 = SinOsc.ar(f3)*a3*env3;
		var op2 = HPF.ar(SinOsc.ar(f2+op3)*a2*env2, hp_cutoff);
		var op1 = SinOsc.ar(f1+op2)*a1*env1;
		var op5 = SinOsc.ar(f5)*a5*env5;
		var op6_feedback_amp = op6_feedback * 0.3 *
		(1 + (mlfo * op6_lfo_feedback)) *
		(1 + (env6 * op6_env_feedback)) *
		(1 + (x * op6_feedback));
		var op6_internal_feedback = LocalIn.ar(1) * f6 * op6_feedback_amp;
		var op6 = HPF.ar(SinOsc.ar(f6+op6_internal_feedback), hp_cutoff);
		var op4 = SinOsc.ar(f4+op5+(op6 * f4 * env6 * a6)) * a4 * env4;

		var op8_feedback_amp = op8_feedback *
		(1 + (mlfo * op8_lfo_feedback)) *
		(1 + (env8 * op8_env_feedback)) *
		(1 + (x * op8_x_feedback));
		var op8 = HPF.ar(SinOscFB.ar(f8,op8_feedback_amp)*a8*env8, hp_cutoff);
		var op7 = SinOsc.ar(f7+op8)*a7*env7;

		Out.ar(outbus1, op1);
		Out.ar(outbus4, op4);
		Out.ar(outbus7, op7);

		LocalOut.ar(op6);
		EnvGen.kr(Env.asr(0,1,hold_time),gate, doneAction: doneAction);

}).load)



