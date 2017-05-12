/*
** SS2 (Simple Synth 2) is an extreamly simple, bare bones, instrument.
**
** Single multi-wave osscillator: tri, pulse, saw.
** Pulse width is variable.
**
** Single multi-mode non-resonant filter: bypass, lowpass, highpass.
** Filter frequency alwyas tracks keyboard by some factor.
**
** Dual envelope modes: ADSR, percussive.
** Envelope is only applied to main amplitude.
**
*/

(SynthDef (\SS2, {
    |
	outbus = 0             // primary audio output bus
	gate = 1               // envelope gate normalized high
	doneAction = 2         // doneAction determined by key mode
	freq = 440             // primary frequency
	detune = 1             // MIDI pitch bend ratio
	pw = 0.5               // Pulse width 0.06 0.12 0.25 0.50
	wave = 0               // Wave select 0=tri, 1=pulse, 2=saw
	track = 16             // Filter track 1,2,3,...,64
	filter = 0             // Filter select 0=bypass, 1=lowpass, 2=highpass
	envSelect = 0          // Enevelope select 0=ADSR, 1=Percussive
	attack = 0.0           //
	decay = 0.0            //
	sustain = 1.0          //
	release = 0.1          // Combined ADSR/Percusssive
	amp = 0.1              // 0..2
	|
	var aenv = EnvGen.kr(Env.adsr(attack,decay,sustain,release),gate,1,0,1,doneAction);
	var penv = EnvGen.kr(Env.perc(0.01,release),gate);
	var env = Select.kr(envSelect, [aenv,penv]);
	var f0 = freq*detune;
	var plsig = Pulse.ar(f0,pw);
	var swsig = Saw.ar(f0);
	var trsig = LeakDC.ar(LPF.ar(abs(swsig),(f0*6).min(16000)))*3;
	var fin = Select.ar(wave,[trsig,plsig,swsig]);
	var ffreq = (f0*track).max(f0).min(16000);
	var lp = LPF.ar(fin,ffreq);
	var hp = HPF.ar(fin,ffreq);
	var fout = Select.ar(filter,[fin,lp,hp]);
	Out.ar(outbus,fout*env*amp);
}).load)


