/*
** Combo Organ
*/

(SynthDef (\Combo, {
    |outbus = 0             // primary audio output bus
     gate = 1               // envelope gate normalized high
     doneAction = 2         // doneAction determined by key mode
     freq = 440             // primary frequency
     detune = 1             // MIDI pitch bend ratio
	 flute8 = 1             //  8' <--> 2:1    0..1 --> (0,0.5,1)
     flute4 = 0             //  4' <--> 4:1
     flute3 = 0             //  3' <--> 3:1
     flute2 = 0             //  2' <--> 8:1
     reed16 = 1             // 16' <--> 1:1
     reed8 = 0              //  8' <--> 2:1
	 reedWave = 0           // pulse width 0=0.333 1=0.5
     vspeed = 0             //  0..1  --> 3..7
     vdepth = 0             //  0..1  --> 0..0.05
     chorus = 0             //  0..1  --> 0..5      // Frequency offset
     amp = 0.3|
	var vfreq = vspeed.linlin(0,1,3,7);
	var vamp = vdepth.linlin(0,1,0,0.007);
	var lfo = LFCub.kr(vfreq,0,vamp);
	var f0 = (freq*detune)*(1+lfo);
	var fluteFreq = f0*[2,4,3,8];
	var fluteAmps = [flute8,flute4*0.5,flute3*0.5,flute2*0.35];
	var fluteSig = Mix.ar(SinOsc.ar(fluteFreq,0,fluteAmps));
	var maxChorusBeat = 1.5;
	var chorusBeat = chorus.linlin(0,1,0,maxChorusBeat);
	var reedFreq = [f0-chorusBeat, (f0*2)+chorusBeat];
	var reedAmps = [reed16,reed8];
	var reedFilterCutoff = (freq*12).min(16000);
	var reedPw = reedWave.linlin(0,1,0.20, 0.51);
	var reedSig = LPF.ar(Mix.ar(Pulse.ar(reedFreq,reedPw,reedAmps)),reedFilterCutoff);
	var env = EnvGen.kr(Env.asr(0.001, 1.0,0.001),gate,amp*0.5,0,1,doneAction);
	var outsig = (fluteSig+reedSig)*env;
	var famp = Lag2.kr(Amplitude.kr(fluteSig));
	var ramp = Lag2.kr(Amplitude.kr(reedSig));
	Out.ar(outbus,outsig);
}).load)
