/*
** Slug is a hybrid instrument with many performance controls.
**
** Tone consist of 4 elements:
**      Filtered pulse.
**      Pluck (Karplus Strong)
**      2 FM "stacks"   [modulator]-->[carrier]
**
** The pluck signal may frequency modulate any of the FM components.
**
** Control signals:
**      Single LFO with optional noise and onset delay.
**      2 ADSR envelopes
**      2 Percussive envelopes.
**
** Performance controls:
**      velocity  --> portamento time
**                --> ADSR attack times
** 	              --> pulse filter
** 		          --> FM modulation depths
** 	              --> amplitude
**      key-track --> ADSR attack times
**                --> pulse filter
** 		          --> FM modulation depth
** 		          --> amplitude
*/

(SynthDef (\Slug, {
    |
	outbus = 0             // primary audio output bus
	xbus = 1023            // optional control bus
	gate = 1               // envelope gate normalized high
	doneAction = 2         // doneAction determined by key mode
	freq = 440             // primary frequency
	keynumber = 69         // MIDI key number
	detune = 1             // MIDI pitch bend ratio
	velocity = 1.0         // normalized range (0..1)
	port = 0.00            // Portemento 0..1
	velocity_port = 0.00   // Velocity to port time
	break_key = 60         // MIDI key number
	amp = 0.100            // Main amplitude
	// LFO
	vfreq = 5.00           // Vibrato frequency
	vdelay = 0.00          // Vibrato onset delay 0..2
	vsens = 0.1            // Vibrato sensitivity 0..1
	vdepth = 0.00          // Vibrato depth 0..1 (programmed)
	vibrato = 0.00         // Vibrato depth 0..1
	vnoise = 0.00          // Vibrato low freq noise amp 0..1 (noise always delayed)
	xpitch = 0.00          // xbus -> pitch 0..1
	// Env 1 (modulation)
	env_mode = 0           // Common envelope mode. 0=gate, 1=trig.
	env1_attack = 0.01     // 0..4
	env1_decay = 0.10      // 0..4
	env1_sustain = 1.00    // 0..1
	env1_release = 0.01    // 0..4
	env1_velocity_attack=0 // velocity --> attack -1 .. +1
	env1_key_attack = 0.00 // keynumber --> attack -1 .. +1
	penv1_decay = 1.00     // Percussive envelope 1 decay 0..4
	// Env 2 (primary)
	env2_attack = 0.01
	env2_decay = 0.10
	env2_sustain = 1.00
	env2_release = 0.01
	env2_velocity_attack = 0
	env2_key_attack = 0
	penv2_decay = 1.00
	// Pulse tone
	pulse_ratio = 1.00           // >0 (tune)
	pulse_width = 0.5            // 0..1
	pulse_width_env1 = 0.00      // 0..1
	pulse_width_lfo = 0.00       // 0..1
	pulse_filter_res = 0.5       // 0..1
	pulse_filter_cutoff = 16000  // Hz
	pulse_filter_env1 = 0        // -+ Hz.
	pulse_filter_penv1 = 0       // -+ Hz.
	pulse_filter_lfo = 0         // -+ Hz.
	pulse_filter_x = 0           // -+ Hz. external -> filter
	pulse_filter_velocity = 0    // -+ Hz
	pulse_filter_left_track = 0  // -+ Hz (per octave)
	pulse_filter_right_track = 0 // -+ Hz (per octave)
	pulse_amp_env = 1.00         // cross mix env2 and penv2,  0=env2, 1=penv2
	pulse_amp = 1.00
	pulse_enable = 1             // 0=off, 1=on
	// Karplus Strong tone
	pluck_ratio = 1.00           // >0 (tune)
	pluck_decay = 3.00           // >0
	pluck_harmonic = 1           // (1,2,3,...,16?)
	pluck_width = 1              // 0|1  0=50%  1=75%
	pluck_excite = 0.0           // Excitation signal 0=pulse, 1=white noise
	pluck_damp = 0.5             // 0..1
	pluck_velocity = 0.00        // 0..1 velocity -> pluck amp
	pluck_left_scale = 0         // left key scale in db/oct
	pluck_right_scale = 0        // right key scale in db/oct
	pluck_amp = 1.00             // 0..2
    pluck_enable = 1             // 0=off, 1=on
    // FM 1
	car1_ratio = 0.5             // 0 <= ratio <= 16
	car1_bias = 0                // 0 <= bias <= 999  in Hz.
	car1_velocity = 0.0          // velocity -> car1 amp
	car1_left_scale = 0          // left key -> car1 amp in db/oct.
	car1_right_scale = 0         // right key -> car1 amp in db/oct.
	car1_mod_scale = 1           // FM depth scale factor 1,2,8,16,...,512,1024,2048(?)
	car1_xmod_depth = 0.00       // 0..1, external sig -> car 1 mod depth
	car1_mod_depth = 1.0         // FM depth mod1 -> car1
	car1_mod_pluck = 0.0         // FM depth pluck -> car1
	car1_amp_env = 0.00          // main amp env cross mix, 0=env2, 1=penv2
	car1_enable = 1              // 0=off, 1=on
	car1_amp = 1.00              // 0..2
	mod1_ratio = 0.5             // 0 < ratio <= 16
	mod1_mod_pluck = 0.0         // 0..1 pluck -> mod1 FM
	mod1_velocity = 0.00         // 0..1
	mod1_left_scale = 0          // db/octave
	mod1_right_scale = 0         // db/octave
	mod1_env = 0.00              // 0=env1, 1=penv1
	mod1_enable = 1              // 0=off, 1=on
    // FM 2
	car2_ratio = 0.5             // 0 <= ratio <= 16
	car2_bias = 0                // 0 <= bias <= 999  in Hz.
	car2_velocity = 0.0          // velocity -> car2 amp
	car2_left_scale = 0          // left key -> car2 amp in db/oct.
	car2_right_scale = 0         // right key -> car2 amp in db/oct.
	car2_mod_scale = 1           // FM depth scale factor 1,2,8,16,...,512,1024,2048(?)
	car2_xmod_depth = 0.00       // 0..1, external sig -> car 1 mod depth
	car2_mod_depth = 1.0         // FM depth mod1 -> car2
	car2_mod_pluck = 0.0         // FM depth pluck -> car2
	car2_amp_env = 0.00          // main amp env cross mix, 0=env2, 1=penv2
	car2_enable = 1              // 0=off, 1=on
	car2_amp = 1.000             // 0..2
	mod2_ratio = 0.5             // 0 < ratio <= 16
	mod2_mod_pluck = 0.0         // 0..1 pluck -> mod2 FM
	mod2_velocity = 0.00         // 0..1
	mod2_left_scale = 0          // db/octave
	mod2_right_scale = 0         // db/octave
	mod2_env = 0.00              // 0=env1, 1=penv1
	mod2_enable = 1              // 0=off, 1=on
    |
	var xsig = In.kr(xbus);
	var left_key_diff = (break_key-keynumber).max(0);
	var left_key_octave = left_key_diff/12;
	var right_key_diff = (keynumber-break_key).max(0);
	var right_key_octave = right_key_diff/12;
	var env_floor = 0.001;
	// Env1
	var env1_gate = Select.kr(env_mode,[gate,Trig.kr(gate,env1_attack+env1_decay+env1_release)]);
	var env1_vel_scale = velocity.linlin(0,1,0,env1_velocity_attack);
	var env1_left_scale = left_key_octave.linlin(0,5,0,env1_key_attack);
	var env1_right_scale = right_key_octave.linlin(0,5,0,-1*env1_key_attack);
	var env1_attack_time = (env1_attack+env1_vel_scale+env1_left_scale+env1_right_scale).max(0);
	var env1 = EnvGen.kr(Env([env_floor,1,env1_sustain.max(env_floor),env_floor],
		[env1_attack,env1_decay,env1_release],\exp,2),env1_gate)-env_floor;
	var penv1 = EnvGen.kr(Env.perc(0.01,penv1_decay),gate);  // Percussive version of env1
	// Env2
	var env2_gate = Select.kr(env_mode,[gate,Trig.kr(gate,env2_attack+env2_decay+env2_release)]);
	var env2_vel_scale = velocity.linlin(0,1,0,env2_velocity_attack);
	var env2_left_scale = left_key_octave.linlin(0,5,0,env2_key_attack);
	var env2_right_scale = right_key_octave.linlin(0,5,0,-1*env2_key_attack);
	var env2_attack_time = (env2_attack+env2_vel_scale+env2_left_scale+env2_right_scale).max(0);
	var env2 = EnvGen.kr(Env([env_floor,1,env2_sustain.max(env_floor),env_floor],
		[env2_attack,env2_decay,env2_release],\exp,2),env2_gate,1,0,1,doneAction)-env_floor;
	var penv2 = EnvGen.kr(Env.perc(0.01,penv2_decay),gate);  // Percussive version of env2
	// LFO
	var venv = EnvGen.kr(Env([0,0,1,0],[vdelay,vdelay,1.1*env2_release],\lin,2),env2_gate);
	var nlfo_env = EnvGen.kr(Env([0,0,1,0],[vdelay,2,1.1*env2_release],\lin,2,env2_gate));
	var slfo = LFCub.kr(vfreq);
	var nlfo = BPF.kr(WhiteNoise.kr(),vfreq*2,0.1,vnoise*14)*nlfo_env;
	var lfo = (slfo+nlfo) * (vibrato+(vdepth*venv));
	var vsig = 1+(vsens.linlin(0,1,0,0.05)*(lfo + (xsig*xpitch)));
	// Portamento & Primary freq.
	var ptime = port+(velocity.linlin(0,1,1,0)*velocity_port);
	var f0 = Lag2.kr(freq,ptime)*detune;
	// Pulse signal
	var pls_width = pulse_width + (env1 * pulse_width_env1) + (lfo * pulse_width_lfo);
	var pls_ffreq1 = pulse_filter_cutoff + (env1 * pulse_filter_env1) +
	(penv1 * pulse_filter_penv1) +
	(lfo * pulse_filter_lfo) +
	(xsig * pulse_filter_x) +
	(velocity * pulse_filter_velocity) +
	(left_key_octave * pulse_filter_left_track) +
	(right_key_octave * pulse_filter_right_track);
	var pls_ffreq = pls_ffreq1.max(50).min(16000);
	var pls_filter_rq = pulse_filter_res.linlin(0,1,1,0.05);
	var pls_filter_agc = 1.0;
	var pls_raw = Pulse.ar(f0*pulse_ratio,pls_width);
	var pls_env = LinXFade2.kr(env2,penv2,pulse_amp_env.linlin(0,1,-1,1));
	var pls_sig = RLPF.ar(Pulse.ar(f0*pulse_ratio,pls_width),pls_ffreq,pls_filter_rq)*pls_filter_agc*pls_env*pulse_enable;
	// Karplus Strong signal
	var ks_max_delay = 0.2;
	var ks_freq = (f0*pluck_ratio*vsig).max(16);
	var ks_delay = (1/ks_freq).min(ks_max_delay);
	var ks_excite_pw = Select.kr(pluck_width,[0.5,0.75]);
	var ks_excite = LinXFade2.ar(Pulse.ar(ks_freq*pluck_harmonic,ks_excite_pw),
		BrownNoise.ar(), pluck_excite.linlin(0,1,-1,1));
	var ks_coef = pluck_damp.linlin(0,1,0.05,0.9).max(0.05).min(0.9);
	var ks_amp = LinXFade2.kr(1,velocity,pluck_velocity.linlin(0,1,-1,1)) *
	dbamp(pluck_left_scale*left_key_octave) *
	dbamp(pluck_right_scale*right_key_octave);
	var ks_sig = LeakDC.ar(Pluck.ar(ks_excite,gate, ks_max_delay,ks_delay,pluck_decay*2, ks_coef)*ks_amp*pluck_enable);
	// FM Pair 1
	var car1_freq = ((f0*car1_ratio)+car1_bias)*vsig;
	var mod1_freq = (f0*mod1_ratio)*vsig*(1 + (ks_sig*mod1_mod_pluck));
	var mod1_amp = LinXFade2.kr(1,velocity,mod1_velocity.linlin(0,1,-1,1)) *
	dbamp(mod1_left_scale*left_key_octave) *
	dbamp(mod1_right_scale*right_key_octave);
	var mod1 = LeakDC.ar(SinOsc.ar(mod1_freq,0,LinXFade2.kr(env1,penv1,mod1_env.linlin(0,1,-1,1))*mod1_amp*mod1_enable));
	var car1_amp2 = LinXFade2.kr(1,velocity,car1_velocity.linlin(0,1,-1,1)) *
	dbamp(car1_left_scale*left_key_octave) *
	dbamp(car1_right_scale*right_key_octave) *
	car1_enable * car1_amp;
	var car1_mod_sig = (car1_freq * car1_mod_scale * LinXFade2.kr(1,xsig,car1_xmod_depth.linlin(0,1,-1,1))) *
	(1 + (mod1 * car1_mod_depth)) *
	(1 + (ks_sig * car1_mod_pluck));
	var car1_sig = SinOsc.ar(car1_freq+car1_mod_sig,0,car1_amp2*LinXFade2.kr(env2,penv2,car1_amp_env.linlin(0,1,-1,1)));
	// FM Pair 2
	var car2_freq = ((f0*car2_ratio)+car2_bias)*vsig;
	var mod2_freq = (f0*mod2_ratio)*vsig*(1 + (ks_sig*mod2_mod_pluck));
	var mod2_amp = LinXFade2.kr(1,velocity,mod2_velocity.linlin(0,1,-1,1)) *
	dbamp(mod2_left_scale*left_key_octave) *
	dbamp(mod2_right_scale*right_key_octave);
	var mod2 = LeakDC.ar(SinOsc.ar(mod2_freq,0,LinXFade2.kr(env1,penv1,mod2_env.linlin(0,1,-1,1))*mod2_amp*mod2_enable));
	var car2_amp2 = LinXFade2.kr(1,velocity,car2_velocity.linlin(0,1,-1,1)) *
	dbamp(car2_left_scale*left_key_octave) *
	dbamp(car2_right_scale*right_key_octave) *
	car2_enable*car2_amp;
	var car2_mod_sig = (car2_freq * car2_mod_scale * LinXFade2.kr(1,xsig,car2_xmod_depth.linlin(0,1,-1,1))) *
	(1 + (mod2 * car2_mod_depth)) *
	(1 + (ks_sig * car2_mod_pluck));
	var car2_sig = SinOsc.ar(car2_freq+car2_mod_sig,0,car2_amp2*LinXFade2.kr(env2,penv2,car2_amp_env.linlin(0,1,-1,1)));
	var sig = (car1_sig+car2_sig+(pls_sig*pulse_amp)+(ks_sig*ks_amp));
	sig = HPF.ar(sig,30)*amp;
	Out.ar(outbus,sig);
}).load)
