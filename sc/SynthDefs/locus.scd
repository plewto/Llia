/*
** Locus, A Vector synth.
*/

(SynthDef (\Locus, {
    |
	outbus = 0               // primary audio output bus
	xoutbus = 2              // x signal output bus
	youtbus = 2              // y signal output bus
	xbus = 1023              // external -> x-axis
	ybus = 1023              // external -> y-axis
	gate = 1                 // envelope gate normalized highvsens
	doneAction = 2           // doneAction determined by key mode
	freq = 440               // primary frequency
	detune = 1               // MIDI pitch bend ratio
	amp = 0.1                // main output amplitude
	xamp = 1.0               // x-axis (ops A C) amp
	yamp = 1.0               // y-axis (ops B D) amp
	env1_attack = 0.00       // env1 ADDSR modulation source
	env1_decay1 = 0.00       // all env times (0..?)
	env1_decay2 = 0.00
	env1_release = 0.00
	env1_breakpoint = 1.00   // (0..1)
	env1_sustain= 1.00       // (0..1)
	env2_attack = 0.00       // env2 primary envelope
	env2_decay1 = 0.00
	env2_decay2 = 0.00
	env2_release = 0.00
	env2_breakpoint = 1.00   // (0..1)
	env2_sustain = 1.00      // (0..1)
	vfreq = 5.00             // vlfo - primary LFO & vibrato (0..99)
	vsens = 0.1              // vibrato sensitivity (0..1)
	vdepth = 0.0             // vibrato depth (0..1)
	vdelay = 0.0             // vibrato LFO onset delay (0..4)
	lfox_ratio = 1.0         // x-axis LFO frequency relative to vlfo
	lfox_delay = 0.0         // xlfo onset delay (0..4)
	lfoy_ratio = 0.5         // y-axis LFO frequency relative to vlfo
	lfoy_delay = 0.0         // ylfo onset delay (0..4)
	xpos = 0.0               // initial x-axis value (-1..+1)
	xpos_lfo = 0.0           // lfox -> x position (-1..+1)
	xpos_env1 = 0.0          // env1 -> x position (-1..+1)
	xpos_xbus = 0.0          // external bus x -> x position (-1..+1)
	ypos = 0.0               // initial y-axis value
	ypos_lfo = 0.0           // lfoy -> y position
	ypos_env1 = 0.0          // env1 -> y position
	ypos_ybus = 0.0          // external bus y -> y position
	// OPA - simple FM  [mod]->[car]
	opa_lfo_ratio  = 1.0     // relative to vlfo
	opa_lfo_wave   = 0.5     // (0..1) 0.5=tri
	opa_mod_ratio  = 1.0     // modulator frequency ratio (0.125...16)
	opa_mod_depth  = 1.0     // modulator output amp (0..1)
	opa_mod_scale  = 1.0     // modulator output scale (1,10,100,..,10000)
	opa_mod_env1   = 1.0     // env1 to mod depth (0..1)
	opa_mod_lfo    = 0.0     // lfo to mod depth (0..1)
	opa_car_ratio  = 1.0     // carrier frequency ratio (0,0.125...16)
	opa_car_bias   = 0       // carrier frequency bias (0...9999)
	opa_env_delay  = 0.0     // (0..1)
	opa_feedback   = 0.0     // (0..1)
	opa_pitch_env1 = 0.0     // (-1..+1)
	opa_pitch_lfo  = 0.0     // (-1..+1)
	opa_amp = 1.0            // (0..2)
	// OPB - simple FM [mod]->[car]
	opb_lfo_ratio  = 1.0     // relative to vlfo
	opb_lfo_wave   = 0.5     // (0..1) 0.5=tri
	opb_mod_ratio  = 1.0     // modulator frequency ratio (0.125...16)
	opb_mod_depth  = 1.0     // modulator output amp (0..1)
	opb_mod_scale  = 1.0     // modulator output scale (1,10,100,..,10000)
	opb_mod_env1   = 1.0     // env1 to mod depth (0..1)
	opb_mod_lfo    = 0.0     // lfo to mod depth (0..1)
	opb_car_ratio  = 1.0     // carrier frequency ratio (0,0.125...16)
	opb_car_bias   = 0       // carrier frequency bias (0...9999)
	opb_env_delay  = 0.0     // (0..1)
	opb_feedback   = 0.0     // (0..1)
	opb_pitch_env1 = 0.0     // (-1..+1)
	opb_pitch_lfo  = 0.0     // (-1..+1)
	opb_amp = 1.0            // (0..2)
	// OPC multi-wave subtractive
	opc_lfo_ratio  = 1.0     // relative to vlfo
	opc_lfo_wave   = 0.5     // (0..1) 0.5 = tri
	opc_wave       = 0.5     // cross mix tri/pulse/saw/noise (0..1)
	opc_wave_lfo   = 0.0     // lfo to wave mix (-1..+1)
	opc_wave_env1  = 0.0     // env1 to wave mix (-1..+1)
	opc_sine_ratio   = 1.0   // sine wave freq ratio (0.125..16)
	opc_pulse_ratio = 1.0    // pulse wave freq ratio    (0.125..16)
	opc_saw_ratio   = 1.0    // sawtooth wave freq ratio (0.125..16)
	opc_pulse_width     = 0.5 // (0..1)
	opc_pulse_width_lfo = 0.0 // (0..1)
	opc_noise_amp  = 0.0      // (0..2)
	opc_noise_lowpass = 16000 // (100..16k)
	opc_noise_highpass = 20   // (20..8k)
	opc_filter_freq = 16000   // (20..16k)
	opc_filter_freq_lfo = 0   // (-12k..+12k)
	opc_filter_freq_env1 = 0  // (-12k..+12k)
	opc_filter_res = 0.0      // (0..1)
	opc_env_delay = 0.0       // (0..1)
	opc_pitch_env1 = 0.0      // (-1..+1)
	opc_pitch_lfo = 0.0       // (-1..+1)
	opc_amp = 1.0             // (0..2)
	// OPD multi-wave subtractive
	opd_lfo_ratio  = 1.0      // relative to vlfo
	opd_lfo_wave   = 0.5      // (0..1) 0.5 = tri
	opd_wave       = 0.5      // cross mix tri/pulse/saw/noise (0..1)
	opd_wave_lfo   = 0.0      // lfo to wave mix (-1..+1)
	opd_wave_env1  = 0.0      // env1 to wave mix (-1..+1)
	opd_sine_ratio   = 1.0    // sine wave freq ratio (0.125..16)
	opd_pulse_ratio = 1.0     // pulse wave freq ratio    (0.125..16)
	opd_saw_ratio   = 1.0     // sawtooth wave freq ratio (0.125..16)
	opd_pulse_width     = 0.5 // (0..1)
	opd_pulse_width_lfo = 0.0 // (0..1)
	opd_noise_amp  = 0.0      // (0..2)
	opd_noise_lowpass = 16000 // (100..16k)
	opd_noise_highpass = 20   // (20..8k)
	opd_filter_freq = 16000   // (20..16k)
	opd_filter_freq_lfo = 0   // (-12k..+12k)
	opd_filter_freq_env1 = 0  // (-12k..+12k)
	opd_filter_res = 0.0      // (0..1)
	opd_env_delay = 0.0       // (0..1)
	opd_pitch_env1 = 0.0      // (-1..+1)
	opd_pitch_lfo = 0.0       // (-1..+1)
	opd_amp = 1.0             // (0..2)
	|
	var xextern = In.kr(xbus);
	var yextern = In.kr(ybus);
	var hold_time = env2_release*2;
	var vlfo_env = EnvGen.kr(Env([0,0,1,0],[vdelay,vdelay,hold_time],\lin,2),gate);
	var xlfo_env = EnvGen.kr(Env([0,0,1,0],[lfox_delay,lfox_delay,hold_time],\lin,2),gate);
	var ylfo_env = EnvGen.kr(Env([0,0,1,0],[lfoy_delay,lfoy_delay,hold_time],\lin,2),gate);
	var env_floor = 0.0001;
	var env1 = EnvGen.kr(Env([env_floor,1,env1_breakpoint.max(env_floor),env1_sustain.max(env_floor), env_floor],
		[env1_attack, env1_decay1, env1_decay2, env1_release],\lin,3),
		gate, 1,0,1,0);
	var env2 = EnvGen.kr(Env([env_floor,1,env2_breakpoint.max(env_floor),env2_sustain.max(env_floor), env_floor],
		[env2_attack, env2_decay1, env2_decay2, env2_release],\exp,3),
		gate, 1,0,1,doneAction);
	var vlfo = SinOsc.kr(vfreq)*vdepth*vsens.linlin(0,1,0,0.1)*vlfo_env;
	var xlfo = SinOsc.kr(vfreq*lfox_ratio)*xlfo_env;
	var ylfo = SinOsc.kr(vfreq*lfoy_ratio)*ylfo_env;
	var x = (xpos+(xlfo*xpos_lfo)+(env1*xpos_env1)+(xextern*xpos_xbus)).min(1).max(-1);
	var y = (ypos+(ylfo*ypos_lfo)+(env1*ypos_env1)+(yextern*ypos_ybus)).min(1).max(-1);
	var f0 = (freq*detune)*(1 + vlfo);
	var fm_feedback = LeakDC.ar(LocalIn.ar(2));
	// OPA FM [mod] -> [car]
	var alfo = VarSaw.kr(vfreq*opa_lfo_ratio,0,opa_lfo_wave);
	var aenv = DelayL.kr(env1,2,min(opa_env_delay.linlin(0,1,0,2),2));
	var afreq = f0 * (1 + (aenv * opa_pitch_env1 * 0.25) * (1 + (alfo * opa_pitch_lfo * 0.25)));
	var amod_freq = afreq*opa_mod_ratio;
	var acar_freq = (afreq*opa_car_ratio)+opa_car_bias;
	var amod_amp = acar_freq*opa_mod_scale*opa_mod_depth*
	    XFade2.kr(1.0,aenv,opa_mod_env1.linlin(0,1,-1,1))*
	    XFade2.kr(1,alfo,opa_mod_lfo.linlin(0,1,-1,1));
	var amod = SinOsc.ar(amod_freq,0,amod_amp);
	var afeedback_sig = opa_feedback.linlin(0,1,0,6)*fm_feedback[0]*acar_freq*0.2;
	var asig = SinOsc.ar(acar_freq+amod+afeedback_sig)*opa_amp*2;
	// OPB FM [mod] -> [car]
	var blfo = VarSaw.kr(vfreq*opb_lfo_ratio,0,opb_lfo_wave);
	var benv = DelayL.kr(env1,2,min(opb_env_delay.linlin(0,1,0,2),2));
	var bfreq = f0 * (1 + (benv * opb_pitch_env1 * 0.25) * (1 + (blfo * opb_pitch_lfo * 0.25)));
	var bmod_freq = bfreq*opb_mod_ratio;
	var bcar_freq = (bfreq*opb_car_ratio)+opb_car_bias;
	var bmod_amp = bcar_freq*opb_mod_scale*opb_mod_depth*
	    XFade2.kr(1.0,benv,opb_mod_env1.linlin(0,1,-1,1))*
	    XFade2.kr(1,blfo,opb_mod_lfo.linlin(0,1,-1,1));
	var bmod = SinOsc.ar(bmod_freq,0,bmod_amp);
	var bfeedback_sig = opb_feedback.linlin(0,1,0,6)*fm_feedback[1]*bcar_freq*0.2;
	var bsig = SinOsc.ar(bcar_freq+bmod+bfeedback_sig)*opb_amp*2;

	// OPC multi-wave subtractive.
	var clfo = VarSaw.kr(vfreq*opc_lfo_ratio,0,opc_lfo_wave);
	var cenv = DelayL.kr(env1,2,min(opc_env_delay.linlin(0,1,0,2),2));
	var cfreq = f0 * (1 + (cenv * opc_pitch_env1 * 0.25) * (1 + (clfo * opc_pitch_lfo * 0.25)));
	var cpulse_width = opc_pulse_width + (clfo * opc_pulse_width_lfo * 0.5);
	var csine = SinOsc.ar(cfreq*opc_sine_ratio);
	var cpulse = Pulse.ar(cfreq*opc_pulse_ratio,cpulse_width);
	var csaw = Saw.ar(cfreq*opc_saw_ratio);
	var cnoise = LPF.ar(HPF.ar(WhiteNoise.ar(opc_noise_amp*2),opc_noise_highpass),opc_noise_lowpass);
	var csig_array = [csine,csine,cpulse,cpulse,csaw,csaw,cnoise,cnoise];
	var cwave_select = (opc_wave + (clfo.linlin(-1,1,0,1)*opc_wave_lfo) + (cenv * opc_wave_env1)).linlin(0,1,0,7);
	var cfilter_in = SelectX.ar(cwave_select,csig_array);
	var cfilter_freq = (opc_filter_freq + (clfo * opc_filter_freq_lfo) +
		(cenv * opc_filter_freq_env1)).max(50).min(16000);
	var cfilter_gain = opc_filter_res.linlin(0,1,0,3.9);
	var cfilter_agc = min(3.0, opc_filter_res.linexp(0,1,1,3));
	var csig = MoogFF.ar(cfilter_in,cfilter_freq,cfilter_gain)*cfilter_agc*opc_amp;

	// OPD multi-wave subtractive.
	var dlfo = VarSaw.kr(vfreq*opd_lfo_ratio,0,opd_lfo_wave);
	var denv = DelayL.kr(env1,2,min(opd_env_delay.linlin(0,1,0,2),2));
	var dfreq = f0 * (1 + (denv * opd_pitch_env1 * 0.25) * (1 + (dlfo * opd_pitch_lfo * 0.25)));
	var dpulse_width = opd_pulse_width + (dlfo * opd_pulse_width_lfo * 0.5);
	var dsine = SinOsc.ar(dfreq*opd_sine_ratio);
	var dpulse = Pulse.ar(dfreq*opd_pulse_ratio,dpulse_width);
	var dsaw = Saw.ar(dfreq*opd_saw_ratio);
	var dnoise = LPF.ar(HPF.ar(WhiteNoise.ar(opd_noise_amp*2),opd_noise_highpass),opd_noise_lowpass);
	var dsig_array = [dsine,dsine,dpulse,dpulse,dsaw,dsaw,dnoise,dnoise];
	var dwave_select = (opd_wave + (dlfo.linlin(-1,1,0,1)*opd_wave_lfo) + (denv * opd_wave_env1)).linlin(0,1,0,7);
	var dfilter_in = SelectX.ar(dwave_select,dsig_array);
	var dfilter_freq = (opd_filter_freq + (dlfo * opd_filter_freq_lfo) +
		(denv * opd_filter_freq_env1)).max(50).min(16000);
	var dfilter_gain = opd_filter_res.linlin(0,1,0,3.9);
	var dfilter_agc = min(3.0, opd_filter_res.linexp(0,1,1,3));
	var dsig = MoogFF.ar(dfilter_in,dfilter_freq,dfilter_gain)*dfilter_agc*opd_amp;

	// Crossmix vectors.
	var xvector = (xpos + (xlfo*xpos_lfo) + (env1*xpos_env1) + (xextern * xpos_xbus)).max(-1).min(1);
	var yvector = (ypos + (ylfo*ypos_lfo) + (env1*ypos_env1) + (yextern * ypos_ybus)).max(-1).min(1);
	var xsig = HPF.ar(XFade2.ar(asig,csig,xvector),30)*env2*amp*xamp;
	var ysig = HPF.ar(XFade2.ar(bsig,dsig,yvector),30)*env2*amp*yamp;
	LocalOut.ar([asig,bsig]);
	Out.ar(xoutbus,xsig);
	Out.ar(youtbus,ysig);
	Out.ar(outbus,xsig+ysig);
	}).load)
