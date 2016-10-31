/*
** Defines QMod synth
*/

(SynthDef (\QMod,{
	|inbus = 128
	outbus = 0
	gate = 1
	freq = 440           // last key frequency
	keyTrack = 0
	fixedFrequency = 1.0
	inputFilter = 5000        // Hz
	inputGain = 1             // Should have very wide range (1,10,100,...?)
	modDepth = 1.0            // 0..1
	attack = 0.01             // Common to envelope follower
	release = 0.01            // and internal ASR envelope
	envelopeSelect = 0        // 0 -> envelope follower, 1 -> ASR
	wetAmp = 1.0
	dryAmp = 1.0|
	var dry = In.ar(inbus,1);
	var fm1 = LPF.ar(dry,inputFilter)*inputGain*modDepth;
	var fm2 = freq*keyTrack;
	var f = (fm1+fm2+fixedFrequency).abs.min(20000);
	var oscout = HPF.ar(SinOsc.ar(f),30);
	var env1 = Lag.kr(Amplitude.kr(dry,attack,release), 0.05);
	var env2 = EnvGen.kr(Env.adsr(attack,0,1,release),gate, doneAction: 0);
	var env = Select.kr(envelopeSelect, [env1,env2]);
	var wetsig = oscout*env*wetAmp;
	var drysig = dry*dryAmp;
    Out.ar(outbus,wetsig+drysig);
}).load)