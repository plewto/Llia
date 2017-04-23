/*
** Sol
*/

(SynthDef (\Sol, {
    |
	outbus = 0             // primary audio output bus
	xout = 2               // x stack audio output
	yout = 2               // y stack audio output
	vxbus = 1023           // external control -> x-axis
	vybus = 1023           // external control -> y-axis
	ctrlbus = 1023         // general external control bus
	gate = 1               // envelope gate normalized high
	doneAction = 2         // doneAction determined by key mode
	freq = 440             // primary frequency
	detune = 1             // MIDI pitch bend ratio
	port = 0.0             // portamento time 0..1
	amp = 0.3              // Master gain
	timebase = 7.00         // master LFO time reference in Hz
	// Vibrato
	vratio = 1              // vibrato freq ratio
	vsens = 0.1             // vibrato sensitivity
	vdepth = 0.0            // vibrato depth
	vdelay = 0.0            // vibrato onset dealy
	pitch_ctrlbus = 0.0     // external ctrlbus -> pitch
	// X Axis
	xlfo_ratio = 1.0        // X LFO frequency ratio
	xlfo_wave = 0.5         // saw/tri  0.5 = tri
	xlfo_delay = 0.0        // xlfo onset delay
	xenv_attack = 0.0       // x-axis ADSR
	xenv_decay = 0.0
	xenv_sustain = 0.0
	xenv_release = 0.0
	xenv_lfo_trig = 0       // 0 trig<-gate  1 trig<-lfo
	xpos = 0.0              // initial x position (-1..+1)
	xpos_xlfo = 0.0         // pos<-lfo (-1..+1)
	xpos_xenv = 0.0         // pos<-env (-1..+1)
	xpos_vxbus= 0.0         // pos<-external (-1..+1)
	xamp = 1.0              // x-axis signals combined gain
	// Y Axis
	ylfo_ratio = 1.0        // X LFO frequency ratio
	ylfo_wave = 0.5         // saw/tri  0.5 = tri
	ylfo_delay = 0.0        // xlfo onset delay
	yenv_attack = 0.0       // x-axix ADSR
	yenv_decay = 0.0
	yenv_sustain = 0.0
	yenv_release = 0.0
	yenv_lfo_trig = 0       // 0 trig<-gate  1 trig<-lfo
	ypos = 0.0              // initial x positin (-1..+1)
	ypos_ylfo = 0.0         // pos<-lfo (-1..+1)
	ypos_yenv = 0.0         // pos<-env (-1..+1)
	ypos_vybus= 0.0         // pos<-external (-1..+1)
	yamp = 1.0              // y-axis signals combined gain
	// General LFO A        // general LFOS A & B Sine
	alfo_ratio = 1.0
	alfo_delay = 0.0
	// General LFO B
	blfo_ratio = 1.0
	blfo_delay = 0.0
	// General ADSR Env A
	aenv_attack = 0.00
    aenv_decay = 0.00
	aenv_sustain = 1.00
	aenv_release = 0.00
	aenv_lfo_trig = 0
	// General ADSR Env B
	benv_attack = 0.00
	benv_decay = 0.00
	benv_sustain = 0.00
	benv_release = 0.00
	benv_lfo_trig = 0
	// Primary output ADDSR Env C
	cenv_attack = 0.00
	cenv_decay1 = 0.00
	cenv_decay2 = 0.00
	cenv_release = 0.00
	cenv_breakpoint = 1.0
	cenv_sustain = 1.0
	cenv_trig_mode = 0            // arg count = 24
	// OP A (fm pair)
	opa_mod_ratio = 1.00
	opa_mod_scale = 1
	opa_mod_depth = 1.00
	opa_mod_alfo = 0.00           // lfoa -> mod depth
	opa_mod_aenv = 0.00           // enva -> mod depth
	opa_car_ratio = 1.00
	opa_car_bias = 0.00
	opa_feedback = 0.00
	opa_cross_feedback = 0.00
	opa_amp = 1.0
    // OP B (fm pair)
	opb_mod_ratio = 1.00
	opb_mod_scale = 1
	opb_mod_depth = 1.00
	opb_mod_blfo = 0.00
	opb_mod_benv = 0.00
	opb_car_ratio = 1.00
	opb_car_bias = 0.00
	opb_feedback = 0.00
	opb_cross_feedback = 0.00
	opb_amp = 1.0
	// OP C (saw/pulse/tri/noise)
	opc_saw_ratio = 1.00
	opc_pulse_ratio = 0.50
	opc_pulse_width = 0.50
	opc_pulse_width_alfo = 0.0
	opc_wave = 0   // multi wave selection
	opc_wave_alfo = 0.0
	opc_wave_aenv = 0.0
	opc_noise_amp = 0.0
	opc_filter_track = 16 // rel to saw freq
	opc_filter_aenv = 1   // rel to saw freq
	opc_amp = 1.0
	// OP D (saw/pulse/tri/noise)
	opd_saw_ratio = 1.00
	opd_pulse_ratio = 0.50
	opd_pulse_width = 0.50
	opd_pulse_width_blfo = 0.0
	opd_wave = 0   // multi wave selection
	opd_wave_blfo = 0.0
	opd_wave_benv = 0.0
	opd_noise_amp = 0.0
	opd_filter_track = 16  // rel to saw freq
	opd_filter_benv = 1   // rel to saw freq
	opd_amp = 1.0
	xfilter_freq = 16000   // Hz
	xfilter_track = 0      // key track
	xfilter_freq_aenv = 0  //
	xfilter_freq_cenv = 0
	xfilter_freq_alfo = 0
	xfilter_freq_vlfo = 0
	xfilter_res = 0
	yfilter_freq = 16000   // Hz
	yfilter_track = 0      // key track
	yfilter_freq_benv = 0  //
	yfilter_freq_cenv = 0
	yfilter_freq_blfo = 0
	yfilter_freq_vlfo = 0
	yfilter_res = 0|
	var vxsig = In.kr(vxbus);
	var vysig = In.kr(vybus);
	var ctrlsig = In.kr(ctrlbus);
	var hold_time = cenv_release;
	// LFOs
	var vlfo_env = EnvGen.kr(Env([0,0,1,0],[vdelay,vdelay,hold_time],\lin,2),gate);
	var xlfo_env = EnvGen.kr(Env([0,0,1,0],[xlfo_delay,xlfo_delay,hold_time],\lin,2),gate);
	var ylfo_env = EnvGen.kr(Env([0,0,1,0],[ylfo_delay,ylfo_delay,hold_time],\lin,2),gate);
	var alfo_env = EnvGen.kr(Env([0,0,1,0],[alfo_delay,alfo_delay,hold_time],\lin,2),gate);
	var blfo_env = EnvGen.kr(Env([0,0,1,0],[blfo_delay,blfo_delay,hold_time],\lin,2),gate);
	var vlfo = LFCub.kr(timebase*vratio)*(vlfo_env*vdepth);
	var xlfo = VarSaw.kr(timebase*xlfo_ratio, 0, xlfo_wave,xlfo_env);
	var ylfo = VarSaw.kr(timebase*ylfo_ratio, 0, ylfo_wave,ylfo_env);
	var alfo = LFCub.kr(timebase*alfo_ratio,0,alfo_env);
	var blfo = LFCub.kr(timebase*blfo_ratio,0,blfo_env);
    // Envelopes
	var xenv_gate = Select.kr(xenv_lfo_trig,[gate,xlfo]);
	var yenv_gate = Select.kr(yenv_lfo_trig,[gate,ylfo]);
	var aenv_gate = Select.kr(aenv_lfo_trig,[gate,alfo]);
	var benv_gate = Select.kr(benv_lfo_trig,[gate,blfo]);
	var cenv_gate = Select.kr(cenv_trig_mode, [gate, Trig.kr(gate, (cenv_attack+cenv_decay1+cenv_decay2))]);
	var xenv = EnvGen.kr(Env.adsr(xenv_attack,xenv_decay,xenv_sustain,xenv_release,1,\lin),xenv_gate);
	var yenv = EnvGen.kr(Env.adsr(yenv_attack,yenv_decay,yenv_sustain,yenv_release,1,\lin),yenv_gate);
	var aenv = EnvGen.kr(Env.adsr(aenv_attack,aenv_decay,aenv_sustain,aenv_release,1,\lin),aenv_gate);
	var benv = EnvGen.kr(Env.adsr(benv_attack,benv_decay,benv_sustain,benv_release,1,\lin),benv_gate);
	var cenv_lin = EnvGen.kr(Env([0,1,cenv_breakpoint,cenv_sustain,0],
		[cenv_attack,cenv_decay1,cenv_decay2,cenv_release],\lin,3),
		cenv_gate,1,0,1,doneAction);
	var cenv = cenv_lin*cenv_lin;
	// General
	var f0 = (Lag2.kr(freq,port)*detune)*(1 + (vsens.linlin(0,1,0,0.2) * (vlfo + (ctrlsig * pitch_ctrlbus))));
	var fm_feedback = LocalIn.ar(2);
	// OPA  FM Pair [mod]->[car]
	var opa_car_freq = (f0*opa_car_ratio)+opa_car_bias;
	var opa_mod_freq = f0*opa_mod_ratio;
	var opa_mod_envsig = XFade2.kr(1.0,aenv,opa_mod_aenv.linlin(0,1,-1,1));
	var opa_mod_lfosig = XFade2.kr(1.0,alfo,opa_mod_alfo.linlin(0,1,-1,1));
	var opa_mod_amp = opa_mod_scale*opa_mod_depth*opa_mod_envsig*opa_mod_lfosig*opa_car_freq;
	var opa_fbsig = fm_feedback[0]*opa_feedback*opa_car_freq;
	var opa_cross_fbsig = fm_feedback[1]*opa_cross_feedback*opa_car_freq;
	var opa_modsig = LeakDC.ar(opa_fbsig + opa_cross_fbsig + SinOsc.ar(opa_mod_freq,0,opa_mod_amp));
	var opa_sig = SinOsc.ar(opa_car_freq+opa_modsig);  // A carrier pre gain scale.
	// OPB  FM Pair [mod]->[car]
	var opb_car_freq = (f0*opb_car_ratio)+opb_car_bias;
	var opb_mod_freq = f0*opb_mod_ratio;
	var opb_mod_envsig = XFade2.kr(1.0,benv,opb_mod_benv.linlin(0,1,-1,1));
	var opb_mod_lfosig = XFade2.kr(1.0,blfo,opb_mod_blfo.linlin(0,1,-1,1));
	var opb_mod_amp = opb_mod_scale*opb_mod_depth*opb_mod_envsig*opb_mod_lfosig*opb_car_freq;
	var opb_fbsig = fm_feedback[1]*opb_feedback*opb_car_freq;
	var opb_cross_fbsig = fm_feedback[0]*opb_cross_feedback*opb_car_freq;
	var opb_modsig = LeakDC.ar(opb_fbsig + opb_cross_fbsig + SinOsc.ar(opb_mod_freq,0,opb_mod_amp));
	var opb_sig = SinOsc.ar(opb_car_freq+opb_modsig);  // B carrier pre gain scale.
	// Vector x  A <---> B
	var x_control_sig = (xpos + (xlfo*xpos_xlfo) + (xenv*xpos_xenv) + (vxsig*xpos_vxbus)).min(1).max(-1);
	var xsig = LeakDC.ar(XFade2.ar(opa_sig*opa_amp,opb_sig*opb_amp,x_control_sig));
	// OPC Saw/Pulse/Noise
	var opc_saw_freq = (f0*opc_saw_ratio).max(20);
	var opc_saw_sig = Saw.ar(opc_saw_freq);
	var opc_tri_sig = LeakDC.ar(LPF.ar(abs(opc_saw_sig),(opc_saw_freq*6).min(16000)))*3;
	var opc_pulse_freq = (f0*opc_pulse_ratio).max(20);
	var opc_pw = opc_pulse_width + (opc_pulse_width_alfo * alfo * 0.5);
	var opc_pulse_sig = Pulse.ar(opc_pulse_freq,opc_pw);
	var opc_noise_sig = HPF.ar(WhiteNoise.ar(),2000)*2*opc_noise_amp;
	var opc_wave_array = [opc_tri_sig,opc_pulse_sig,opc_saw_sig];
	var opc_wave_select = (opc_wave + (opc_wave_alfo * alfo) + (opc_wave_aenv * aenv)).linlin(0,1,0,3);
	var opc_wave_sig = SelectX.ar(opc_wave_select, opc_wave_array);
	var opc_filter_in = opc_wave_sig + opc_noise_sig;
	var opc_filter_freq = (opc_saw_freq * (opc_filter_track + (aenv * opc_filter_aenv))).max(50).min(16000);
	var opc_sig = LPF.ar(opc_filter_in,opc_filter_freq);
	// OPD Saw/Pulse/Noise
	var opd_saw_freq = (f0*opd_saw_ratio).max(20);
	var opd_saw_sig = Saw.ar(opd_saw_freq);
	var opd_tri_sig = LeakDC.ar(LPF.ar(abs(opd_saw_sig),(opd_saw_freq*6).min(16000)))*3;
	var opd_pulse_freq = (f0*opd_pulse_ratio).max(20);
	var opd_pw = opd_pulse_width + (opd_pulse_width_blfo * blfo * 0.5);
	var opd_pulse_sig = Pulse.ar(opd_pulse_freq,opd_pw);
	var opd_noise_sig = HPF.ar(WhiteNoise.ar(),2000)*2*opd_noise_amp;
	var opd_wave_array = [opd_tri_sig,opd_pulse_sig,opd_saw_sig];
	var opd_wave_select = (opd_wave + (opd_wave_blfo * blfo) + (opd_wave_benv * benv)).linlin(0,1,0,3);
	var opd_wave_sig = SelectX.ar(opd_wave_select, opd_wave_array);
	var opd_filter_in = opd_wave_sig + opd_noise_sig;
	var opd_filter_freq = (opd_saw_freq * (opd_filter_track + (benv * opd_filter_benv))).max(50).min(16000);
	var opd_sig = LPF.ar(opd_filter_in,opd_filter_freq);
	// Vector y  C <---> D
	var y_control_sig = (ypos + (ylfo*ypos_ylfo) + (yenv*ypos_yenv) + (vysig*ypos_vybus)).min(1).max(-1);
	var ysig = XFade2.ar(opc_sig*opc_amp,opd_sig*opd_amp,y_control_sig);
	// XFilter
	var xff_freq = (xfilter_freq +
		(freq*xfilter_track) +
		(aenv*xfilter_freq_aenv) +
		(cenv*xfilter_freq_cenv) +
		(alfo*xfilter_freq_alfo) +
		(vlfo*xfilter_freq_vlfo)).max(50).min(16000);
	var xff_gain = xfilter_res.linlin(0,1,0,3.95);
	var xff_agc = min(3.0, xfilter_res.linexp(0,1,1,3));
	var xfilter_out = MoogFF.ar(xsig,xff_freq,xff_gain)*xff_agc*xamp*amp*cenv;
	// yFilter
	var yff_freq = (yfilter_freq +
		(freq*yfilter_track) +
		(aenv*yfilter_freq_benv) +
		(cenv*yfilter_freq_cenv) +
		(alfo*yfilter_freq_blfo) +
		(vlfo*yfilter_freq_vlfo)).max(50).min(16000);
	var yff_gain = yfilter_res.linlin(0,1,0,3.95);
	var yff_agc = min(3.0, yfilter_res.linexp(0,1,1,3));
	var yfilter_out = MoogFF.ar(ysig,yff_freq,yff_gain)*yff_agc*yamp*amp*cenv;
	LocalOut.ar([opa_sig,opb_sig]);
	Out.ar(outbus,yfilter_out+xfilter_out);
	Out.ar(xout,xfilter_out);
	Out.ar(yout,yfilter_out);
}).load)