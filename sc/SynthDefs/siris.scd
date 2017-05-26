/*
** Siris
*/

(SynthDef (\Siris, {
	|outbus = 0
	gate = 1
	freq = 440
	detune = 1.0
	doneAction = 0
	velocity = 0.5
	port = 0.0                // portamento time 0..1
	amp = 1.0                 // main linear amp
	// Common LFO
	timebase = 1.0            // common LFO frequenciy >0
	vratio = 7.0              // vibrato LFO freq ratio
	vsens = 0.1               // vibrato sensitivity 0..1
	vdepth = 0.0              // vibrato depth 0..1
	vdelay = 0.0              // vibrato onset delay 0..2
	// Common ADSR env
	env_attack = 0.01         // attack time
	env_decay = 0.1           //
	env_sustain = 1.0         //
	env_release = 3.0         //
	env_mode = 0              // 0=gate, 1=trig
	// Excitation signals
	ex_lfo_ratio = 1          // relative ex LFO frequency
	ex_env_attack = 0.001
	ex_env_decay = 3.000
    // Excitation pulse 1
	ex1_harmonic = 1          // int 1,2,3,...
	ex1_harmonic_lfo = 0      // exLFO -> harmonic
	ex1_harmonic_env = 0      // exEnv -> harmonic
	ex1_pw = 0.5              // pulse width 0..1
	ex1_pwm_lfo = 0           // exLFO -> pw
	ex1_pwm_env = 0           // exEnv -> pw
    // Excitation pulse 2
	ex2_harmonic = 1          // int 1,2,3,...
	ex2_harmonic_lfo = 0      // exLFO -> harmonic
	ex2_harmonic_env = 0      // exEnv -> harmonic
	ex2_pw = 0.5              // pulse width 0..1
	ex2_pwm_lfo = 0           // exLFO -> pw
	ex2_pwm_env = 0           // exEnv -> pw
	// KS line 1
	ks1_excite1 = 1.0         // excite1 pulse -> ks1
	ks1_excite2 = 0.0         // excite2 pulse -> ks1
	ks1_excite_noise = 0.0    // noise -> ks1 excite pulse
	ks1_excite_white = 1      // 0=pink 1=white (only applies if ks1_exite_noise is non-zero)
	ks1_ratio = 1.0           // Tuning
	ks1_decay = 3             //
	ks1_coef = 0.3            // ks feedback coeficienat 0..1
	ks1_trig_mode = 0         // 0=gate, 1=trem, 2=continuous
	ks1_trig_ratio = 1        // trig LFO frequency relative to timebase.
	ks1_clip_enable = 0       // 0=disable, 1=enable
	ks1_clip_gain = 1         // pre-clipler gain
	ks1_clip_threshold = 1    // >0..1
	ks1_attack = 0.0          //
	ks1_velocity = 0.0        // velocity -> ks1 amp
	ks1_amp = 1.0             // linear amp
	// KS line 2
	ks2_delay = 0.0           // trigger delay in seconds
	ks2_excite1 = 0.0         // excite1 pulse -> ks2
	ks2_excite2 = 1.0         // excite2 pulse -> ks2
	ks2_excite_noise = 0.0    // noise -> ks2 excite pulse
	ks2_excite_white = 1      // 0=pink 1=white (only applies if ks2_exite_noise is non-zero)
	ks2_ratio = 1.0           // Tuning
	ks2_decay = 3             //
	ks2_coef = 0.3            // ks feedback coeficienat 0..1
	ks2_trig_mode = 0         // 0=gate, 1=trem, 2=continuous
	ks2_trig_ratio = 1        // trig LFO frequency relative to timebase.
	ks2_clip_enable = 0       // 0=disable, 1=enable
	ks2_clip_gain = 1         // pre-clipler gain
	ks2_clip_threshold = 1    // >0..1
	ks2_attack = 0.0          //
	ks2_velocity = 0.0        // velocity -> ks2 amp
	ks2_amp = 1.0             // linear amp
	// Noise
	nse_attack = 0.01
	nse_decay = 3.0           //
	nse_velocity =0.0         // velocity -> noise amp
	nse_lowpass = 20000       // Hz
	nse_highpass = 20         // Hz
	nse_amp = 0               // linear amp
	// Filter
	filter_cutoff = 16000     // Hz
	filter_env = 0            // ADSR env -> cutoff, Hz
	filter_vlfo = 0           // vibrato LFO -> cutoff, Hz
	filter_velocity = 0       // velocity -> cutoff
	filter_track = 0          // key freq -> cutoff
	filter_res = 0|           // 0..1
	var venv = EnvGen.kr(Env([0,0,1,0],[vdelay,vdelay,env_release],'lin',2),gate);
	var envtrig = Select.kr(env_mode,[gate,Trig1.kr(gate,env_attack+env_decay)]);
	var adsr = EnvGen.kr(Env.adsr(env_attack,env_decay,env_sustain,env_release),envtrig,1,0,1,doneAction);
	var exenv = EnvGen.kr(Env.perc(ex_env_attack,ex_env_decay),gate);
	var vlfo = LFCub.kr(timebase*vratio,0,venv*vdepth);
	var vsig = 1+(vlfo*vsens);
	var exlfo = LFTri.kr(timebase*ex_lfo_ratio);
	var f0 = (Lag2.kr(freq*detune,port.linlin(0,1,0,0.4))*vsig).max(15).min(20000);
	// Excite signal 1
	var ex1harm = (ex1_harmonic + (exlfo * ex1_harmonic_lfo) + (exenv * ex1_harmonic_env)).max(1);
	var ex1freq = f0*ex1harm;
	var ex1pw = ex1_pw + (exlfo * ex1_pwm_lfo.linlin(-1,1,-0.5,0.5)) + (exenv * ex1_pwm_env);
	var ex1 = Pulse.ar(ex1freq,ex1pw);
	// Excite signal 2
	var ex2harm = (ex2_harmonic + (exlfo * ex2_harmonic_lfo) + (exenv * ex2_harmonic_env)).max(1);
	var ex2freq = f0*ex2harm;
	var ex2pw = ex2_pw + (exlfo * ex2_pwm_lfo.linlin(-1,1,-0.5,0.5)) + (exenv * ex2_pwm_env);
	var ex2 = Pulse.ar(ex2freq,ex2pw);
	// Noise
	var pink = PinkNoise.ar(4);
	var white = WhiteNoise.ar();
	var nsenv = EnvGen.kr(Env.asr(nse_attack,1,nse_decay),gate);
	var nsamp = XFade2.kr(1,velocity,nse_velocity.linlin(0,1,-1,1))*nse_amp;
	var nssig = LPF.ar(HPF.ar(white,nse_highpass),nse_lowpass,nsenv*nsamp);
	// Karplus-Strong 1
	var ks1_freq = f0*ks1_ratio;
	var ks1_nse = Select.ar(ks1_excite_white, [pink, white]);
	var ks1_excite = LeakDC.ar((ex1*ks1_excite1) + (ex2*ks1_excite2) + (ks1_nse * ks1_excite_noise));
	var ks1_trem = LFPulse.ar(timebase*ks1_trig_ratio);
	var ks1_sus = LFPulse.ar(0.9*ks1_freq);
	var ks1_trig = Select.ar(ks1_trig_mode, [K2A.ar(gate),ks1_trem,ks1_sus]);
	var ks1a = Pluck.ar(ks1_excite, ks1_trig, 0.2, 1/ks1_freq, ks1_decay, ks1_coef);
	var ks1b = Select.ar(ks1_trig_mode, [ks1a,ks1a,ks1a.clip2(1)]);
	var ks1c = (ks1b*ks1_clip_gain).clip2(ks1_clip_threshold);
	var ks1env = EnvGen.kr(Env.asr(ks1_attack,1.0,ks1_decay),gate);
	var ks1amp = ks1_amp*XFade2.kr(1,velocity,ks1_velocity.linlin(0,1,-1,1));
	var ks1 = Select.ar(ks1_clip_enable, [ks1b,ks1c])*ks1env*ks1amp;
    // Karplus-Strong 2
    var ks2_max_delay = 0.1;
	var ks2_freq = f0*ks2_ratio;
	var ks2_nse = Select.ar(ks2_excite_white, [pink, white]);
	var ks2_excite = LeakDC.ar((ex1*ks2_excite1) + (ex2*ks2_excite2) + (ks2_nse * ks2_excite_noise));
	var ks2_trem = LFPulse.ar(timebase*ks2_trig_ratio);
	var ks2_sus = LFPulse.ar(0.9*ks2_freq);
	var ks2_trig = DelayL.ar(Select.ar(ks2_trig_mode, [K2A.ar(gate),ks2_trem,ks2_sus]), ks2_max_delay,ks2_delay.min(ks2_max_delay));
	var ks2a = Pluck.ar(ks2_excite, ks2_trig, 0.2, 1/ks2_freq, ks2_decay, ks2_coef);
	var ks2b = Select.ar(ks2_trig_mode, [ks2a,ks2a,ks2a.clip2(1)]);
	var ks2c = (ks2b*ks2_clip_gain).clip2(ks2_clip_threshold);
	var ks2env = EnvGen.kr(Env.asr(ks2_attack,1.0,ks2_decay),gate);
	var ks2amp = ks2_amp*XFade2.kr(1,velocity,ks2_velocity.linlin(0,1,-1,1));
	var ks2 = Select.ar(ks2_clip_enable, [ks2b,ks2c])*ks2env*ks2amp;
	var filter_in = LeakDC.ar(ks1+ks2+nssig);
	var ffreq = filter_cutoff + (filter_env * adsr) + (filter_vlfo * vlfo) + (filter_velocity * velocity) + (f0 * filter_track);
	var ffgain = filter_res.linlin(0,1,0,3.99);
	var fagc = min(3.0, filter_res.linexp(0,1,1,3));
	var ffout = MoogFF.ar(filter_in,ffreq.max(20).min(16000),ffgain)*adsr*amp*fagc;
	Out.ar(outbus, ffout);
}).load)
