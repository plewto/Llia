/*
** Corvus hybrid synth
** 4 sets of simple FM pairs [m]->[c]
** 3 LFOS, vibrato
**         lfo1
**         lfo2
*/

(SynthDef (\Corvus,
	{|outbus = 0
		outbus1 = 128,
		outbus2 = 128,
		outbus3 = 128,
		outbus4 = 128,
		xbus = 1024
		gate = 1
		doneAction = 2
		freq = 440
		keynumber = 60
		velocity = 1.0
		detune = 1.0
		port = 0.00
		amp = 0.1
		vfreq = 7.0						// vibrato freq (master LFO freq)
		vdelay = 0.0
		vsens = 0.0
		vdepth = 0.0
		xpitch = 0.0					// external -> pitch (via vsens)
		lfo1_ratio = 1.0				// relative to vfreq
		lfo1_delay = 0.0
		lfo2_ratio = 0.5
		lfo2_delay = 0.0
		// pitch envelope
		pe_t1 = 1.0                     // pitch enve times
		pe_t2 = 1.0
		pe_t3 = 1.0
		pe_t4 = 1.0
		pe_a0 = 0.0                     // pitch envelope levels -/+1
		pe_a1 = 0.0
		pe_a2 = 0.0
		pe_a3 = 0.0
		pe_a4 = 0.0
		pe_rnode = 3                    // pitch env release node (1,2,3)
		pe_loop = 4                     // pitch env loop node (1,2,3,4)
		op1_pe = 0.0                    // pitch env -> op
		op2_pe = 0.0
		op3_pe = 0.0
		op4_pe = 0.0
		// op 1
		op1_enable = 1                  // (0|1)
		op1_ratio = 1.0                 // (0..16)
		op1_bias = 0.0                  // (0..999)
		op1_amp = 1.0                   // (0..2)
		op1_velocity = 0.0              // (0..1) velocity -> amp -> mod depth
		op1_lfo1 = 0.0                  // (0..1) lfo1 -> amp
		op1_lfo2 = 0.0                  // (0..1) lfo2 -> amp
		op1_external = 0.0              // (0..1) external -> amp
		op1_left = 0                    // (-18,-15,-12,...,0,...+12,+15,+18) left key scale
		op1_right = 0                   // right key scale
		op1_key = 60                    // (0,6,12,...,120)  key scale key
		op1_attack = 0.00               // (0..8)
		op1_decay1 = 0.00               // (0..8)
		op1_decay2 = 0.00               // (0..8)
		op1_release = 0.00              // (0..8)
		op1_breakpoint = 1.0            // (0..1)
		op1_sustain = 1.0               // (0..1)
		op1_env_mode = 0                // (0|1) 0 = gated, 1 = triggered
		fm1_ratio = 1.00                // (0..16) modulation frequency ratio
		fm1_modscale = 1                // (1,10,100,...10^^n)  n=(0,1,2,...,5)
		fm1_moddepth = 0.0              // (0..1) modulation depth
		fm1_lag = 0.00                  // (0..1) modulator envelope lag
		fm1_lfo1 = 0.00                 // (0..1) lfo1 -> modulation depth
		fm1_lfo2 = 0.00                 // (0..1) lfo2 -> modulation depth
		fm1_external = 0.00             // (0..1) external ->modulation depth
		fm1_left = 0                    // modulator left keyscale
		fm1_right = 0                   // modulator right keyscale
		// op 2
		op2_enable = 1
		op2_ratio = 1.0
		op2_bias = 0.0
		op2_amp = 1.0
		op2_velocity = 0.0
		op2_lfo1 = 0.0
		op2_lfo2 = 0.0
		op2_external = 0.0
		op2_left = 0
		op2_right = 0
		op2_key = 60
		op2_attack = 0.00
		op2_decay1 = 0.00
		op2_decay2 = 0.00
		op2_release = 0.00
		op2_breakpoint = 1.0
		op2_sustain = 1.0
		op2_env_mode = 0
		fm2_ratio = 1.00
		fm2_modscale = 1
		fm2_moddepth = 0.0
		fm2_lag = 0.00
		fm2_lfo1 = 0.00
		fm2_lfo2 = 0.00
		fm2_external = 0.00
		fm2_left = 0
		fm2_right = 0
		// op 3
		op3_enable = 1
		op3_ratio = 1.0
		op3_bias = 0.0
		op3_amp = 1.0
		op3_velocity = 0.0
		op3_lfo1 = 0.0
		op3_lfo2 = 0.0
		op3_external = 0.0
		op3_left = 0
		op3_right = 0
		op3_key = 60
		op3_attack = 0.00
		op3_decay1 = 0.00
		op3_decay2 = 0.00
		op3_release = 0.00
		op3_breakpoint = 1.0
		op3_sustain = 1.0
		op3_env_mode = 0
		fm3_ratio = 1.00
		fm3_modscale = 1
		fm3_moddepth = 0.0
		fm3_lag = 0.00
		fm3_lfo1 = 0.00
		fm3_lfo2 = 0.00
		fm3_external = 0.00
		fm3_left = 0
		fm3_right = 0
		nse3_mix = 0.0      // noise ring modulated w op3, 0-> c3, 1-> noise
		nse3_bw = 1.0       // noise band width (1..1000)
		// op 4
		op4_enable = 1
		op4_ratio = 1.0
		op4_bias = 0.0
		op4_amp = 1.0
		op4_velocity = 0.0
		op4_lfo1 = 0.0
		op4_lfo2 = 0.0
		op4_external = 0.0
		op4_left = 0
		op4_right = 0
		op4_key = 60
		op4_attack = 0.00
		op4_decay1 = 0.00
		op4_decay2 = 0.00
		op4_release = 0.00
		op4_breakpoint = 1.0
		op4_sustain = 1.0
		op4_env_mode = 0
		fm4_ratio = 1.00
		fm4_modscale = 1
		fm4_moddepth = 0.0
		fm4_lag = 0.00
		fm4_lfo1 = 0.00
		fm4_lfo2 = 0.00
		fm4_external = 0.00
		fm4_left = 0
		fm4_right = 0
		bzz4_n = 1        //  1..63
		bzz4_env = 16     //  +/- 63
		bzz4_lfo2 = 0.0    // lfo2 -> buzz
		bzz4_mix = 0.0    //  0-> c4, 1-> buzz
		bzz4_lag = 0.0|
		var x = In.kr(xbus,1);
		// envelopes
		//var hold_time = [op1_release,op2_release,op3_release,op4_release].max;
		var hold_time = max(op1_release, max(op2_release, max(op3_release, op4_release)));
		var env_floor = 0.000;
		var gate1 = Select.kr(op1_env_mode, [gate,Trig1.kr(gate,(op1_attack + op1_decay1 + op1_decay2))]);
		var env1 = EnvGen.kr(Env([env_floor,1,op1_breakpoint.max(env_floor),op1_sustain.max(env_floor),env_floor],
			[op1_attack,op1_decay1,op1_decay2,op1_release],\lin,3),gate1,doneAction: 0);
		var gate2 = Select.kr(op2_env_mode, [gate,Trig1.kr(gate,(op2_attack + op2_decay1 + op2_decay2))]);
		var env2 = EnvGen.kr(Env([env_floor,1,op2_breakpoint.max(env_floor),op2_sustain.max(env_floor),env_floor],
			[op2_attack,op2_decay1,op2_decay2,op2_release],\lin,3),gate2,doneAction: 0);
		var gate3 = Select.kr(op3_env_mode, [gate,Trig1.kr(gate,(op3_attack + op3_decay1 + op3_decay2))]);
		var env3 = EnvGen.kr(Env([env_floor,1,op3_breakpoint.max(env_floor),op3_sustain.max(env_floor),env_floor],
			[op3_attack,op3_decay1,op3_decay2,op3_release],\lin,3),gate3,doneAction: 0);
		var gate4 = Select.kr(op4_env_mode, [gate,Trig1.kr(gate,(op4_attack + op4_decay1 + op4_decay2))]);
		var env4 = EnvGen.kr(Env([env_floor,1,op4_breakpoint.max(env_floor),op4_sustain.max(env_floor),env_floor],
			[op4_attack,op4_decay1,op4_decay2,op4_release],\lin,3),gate4,doneAction: 0);
	    // Pitch envelope
		var pe = EnvGen.kr(Env([pe_a0,pe_a1,pe_a2,pe_a3,pe_a4],
			[pe_t1,pe_t2,pe_t3,pe_t4],\lin,pe_rnode,pe_loop),gate);
        // LFOs
		var lfov_env = EnvGen.kr(Env([0,0,1,0],[vdelay,vdelay,hold_time],\lin,2),gate);
		var lfo1_env = EnvGen.kr(Env([0,0,1,0],[lfo1_delay,lfo1_delay,hold_time],\lin,2),gate);
		var lfo2_env = EnvGen.kr(Env([0,0,1,0],[lfo2_delay,lfo2_delay,hold_time],\lin,2),gate);
		var lfos = LFCub.kr([vfreq, vfreq*lfo1_ratio, vfreq*lfo2_ratio],0,[lfov_env,lfo1_env,lfo2_env]);
		var vibsig = 1+(vsens.linlin(0,1,0,0.1)*((vdepth*lfos[0])+(xpitch*x)));
		var mlfo1 = LinXFade2.kr(1, lfos[1],[fm1_lfo1,fm2_lfo1,fm3_lfo1,fm4_lfo1].linlin(0,1,-1,1));
		var mlfo2 = LinXFade2.kr(1, lfos[2],[fm1_lfo2,fm2_lfo2,fm3_lfo2,fm4_lfo2].linlin(0,1,-1,1));
		var mxtern = LinXFade2.kr(1, x, [fm1_external,fm2_external,fm3_external,fm4_external].linlin(0,1,-1,1));
		var clfo1 = 1+LinXFade2.kr(1, lfos[1],[op1_lfo1,op2_lfo1,op3_lfo1,op4_lfo1].linlin(0,1,-1,1));
		var clfo2 = 1+LinXFade2.kr(1, lfos[2],[op1_lfo2,op2_lfo2,op3_lfo2,op4_lfo2].linlin(0,1,-1,1));
		var cxtern = LinXFade2.kr(1, x, [op1_external,op2_external,op3_external,op4_external].linlin(0,1,-1,1));
		// carrier frequencies
		var f = Lag2.kr(freq,port)*detune*vibsig;
		var cratios = [op1_ratio,op2_ratio,op3_ratio,op4_ratio]*f;
		var cfrequencies = (cratios+[op1_bias,op2_bias,op3_bias,op4_bias]) * [1+(op1_pe*pe), 1+(op2_pe*pe), 1+(op3_pe*pe), 1+(op4_pe*pe)];
		// velocities
		var cvelocities = LinXFade2.kr(1,velocity,[op1_velocity,op2_velocity,op3_velocity,op4_velocity].linlin(0,1,-1,1));
		var mvelocities = cvelocities;
		// keyscales
		var op1_left_octave = ((op1_key-keynumber)/12).max(0);
		var op1_right_octave = ((keynumber-op1_key)/12).max(0);
		var op2_left_octave = ((op2_key-keynumber)/12).max(0);
		var op2_right_octave = ((keynumber-op2_key)/12).max(0);
		var op3_left_octave = ((op3_key-keynumber)/12).max(0);
		var op3_right_octave = ((keynumber-op3_key)/12).max(0);
		var op4_left_octave = ((op4_key-keynumber)/12).max(0);
		var op4_right_octave = ((keynumber-op4_key)/12).max(0);
		var ckeyamps = dbamp([(op1_left*op1_left_octave)+(op1_right*op1_right_octave),
			(op2_left*op4_left_octave)+(op2_right*op2_right_octave),
			(op3_left*op3_left_octave)+(op3_right*op3_right_octave),
			(op4_left*op4_left_octave)+(op4_right*op4_right_octave)]);
		var mkeyamps = dbamp([(fm1_left*op1_left_octave)+(fm1_right*op1_right_octave),
		      (fm2_left*op4_left_octave)+(fm2_right*op2_right_octave),
		      (fm3_left*op3_left_octave)+(fm3_right*op3_right_octave),
		      (fm4_left*op4_left_octave)+(fm4_right*op4_right_octave)]);
		// modulators
		var mamps = [fm1_modscale*fm1_moddepth,fm2_modscale*fm2_moddepth,fm3_modscale*fm3_moddepth,fm4_modscale*fm4_moddepth]*
		             cfrequencies*mlfo1*mlfo2*mxtern*mvelocities*mkeyamps;
		var mfrequencies = [fm1_ratio,fm2_ratio,fm3_ratio,fm4_ratio]*f* [1+(op1_pe*pe), 1+(op2_pe*pe), 1+(op3_pe*pe), 1+(op4_pe*pe)];
		var menvs = Lag2.kr([env1,env2,env3,env4],[fm1_lag,fm2_lag,fm3_lag,fm4_lag]);
		var msigs = SinOsc.ar(mfrequencies,0,mamps*menvs);
		// carriers
		var camps = [op1_enable*op1_amp,op2_enable*op2_amp,op3_enable*op3_amp,op4_enable*op4_amp]*
		             cvelocities*clfo1*clfo2*cxtern*ckeyamps;
		var csig = SinOsc.ar(cfrequencies+msigs,0,camps*[env1,env2,env3,env4])*amp;
		var c1 = csig[0];
		var c2 = csig[1];
		var c3 = csig[2];
		var c4 = csig[3];
		var nsemod = LPF.ar(WhiteNoise.ar(),nse3_bw);
		var nserm = (c3*nsemod) * nse3_bw.expexp(1,1000,350,3);
		var bzz_max = 128;
		var bzz_env = Lag2.kr(env4,bzz4_lag)*bzz4_env;
		var bzz_harmonics = ((bzz4_n+bzz_env)+(bzz4_lfo2*lfos[2])).max(1).min(bzz_max);
		var bzz = Blip.ar(cfrequencies[3],bzz_harmonics)*camps[3]*env4*amp;
		var outsig;
		c3 = XFade2.ar(c3,nserm,nse3_mix.linlin(0,1,-1,1));
		c4 = XFade2.ar(c4,bzz,bzz4_mix.linlin(0,1,-1,1));
		outsig = (c1+c2+c3+c4);
		Out.ar([outbus1,outbus2,outbus3,outbus4],[c1,c2,c3,c4]);
		Out.ar(outbus,outsig*0.25);
		Linen.kr(gate, 0.01, 1, hold_time, doneAction); // Voice hold envelope

}).load)