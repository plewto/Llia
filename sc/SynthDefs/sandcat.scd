


(SynthDef (\Sandcat, {
	|outbus1 = 0          // Audio outputs
	outbus2 = 1
	xbus1 = 1024          // external control buses
	xbus2 = 1024
	gate = 1
	doneAction = 2
	freq = 440
	keynumber = 69
	detune = 1
	velocity = 1.0
	amp = 1.0                    // 0..2 main linear amp
	// LFOS and clocks
	//   lfov - (master) vibrato LFO with onset delay
	//   lfo1 - general mod source
	//   lfo2 - general mod source, with Fm from LFO1
	//   clk1 - extra trigger source
	//   clk2 - extra trigger source
	vfreq = 7.0              // 0..100  vibrato frequency
	vdelay = 0.0             // 0..2     vibrato onset delay
	vdepth = 0.0             // 0..1     programmed vibrato depth
	vibrato = 0.0            // 0..1     manual vibrato depth
	vsens = 0.1              // 0..1     vibrato sensitivity
	vxbus1 = 0.0             // 0..1     xbus1 -> pitch
	lfo1_ratio = 1.0         // 0..1     LFO1 freq ratio relative to vfreq
	lfo1_freq_lfo2 = 0       // 0..8     LFO2 -> LFO1 freq.
	lfo2_ratio = 1.0         // 0..1     LFO2 freq ratio relative to vfreq
	lfo2_freq_lfo1 = 0       // 0..8     LFO1 -> LFO2 freq.
	clk1_ratio = 1
	clk2_ratio = 1
	// Envelopes
	//    ADSR1   - general mod source
	//    ADSR2   - general mod source
	//    ADSR3   - master amp envelope
	//    perc3
	env1_attack = 0.01
	env1_decay = 0.0
	env1_sustain = 1.0
	env1_release = 1.0
	env1_trig_src = 0
	env1_trig_mode = 0            // 0->gate, 1->trig
	env2_attack = 0.01
	env2_decay = 0.0
	env2_sustain = 1.0
	env2_release = 1.0
	env2_trig_src = 0
	env2_trig_mode = 0
	env3_attack = 0.01
	env3_decay = 0.0
	env3_sustain = 1.0
	env3_release = 1.0
	env3_trig_src = 0
	env3_trig_mode = 0

	env4_attack = 0.01
	env4_decay = 0.0
	env4_sustain = 1.0
	env4_release = 1.0
	env4_trig_src = 0
	env4_trig_mode = 0

	// Karplus Strong excite signals.
	//
	ex1_harmonic = 1               // 1,2,3,...,8
	ex1_lfo1 = 0                   // 1..8 LFO1 -> pulse freq
	ex1_env1 = 0                   // 1..8 env1 -> pulse freq
	ex1_pw = 0.5                   // 0..1
	ex1_pw_lfo1 = 0                // 0..1 LFO1 -> pw
	ex1_noise_select = 0           // 0|1  0->white 1->pink
	ex1_source_mix = 0             // -1..+1  -1 -> pulse +1 -> noise
	ex2_harmonic = 1               // 1,2,3,...,8
	ex2_lfo2 = 0                   // 1..8 LFO2 -> pulse freq
	ex2_env2 = 0                   // 1..8 env2 -> pulse freq
	ex2_pw = 0.5                   // 0..1
	ex2_pw_lfo2 = 0                // 0..1 LFO1 -> pw
	ex2_noise_select = 0           // 0|1  0->white 1->pink
	ex2_source_mix = 0             // -1..+1  -1 -> pulse +1 -> noise
	// Karpuls Strong trigger selections.
	ks1_trig_src = 0               // 0->gate, 1->LFO1, 2->LFO2, 3->x1, 4->x2
	ks2_trig_src = 0
	// karplus Strong params
	ks1_ratio = 1                  // >0 KS Pluck tuning.
	ks1_decay = 2                  // 0..6
	ks1_coef = 0.3                 // 0..1 Feedback coefficient.
	ks1_velocity = 0               // 0..1 velocity -> ks amp
	ks2_ratio = 1
	ks2_decay = 2
	ks2_coef = 0.3
	ks2_velocity = 0
	// FM Stack 1
	stack1_break_key = 60          // 0..127  MIDI key number
	stack1_fb = 0.0                // 0..4    feedback carrier1 -> modulator 1
	stack1_fb_lfo1 = 0.0           // 0..1    LFO1 -> feedback amount
	mod1_ratio = 1.0               // 0..16   realative frequency
	mod1_bias = 0.0                // 0..999  fixed frequency offset in Hz.
	mod1_ks1 = 0.0                 // 0..?   ks1 -> mod1   FM depth
	mod1_env1 = 1                  // 0|1    0=gate, 1=env1
	mod1_lag = 0.0                 // 0..1   env lag time
	mod1_lfo1 = 0.0                // 0..1   LFO1 -> mod1 amp
	mod1_velocity = 0.0            // 0..1   velocity -> mod1 amp
	mod1_left_scale = 0            // -99, -18..+18  key scale   db/octave
	mod1_right_scale = 0           // -99, -18..+18
	car1_ratio = 1.0               // 0..16   carrier freq ratio
	car1_bias = 0.0                // 0..999  fixed freq bias in Hz.
	car1_mod1= 0.0                 // 0..?    mod1 -> car1 FM depth
	car1_ks1 = 0.0                 // 0..?    ks1 -> car1 FM depth
	car1_env_mode= 0               // 0|1     0=env1  1=gate
	car1_lfo1=0                    // 0..1    LFO1 -> car1 amp
	car1_velocity= 0               // 0..1    velocity -> car amp
	car1_left_scale=0              // -99,-18..+18  key scale db/octacve
	car1_right_scale=0             // -99,-18..+18
	// FM Stack 2
	stack2_break_key = 60          // 0..127  MIDI key number
	stack2_fb = 0.0                // 0..4    feedback carrier2 -> modulator 2
	stack2_fb_lfo2 = 0.0           // 0..1    LFO2 -> feedback amount
	mod2_ratio = 1.0               // 0..16   realative frequency
	mod2_bias = 0.0                // 0..999  fixed frequency offset in Hz.
	mod2_ks2 = 0.0                 // 0..?   ks2 -> mod2   FM depth
	mod2_env2 = 1                  // 0|1    0=gate, 1=env2
	mod2_lag = 0.0                 // 0..1   env lag time
	mod2_lfo2 = 0.0                // 0..1   LFO2 -> mod2 amp
	mod2_velocity = 0.0            // 0..1   velocity -> mod1 amp
	mod2_left_scale = 0            // -99, -18..+18  key scale   db/octave
	mod2_right_scale = 0           // -99, -18..+18
	car2_ratio = 1.0               // 0..16   carrier freq ratio
	car2_bias = 0.0                // 0..999  fixed freq bias in Hz.
	car2_mod1=0.0                  // 0..?    mod1 -> car2 FM depth
	car2_mod2= 0.0                 // 0..?    mod2 -> car2 FM depth
	car2_ks2 = 0.0                 // 0..?    ks2 -> car2 FM depth
	car2_env_mode= 0               // 0|1     0=env1  1=gate
	car2_lfo2=0                    // 0..1    LFO2 -> car2 amp
	car2_velocity= 0               // 0..1    velocity -> car amp
	car2_left_scale=0              // -99,-18..+18  key scale db/octacve
	car2_right_scale=0             // -99,-18..+18
	// Mixer
	ks1_amp = 1.0
	ks2_amp = 1.0
	stack1_amp = 1.0
	stack2_amp = 1.0
	ks1_pan = 0.0
	ks2_pan = 0.0
	stack1_pan = 0.0
	stack2_pan = 0.0

	// Filter 1
	f1_cutoff = 16000
	f1_track = 0.0
	f1_env3 = 0
	f1_lfo1 = 0
	f1_lfov = 0
	f1_velocity = 0
	f1_res = 0
	f1_pan = 0

	// Filter 2
	f2_cutoff = 16000
	f2_track = 0
	f2_env4 = 0
	f2_lfo2 = 0
	f2_lfov = 0
	f2_velocity = 0
	f2_res = 0
	f2_pan = 0|
	var white = WhiteNoise.ar();
	var pink = PinkNoise.ar(4);
	var lfnoise = LFNoise0.kr(3);
	var xsig = In.kr([xbus1,xbus2]);
	var venv = EnvGen.kr(Env([0,0,1,1],[vdelay,vdelay,env3_release],\lin,2),gate);
	var lfov = LFCub.kr(vfreq,0,vibrato+(vdepth*venv));
	var vsig = 1 + (vsens.linlin(0,1,0,0.2) * lfov + (vxbus1 * xsig[0]));
	var kr_feedback = LocalIn.kr(1);
	var lfo1_freq = ((vfreq*lfo1_ratio) + (kr_feedback*lfo1_freq_lfo2)).abs;
	var lfo1 = LFTri.kr(lfo1_freq);
	var lfo1p = lfo1.linlin(-1,1,0,1);
	var lfo2_freq = ((vfreq*lfo2_ratio) + (lfo1p*lfo2_freq_lfo1)).abs;
	var lfo2 = LFTri.kr(lfo2_freq);
	var lfo2p = lfo2.linlin(-1,1,0,1);
	var clk = LFPulse.kr([clk1_ratio,clk2_ratio]*vfreq);
	var hold_times = [env1_attack+env1_decay, env2_attack+env2_decay, env3_attack+env3_decay];
	var trig_sources = [gate,gate*clk[0],gate*clk[1],gate*lfo1,gate*lfo2,gate*xsig[0],gate*xsig[1],lfnoise*gate,
		clk[0],clk[1],lfo1,lfo2,xsig[0],xsig[1],lfnoise];
	var e1_trigsrc = Select.kr(env1_trig_src, trig_sources);
	var e1_gate = Select.kr(env1_trig_mode, [e1_trigsrc, Trig1.kr(e1_trigsrc,hold_times[0])]);
	var env1 = EnvGen.kr(Env.adsr(env1_attack,env1_decay,env1_sustain,env1_release),e1_gate);
	var e2_trigsrc = Select.kr(env2_trig_src, trig_sources);
	var e2_gate = Select.kr(env2_trig_mode, [e2_trigsrc, Trig1.kr(e2_trigsrc,hold_times[1])]);
	var env2 = EnvGen.kr(Env.adsr(env2_attack,env2_decay,env2_sustain,env2_release),e2_gate);
	var e3_trigsrc = Select.kr(env3_trig_src, trig_sources);
	var e3_gate = Select.kr(env3_trig_mode, [e3_trigsrc, Trig1.kr(e3_trigsrc,hold_times[2])]);
	var env3 = EnvGen.kr(Env.adsr(env3_attack,env3_decay,env3_sustain,env3_release),e3_gate,1,0,1,0);
	var e4_trigsrc = Select.kr(env4_trig_src, trig_sources);
	var e4_gate = Select.kr(env4_trig_mode, [e4_trigsrc, Trig1.kr(e4_trigsrc,hold_times[2])]);
	var env4 = EnvGen.kr(Env.adsr(env4_attack,env4_decay,env4_sustain,env4_release),e4_gate,1,0,1,0);
	var hold_env = EnvGen.kr(Env.asr(0,1,env3_release.max(env4_release)),gate,1,0,1,doneAction);

	var f0 = freq*detune*vsig;
	// KS Excite signals
	var exp_freq = f0*[ex1_harmonic+(ex1_lfo1*lfo1)+(ex1_env1*env1),
		ex2_harmonic+(ex2_lfo2*lfo2)+(ex2_env2*env2)];
	var exp_pw = [ex1_pw+(ex1_pw_lfo1*lfo1),ex2_pw+(ex2_pw_lfo2*lfo2)];
	var excite = LinXFade2.ar(Pulse.ar(exp_freq,exp_pw),
		Select.ar([ex1_noise_select,ex2_noise_select],[white,pink]),
		[ex1_source_mix,ex2_source_mix]);
	// Karplus Strong components
	var ks_trig = Select.kr([ks1_trig_src,ks2_trig_src],trig_sources);
	var ks_min_freq = 15;
	var ks_max_delay = 1/ks_min_freq;
	var ks_freq = ([ks1_ratio,ks2_ratio]*f0).abs.max(ks_min_freq).min(12000);
	var ks_delay = 1/(ks_freq);
	var ks_velocity = XFade2.kr(velocity,1,[ks1_velocity,ks2_velocity].linlin(0,1,1,-1));
	var ks_sigs = LeakDC.ar(Pluck.ar(excite,ks_trig,ks_max_delay,ks_delay,[ks1_decay,ks2_decay],[
		ks1_coef,ks2_coef],ks_velocity));
	var feedback = LeakDC.ar(LocalIn.ar(2)*
		[stack1_fb,stack2_fb]*
		LinXFade2.kr(1,[lfo1,lfo2],[stack1_fb_lfo1,stack2_fb_lfo2].linlin(0,1,-1,1)));
	// FM Stack 1
	var stack1_left_octave = ((stack1_break_key-keynumber)/12).max(0);
	var stack1_right_octave = ((keynumber-stack1_break_key)/12).max(0);
	var m1_amp = XFade2.kr(1,Lag2.kr(env1,mod1_lag),mod1_env1.linlin(0,1,-1,1)) *
	XFade2.kr(1,lfo1p,mod1_lfo1.linlin(0,1,-1,1)) *
	XFade2.kr(1,velocity,mod1_velocity.linlin(0,1,-1,1)) *
	dbamp(stack1_left_octave*mod1_left_scale) *
	dbamp(stack1_right_octave*mod1_right_scale);
	var m1f = (f0*mod1_ratio)+mod1_bias;
	var m1_modsig = m1f * (1 + (ks_sigs[0]*mod1_ks1) + feedback[0]);
	var mod1 = LeakDC.ar(SinOsc.ar(m1_modsig,0,m1_amp));
	var c1f = (f0*car1_ratio)+car1_bias;
	var c1_amp = Select.kr(car1_env_mode, [env1,gate]) *
	XFade2.kr(1,lfo1,car1_lfo1.linlin(0,1,-1,1)) *
	XFade2.kr(1,velocity,car1_velocity.linlin(0,1,-1,1))*
	dbamp(stack1_left_octave*car1_left_scale)*
	dbamp(stack1_right_octave*car1_right_scale);
	var c1_modsig = c1f*(1 + (ks_sigs[0]*car1_ks1) + (mod1*car1_mod1));
	var car1 = LeakDC.ar(SinOsc.ar(c1_modsig,0,c1_amp));
	// FM Stack 2
	var stack2_left_octave = ((stack2_break_key-keynumber)/12).max(0);
	var stack2_right_octave = ((keynumber-stack2_break_key)/12).max(0);
	var m2_amp = XFade2.kr(1,Lag2.kr(env2,mod2_lag),mod2_env2.linlin(0,1,-1,1)) *
	XFade2.kr(1,lfo1p,mod2_lfo2.linlin(0,1,-1,1)) *
	XFade2.kr(1,velocity,mod2_velocity.linlin(0,1,-1,1)) *
	dbamp(stack2_left_octave*mod2_left_scale) *
	dbamp(stack2_right_octave*mod2_right_scale);
	var m2f = (f0*mod2_ratio)+mod2_bias;
	var m2_modsig = m2f * (1 + (ks_sigs[1]*mod2_ks2) + feedback[1]);
	var mod2 = LeakDC.ar(SinOsc.ar(m2_modsig,0,m2_amp));
	var c2f = (f0*car2_ratio)+car2_bias;
	var c2_amp = Select.kr(car2_env_mode, [env2,gate]) *
	XFade2.kr(1,lfo1,car2_lfo2.linlin(0,1,-1,1)) *
	XFade2.kr(1,velocity,car2_velocity.linlin(0,1,-1,1))*
	dbamp(stack2_left_octave*car2_left_scale)*
	dbamp(stack2_right_octave*car2_right_scale);
	var c2_modsig = c2f * (1 + (ks_sigs[1]*car2_ks2) + (mod1*car2_mod1) + (mod2*car2_mod2));
	var car2 = LeakDC.ar(SinOsc.ar(c2_modsig,0,c2_amp));
	// Mixer
	var mixout = Pan2.ar(ks_sigs[0]*ks1_amp,ks1_pan) +
	Pan2.ar(ks_sigs[1]*ks2_amp,ks2_pan) +
	Pan2.ar(car1*stack1_amp,stack1_pan) +
	Pan2.ar(car2*stack2_amp,stack2_pan);
	// Filters
	var ff1_freq = (f1_cutoff +
		(f0 * f1_track) +
		(env3 * f1_env3) +
		(lfo1 * f1_lfo1) +
		(lfov * f1_lfov) +
		(velocity * f1_velocity)).max(20).min(16000);
	var ff1_rq = f1_res.linlin(0,1,1,0.01);
	var ff1_agc = min(3.0, f1_res.linexp(0,1,1,3));
	var ff1_out = Pan2.ar(RLPF.ar(mixout[0],ff1_freq,ff1_rq,ff1_agc),f1_pan);
	var ff2_freq = (f2_cutoff +
		(f0 * f2_track) +
		(env4 * f2_env4) +
		(lfo2 * f2_lfo2) +
		(lfov * f2_lfov) +
		(velocity * f2_velocity)).max(20).min(16000);
	var ff2_rq = f2_res.linlin(0,1,1,0.01);
	var ff2_agc = min(3.0, f2_res.linexp(0,1,1,3));
	var ff2_out = Pan2.ar(RLPF.ar(mixout[1],ff2_freq,ff2_rq,ff2_agc),f2_pan);
	LocalOut.kr(lfo2p);
	LocalOut.ar([car1,car2]);
	Out.ar(outbus1, ff1_out*amp);
	Out.ar(outbus2, ff2_out*amp);
}).load)




















