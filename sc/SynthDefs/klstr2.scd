/*
** Klstr2
*/

(SynthDef (\Klstr2, {
    |
	outbus1 = 0            // primary audio output bus 1
	outbus2 = 1            // primary audio output bus 2
	xbus = 1023            // external control input bus
	gate = 1               // envelope gate normalized high
	doneAction = 2         // doneAction determined by key mode
	freq = 440             // primary frequency
	keynumber = 69         // MIDI key number
	detune = 1             // MIDI pitch bend ratio
	amp = 0.1              // Main output amplitude
	lfoFreq = 1.0          // Modulation LFO
	lfo2Ratio = 1.0        // Vibrato LFO
	vibrato = 0.0
	env1_attack = 0.0      // Modulation envelope attack
	env1_decay1 = 0.0
	env1_decay2 = 0.0
	env1_release = 0.0
	env1_breakpoint = 1.0
	env1_sustain = 1.0
	env1_mode = 0
	env2_attack = 0.0      // Amplitude Envelope
	env2_decay1 = 0.0
	env2_decay2 = 0.0
	env2_release = 0.0
	env2_breakpoint = 1.0
	env2_sustain = 1.0
	env2_mode = 0
	spread = 0.0           // osc frequency spread
	spread_env1 = 0.0
	spread_lfo1 = 0.0
	spread_external = 0.0
	cluster = 0.0
	cluster_env1 = 0.0
	cluster_lfo1 = 0.0
	cluster_lfo2 = 0.0
	cluster_external = 0.0
	pw = 0.5                // Common pulse width, tones 3 & 4
	pw_lfo1 = 0.0
	pw_env1 = 0.0
	harm1 = 4               // Harmonic count tone 1 (blip)
	harm1_env1 = 0
	harm1_env2 = 0
	harm1_lfo1 = 0
	harm1_lfo2 = 0
	harm2 = 4               // Harmonic count tone 2 (blip)
	harm2_env1 = 0
	harm2_lfo1 = 0
	harm2_external = 0
	harm2_lag = 0.0
	noise_lowpass = 16000
	noise_lowpass_env1 = 0
	noise_lowpass_lfo1 = 0
	noise_highpass = 10
	noise_amp = 0.0
	// Filter input mixer
	// Tone A <-  blip1 + pulse3
	// Tone B <-  blip2 + pulse4
	balance_a = 0.0      // -1.0(moogFF) ... +1.0(Resonz)
    balance_b = 0.0
	balance_noise = 0.0
    // MoogFF
	f1_freq = 16000
	f1_freq_env1 = 0
	f1_freq_lfo1 = 0
	f1_freq_lfo2 = 0
	f1_freq_external = 0
	f1_res = 0.0
	f1_amp = 1
	f1_pan = 0.25
	// Resonz
	f2_freq = 1000
	f2_freq_env1 = 0
	f2_freq_env2 = 0
	f2_freq_lfo1 = 0
	//f2_freq_lfo2 = 0
	f2_freq_lag = 0.0

	f2b_lag = 0.0
	f2b_offset = 0
	f2b_fade = 0.0
	f2_res = 0.0
	f2_amp = 1
	f2_pan = -0.25
	out2_lag = 0.0     // Lag applied to main out 2
	|
	var x = In.kr(xbus);
	var lfo1 = LFCub.kr(lfoFreq);
	var lfo2 = LFCub.kr(lfoFreq*lfo2Ratio);
	var env_floor = 0.0001;
	var env1_gate = Select.kr(env1_mode, [gate, Trig.kr(gate, (env1_attack+env1_decay1+env1_decay2))]);
	var env1 = EnvGen.kr(Env([env_floor,1,env1_breakpoint.max(env_floor),env1_sustain.max(env_floor), env_floor],
		[env1_attack, env1_decay1, env1_decay2, env1_release],\exp,3),
		env1_gate, 1,0,1,0);
	var env2_gate = Select.kr(env2_mode, [gate, Trig.kr(gate, (env2_attack+env2_decay1+env2_decay2))]);
	var env2 = EnvGen.kr(Env([env_floor,1,env2_breakpoint.max(env_floor),env2_sustain.max(env_floor), env_floor],
		[env2_attack, env2_decay1, env2_decay2, env2_release],\exp,3),
		env2_gate, 1,0,1,0,doneAction);
	var fspread = max(0, (spread + (env1 * spread_env1) + (lfo1 * spread_lfo1.linlin(-1,1,-0.25, 0.25)) + (x * spread_external)));
	var r1 = 1.000;
	var r2 = 0.20 * fspread + 1;
	var r3 = 0.50 * fspread + 1;
	var r4 = fspread + 1;
	var r5 = 1.5 * fspread + 1;
	var r6 = 2.0 * fspread + 1;
	var f = freq*detune*(vibrato*lfo2+1);
	var rho = (cluster + (lfo1 * cluster_lfo1 * 0.25) + (lfo2 * cluster_lfo2 * 0.25) + (env1 * cluster_env1) + (x * cluster_external)).linlin(0,1,0,2*pi);
	var a1 = cos(rho);
	var a2 = sin(rho);
	var a3 = sin(rho*1.2);
	var a4 = sin(rho*1.4);
	var a5 = sin(rho*1.6);
	var a6 = sin(rho*1.8);
	var h1 = max(1, harm1 + (lfo1 * harm1_lfo1) + (lfo2 * harm1_lfo2) + (env1 * harm1_env1) + (env2 * harm1_env2));
	var h2 = max(1, Lag2.kr(harm2 + (lfo1 * harm2_lfo1) + (env1 * harm2_env1) + (x * harm2_external),harm2_lag.linlin(0,1,0,4)));
	var tone1 = Blip.ar(r1*f,h1)*a1;
	var tone2 = Blip.ar(r2*f,h2)*a2;
	var pulse_width = max(0.05, min(0.95, pw + (lfo1 * 0.5 * pw_lfo1) + (env1 * pw_env1)));
	var tone3 = Pulse.ar(r3*f,pulse_width)*a3;
	var tone4 = Pulse.ar(r4*f,pulse_width)*a4;
	var tone5 = Pulse.ar(r5*f,pulse_width)*a5;
	var tone6 = Pulse.ar(r6*f,pulse_width)*a6;
	var composite_a = Pan2.ar(tone1+tone3+tone5,balance_a);
	var composite_b = Pan2.ar(tone2+tone4+tone6,balance_b);
	var nseLowCutoff = max(80, min(16000, noise_lowpass + (noise_lowpass_env1 * env1) + (noise_lowpass_lfo1 * lfo1)));
	var nseHighCutoff = max(10, min(10000, noise_highpass));
	var nse = Pan2.ar(LPF.ar(HPF.ar(WhiteNoise.ar(),nseHighCutoff),nseLowCutoff)*noise_amp,balance_noise);
	var f1_in = composite_a[1]+composite_b[1]+nse[1];
	var f1freq = max(80, min(16000, f1_freq + (f1_freq_env1 * env1) + (f1_freq_lfo1 * lfo1) + (f1_freq_lfo2 * lfo2) + (f1_freq_external * x)));
	var f1gain = f1_res.linlin(0,1,0,3.9);
	var f1_agc = min(3.0, f1_res.linexp(0,1,1,3));
	var f1out = Pan2.ar(MoogFF.ar(f1_in,f1freq,f1gain)*f1_amp,f1_pan)*f1_agc;
	var f2_in = composite_a[0]+composite_b[0]+nse[0];
	var f2freq = max(80, min(16000, f2_freq + (f2_freq_env1 * env1) + (f2_freq_env2 * env2) + (f2_freq_lfo1 * lfo1)));
	var f2rq = f2_res.linexp(0,1,1,0.05);
	var f2a_agc = min(3.0, f2_res.linlin(0,1,1,3));

	var f2b_agc = f2a_agc*2;
	var f2a = Resonz.ar(f2_in,f2freq,f2rq)*f2a_agc;
	var f2b = BPF.ar(f2_in,Lag2.kr(max(100, min(16000,f2freq+f2b_offset)),f2b_lag),f2rq)*f2b_agc;
	var f2out = Pan2.ar(XFade2.ar(f2b,f2a,f2b_fade), f2_pan)*f2_amp;

	var out1 = (f1out[0]+f2out[0])*env2;
	var out2 = (f1out[1]+f2out[1])*Lag2.kr(env2,out2_lag.linlin(0,1,0,4));
	Linen.kr(gate,0.01,1, env2_release, doneAction); // Voice hold env
	Out.ar(outbus1,out1*amp);
	Out.ar(outbus2,out2*amp);
}).load)


