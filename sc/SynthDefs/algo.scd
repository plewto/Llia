/*
** Algo, an 8-op FM synth.
**
**  [3]<-+  [4] [6]<-+  [8]<-+
**   |   |   |   |   |   +---+
**  [2]  |   +---+   |   |
**   |   |       |   |   |
**  [1]  |      [5]  |  [7]
**   +---+       +---+   |
**   |           |       |
**   A           B       C
**
*/
(SynthDef (\Algo,{
	|outbus = 0
	outbusA = 1
	outbusB = 1
	outbusC = 1
	xbus = 1023
	gate = 1
	doneAction = 2
	freq = 440
	keynumber = 60
	velocity = 1.0
	detune = 1.0
	port = 0.0
	// voice common values
	modDepth = 1.0		  // Scale factor applied to all modulators
	amp = 0.1                   // Main out amplitude
	lfov_freq = 7.0             // vibrato frequency
	lfov_delay = 0.0
	vsens = 0.1                 // vibrato snsitivity, normalized
	vdepth = 0.0                // vibrato depth
	xscale = 1.0                // external control signal scale
	xpitch = 0.0                // external -> pitch
	xmod = 0.0                  // external -> gloabl modulation depth
	// stack parameters
	// stack A - ops 1,2,3
	// stack B - ops 4,5,6
	// stack C - ops 7,8,9
	stackA_key = 60            // MIDI key number
	stackA_feedback = 0.0
	stackA_env_feedback = 0.0
	stackA_lfo_feedback = 0.0
	stackA_enable = 1
	lfoA_ratio = 1.0           // Stack A LFO freq ratio relative to lfov
	lfoA_delay = 0.0
	lfoA_wave = 0.5
	stackB_key = 60            // MIDI key number
	stackB_feedback = 0.0
	stackB_env_feedback = 0.0
	stackB_lfo_feedback = 0.0
	stackB_enable = 1
	lfoB_ratio = 1.0
	lfoB_delay = 0.0
	lfoB_wave = 0.5
	stackC_key = 60            // MIDI key number
	stackC_feedback = 0.0
	stackC_env_feedback = 0.0
	stackC_lfo_feedback = 0.0
	stackC_enable = 1
	lfoC_ratio = 1.0
	lfoC_delay = 0.0
	lfoC_wave = 0.5
	// Carrier parametes (1,5,7,9)
	op1_ratio = 1.0
	op1_bias = 0.0
	op1_attack = 0.0
	op1_decay1 = 0.0
	op1_decay2 = 0.0
	op1_release = 0.0
	op1_breakpoint = 1.0
	op1_sustain = 1.0
	op1_envmode = 0
	op1_amp = 1.0
	op1_left_scale = 0
	op1_right_scale = 0
	op1_velocity = 0
	op1_lfo  = 0.0
	op1_external = 0.0
	op5_ratio = 1.0
	op5_bias = 0.0
	op5_attack = 0.0
	op5_decay1 = 0.0
	op5_decay2 = 0.0
	op5_release = 0.0
	op5_breakpoint = 1.0
	op5_sustain = 1.0
	op5_envmode = 0
	op5_amp = 1.0
	op5_left_scale = 0
	op5_right_scale = 0
	op5_velocity = 0
	op5_lfo = 0.0
	op5_external = 0.0
	op7_ratio = 1.0
	op7_bias = 0.0
	op7_attack = 0.0
	op7_decay1 = 0.0
	op7_decay2 = 0.0
	op7_release = 0.0
	op7_breakpoint = 1.0
	op7_sustain = 1.0
	op7_envmode = 0
	op7_amp = 1.0
	op7_left_scale = 0
	op7_right_scale = 0
	op7_velocity = 0
	op7_lfo = 0.0
	op7_external = 0.0
	// Modulator parameters (2,3,4,6,8)
	op2_ratio = 1.0
	op2_bias = 0.0
	op2_attack = 0.0
	op2_decay1 = 0.0
	op2_decay2 = 0.0
	op2_release = 0.0
	op2_breakpoint = 1.0
	op2_sustain = 1.0
	op2_envmode = 0
	op2_amp = 0.0
	op2_mod_scale = 1.0
	op2_left_scale = 0
	op2_right_scale = 0
	op2_velocity = 0
	op2_lfo = 0
	op2_external = 0
	op3_ratio = 1.0
	op3_bias = 0.0
	op3_attack = 0.0
	op3_decay1 = 0.0
	op3_decay2 = 0.0
	op3_release = 0.0
	op3_breakpoint = 1.0
	op3_sustain = 1.0
	op3_envmode = 0
	op3_amp = 0.0
	op3_mod_scale = 1.0
	op3_left_scale = 0
	op3_right_scale = 0
	op3_velocity = 0
	op3_lfo = 0
	op3_external = 0
	op4_ratio = 1.0
	op4_bias = 0.0
	op4_attack = 0.0
	op4_decay1 = 0.0
	op4_decay2 = 0.0
	op4_release = 0.0
	op4_breakpoint = 1.0
	op4_sustain = 1.0
	op4_envmode = 0
	op4_amp = 0.0
	op4_mod_scale = 1.0
	op4_left_scale = 0
	op4_right_scale = 0
	op4_velocity = 0
	op4_lfo = 0
	op4_external = 0
	op6_ratio = 1.0
	op6_bias = 0.0
	op6_attack = 0.0
	op6_decay1 = 0.0
	op6_decay2 = 0.0
	op6_release = 0.0
	op6_breakpoint = 1.0
	op6_sustain = 1.0
	op6_envmode = 0
	op6_amp = 0.0
	op6_mod_scale = 1.0
	op6_left_scale = 0
	op6_right_scale = 0
	op6_velocity = 0
	op6_lfo = 0
	op6_external = 0
	op8_ratio = 1.0
	op8_bias = 0.0
	op8_attack = 0.0
	op8_decay1 = 0.0
	op8_decay2 = 0.0
	op8_release = 0.0
	op8_breakpoint = 1.0
	op8_sustain = 1.0
	op8_envmode = 0
	op8_amp = 0.0
	op8_mod_scale = 1.0
	op8_left_scale = 0
	op8_right_scale = 0
	op8_velocity = 0
	op8_lfo = 0
	op8_external = 0|
	var x = In.kr(xbus,1)*xscale;
	var hold_time = max(op1_release,max(op5_release,op7_release))*2;
	var lfov_env = EnvGen.kr(Env([0,0,1,0],[lfov_delay,lfov_delay,hold_time],\lin,2),gate);
	var lfov = LFCub.kr(lfov_freq)*lfov_env;
	var lfoA_env = EnvGen.kr(Env([0,0,1,0],[lfoA_delay,lfoA_delay,hold_time],\lin,2),gate);
	var lfoB_env = EnvGen.kr(Env([0,0,1,0],[lfoB_delay,lfoB_delay,hold_time],\lin,2),gate);
	var lfoC_env = EnvGen.kr(Env([0,0,1,0],[lfoC_delay,lfoC_delay,hold_time],\lin,2),gate);
	var lfoA = VarSaw.kr(lfov_freq*lfoA_ratio,0,lfoA_wave,lfoA_env);
	var lfoB = VarSaw.kr(lfov_freq*lfoB_ratio,0,lfoA_wave,lfoB_env);
	var lfoC = VarSaw.kr(lfov_freq*lfoC_ratio,0,lfoA_wave,lfoC_env);
	// Carrier envelopes
	var env_floor = 0.0001;
	var op1_gate = Select.kr(op1_envmode, [gate, Trig.kr(gate, (op1_attack+op1_decay1+op1_decay2))]);
	var env1 = EnvGen.kr(Env([env_floor,1,op1_breakpoint.max(env_floor),op1_sustain.max(env_floor), env_floor],
		[op1_attack, op1_decay1, op1_decay2, op1_release],\exp,3),
		op1_gate, 1,0,1,0);

	var op5_gate = Select.kr(op5_envmode, [gate, Trig.kr(gate, (op5_attack+op5_decay1+op5_decay2))]);
	var env5 = EnvGen.kr(Env([env_floor,1,op5_breakpoint.max(env_floor),op5_sustain.max(env_floor), env_floor],
		[op5_attack, op5_decay1, op5_decay2, op5_release],\exp,3),
		op5_gate, 1,0,1,0);
	var op7_gate = Select.kr(op7_envmode, [gate, Trig.kr(gate, (op7_attack+op7_decay1+op7_decay2))]);
	var env7 = EnvGen.kr(Env([env_floor,1,op7_breakpoint.max(env_floor),op7_sustain.max(env_floor), env_floor],
		[op7_attack, op7_decay1, op7_decay2, op7_release],\exp,3),
		op7_gate, 1,0,1,0);
	// modulator envelopes
	var op2_gate = Select.kr(op2_envmode, [gate, Trig.kr(gate, (op2_attack+op2_decay1+op2_decay2))]);
	var env2 = EnvGen.kr(Env([0,1,op2_breakpoint,op2_sustain,0],
		[op2_attack,op2_decay1,op2_decay2,op2_release],\lin,3),
		op2_gate,1,0,1,0);
	var op3_gate = Select.kr(op3_envmode, [gate, Trig.kr(gate, (op3_attack+op3_decay1+op3_decay2))]);
	var env3 = EnvGen.kr(Env([0,1,op3_breakpoint,op3_sustain,0],
		[op3_attack,op3_decay1,op3_decay2,op3_release],\lin,3),
		op3_gate,1,0,1,0);
	var op4_gate = Select.kr(op4_envmode, [gate, Trig.kr(gate, (op4_attack+op4_decay1+op4_decay2))]);
	var env4 = EnvGen.kr(Env([0,1,op4_breakpoint,op4_sustain,0],
		[op4_attack,op4_decay1,op4_decay2,op4_release],\lin,3),
		op4_gate,1,0,1,0);
	var op6_gate = Select.kr(op6_envmode, [gate, Trig.kr(gate, (op6_attack+op6_decay1+op6_decay2))]);
	var env6 = EnvGen.kr(Env([0,1,op6_breakpoint,op6_sustain,0],
		[op6_attack,op6_decay1,op6_decay2,op6_release],\lin,3),
		op6_gate,1,0,1,0);
	var op8_gate = Select.kr(op8_envmode, [gate, Trig.kr(gate, (op8_attack+op8_decay1+op8_decay2))]);
	var env8 = EnvGen.kr(Env([0,1,op8_breakpoint,op8_sustain,0],
		[op8_attack,op8_decay1,op8_decay2,op8_release],\lin,3),
		op8_gate,1,0,1,0);
	// Operator frequencies
	var vibsig = vsens*((vdepth*lfov) + (x * xpitch));
	var f = Lag.kr(freq,port)*detune * (1+vibsig);
	var f1 = f*op1_ratio+op1_bias;
	var f2 = f*op2_ratio+op2_bias;
	var f3 = f*op3_ratio+op3_bias;
	var f4 = f*op4_ratio+op4_bias;
	var f5 = f*op5_ratio+op5_bias;
	var f6 = f*op6_ratio+op6_bias;
	var f7 = f*op7_ratio+op7_bias;
	var f8 = f*op8_ratio+op8_bias;
	// op key scale
	var a_left_octave = ((stackA_key-keynumber)/12).max(0);
	var a_right_octave = ((keynumber-stackA_key)/12).max(0);
	var b_left_octave = ((stackB_key-keynumber)/12).max(0);
	var b_right_octave = ((keynumber-stackB_key)/12).max(0);
	var c_left_octave = ((stackC_key-keynumber)/12).max(0);
	var c_right_octave = ((keynumber-stackC_key)/12).max(0);
	var op_key_amps = dbamp([(op1_left_scale*a_left_octave)+(op1_right_scale*a_right_octave),
		(op2_left_scale*a_left_octave)+(op2_right_scale*a_right_octave),
		(op3_left_scale*a_left_octave)+(op3_right_scale*a_right_octave),
		(op4_left_scale*b_left_octave)+(op4_right_scale*b_right_octave),
		(op5_left_scale*b_left_octave)+(op5_right_scale*b_right_octave),
		(op6_left_scale*b_left_octave)+(op6_right_scale*b_right_octave),
		(op7_left_scale*c_left_octave)+(op7_right_scale*c_right_octave),
		(op8_left_scale*c_left_octave)+(op8_right_scale*c_right_octave)]);
	var op_velocity_amps = LinXFade2.kr(1,velocity,
		[op1_velocity,op2_velocity,op3_velocity,
		op4_velocity,op5_velocity,op6_velocity,
		op7_velocity,op8_velocity].linlin(0,1,-1,1));
	var op_lfo_amps = LinXFade2.kr(1,
		[lfoA,lfoA,lfoA,
		lfoB,lfoB,lfoB,
		lfoC,lfoC],
		[op1_lfo,op2_lfo,op3_lfo,
			op4_lfo,op6_lfo,op6_lfo,
			op7_lfo,op8_lfo,op8_lfo].linlin(0,1,-1,1));
	var op_xamps = LinXFade2.kr(1,x,[op1_external,op2_external,op3_external,
		op4_external,op5_external,op6_external,
		op7_external,op8_external].linlin(0,1,-1,1));
	var amps = [op1_amp,op2_amp,op3_amp,
		op4_amp,op5_amp,op6_amp,
		op7_amp,op8_amp] *
	op_key_amps *
	op_velocity_amps *
	op_lfo_amps *
	op_xamps *
	[1, modDepth*op2_mod_scale, modDepth*op3_mod_scale,
		modDepth*op4_mod_scale,1,modDepth*op6_mod_scale,
		1,modDepth*op8_mod_scale] *
	[stackA_enable, stackA_enable, stackA_enable,
		stackB_enable, stackB_enable, stackB_enable,
		stackC_enable, stackC_enable, stackC_enable] *
	[1, f1, f2, f5, 1, f5, 1, f8] *
	[env1, env2, env3, env4, env5, env6, env7, env8];
	var fb = LocalIn.ar(2);   // fb[0]   op1 --> op3
	// fb[1]   op5 --> op6
	// op8 uses internal fb
	var mhp = 30;             // modulator highpass cutoff
	var fba = HPF.ar(fb[0]*f3*
		(stackA_feedback +
			(stackA_env_feedback * env3) +
			(stackA_lfo_feedback * (lfoA*2-1))),
		mhp);
	var fbb = HPF.ar(fb[1]*f6*
		(stackB_feedback +
			(stackB_env_feedback * env6) +
			(stackB_lfo_feedback * (lfoB*2-1))),
		mhp);
	var fbc = stackC_feedback +
	(stackC_env_feedback * env8) +
	(stackC_lfo_feedback * (lfoC*2-1));
	var op3 = HPF.ar(SinOsc.ar(f3+fba),mhp)*amps[2];
	var op2 = HPF.ar(SinOsc.ar(f2+op3),mhp)*amps[1];
	var op1 = SinOsc.ar(f1+op2)*amps[0];
	var op4 = SinOsc.ar(f4)*amps[3];
	var op6 = HPF.ar(SinOsc.ar(f6+fbb),mhp)*amps[5];
	var op5 = SinOsc.ar(f5+op4+op6)*amps[4];
	var op8 = HPF.ar(SinOscFB.ar(f8,fbc),mhp)*amps[7];
	var op7 = SinOsc.ar(f7+op8)*amps[6];
	var a = HPF.ar(op1,30)*amp;
	var b = HPF.ar(op5,30)*amp;
	var c = HPF.ar(op7,30)*amp;
	var outsig = (a+b+c)/3;
	Linen.kr(gate,0.01,1, hold_time, doneAction);  // voice hold envelope
	LocalOut.ar([op1,op5]);
	Out.ar(outbus, outsig);
	Out.ar(outbusA, a);
	Out.ar(outbusB, b);
	Out.ar(outbusC, c);

	//Out.ar(0,SinOsc.ar(f)*env1*0.2);

}).load)
