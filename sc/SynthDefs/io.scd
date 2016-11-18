/*
** Io Synth, FM Produced formants.
*/

(SynthDef (\Io,
	{|outbus = 0
		freq = 440
		amp = 0.07
		gate = 0
		detune = 1.0
		doneAction = 2
		velocity = 0.5
		port = 0.0
		/* Vibrato and Tremolo */
		vfreq = 7.0
		vdelay = 0.0
		vsens = 0.1     // norm 0..1
		vdepth = 0.1    // norm 0..1
		vlock = 0       // 0 -> Off, 1 -> lock vfreq to sub harmonic of freq
		trem = 0.1      // tremolo & mod depth
		/* Noise and Chiff */
		chiffAttack = 0.03
		chiffDecay = 0.2
		chiffAmp = 0.05
		chiffVelocity = 0.0    // velocity -> chiff amp
		noiseAmp = 1.0
		envScale = 1.1
		attack = 0.05
		decay = 0.2        // modulator only
		release = 0.1
		modDepth = 1.0
		feedback = 0.0
		modHP = 30
		velocityDepth = 0.5
		ff1 = 600             // formant frequencies
		ff2 = 1100
		ff3 = 2300
		amp1 = 1.0            // formant amplitudes
		amp2 = 1.0
		amp3 = 1.0
		lag1 = 0.0            // formants envelope lag times
		lag2 = 0.0
		lag3 = 0.0|
		var f0 = (Lag2.kr(freq,port)*detune);
		/* LFOs */
		var vEnv = EnvGen.kr(Env([0,0,1,1],[vdelay,vdelay,release],\lin,2),gate);
		var vf = Select.kr(vlock,[vfreq,freq/((freq/vfreq).round)]);
		var lfo1 = (PinkNoise.kr(0.06)+LFCub.kr(vf))*vsens.linlin(0,1,0,0.1)*vEnv*vdepth;
		var lfo2 = (LFCub.kr(vf,1.667,vEnv*(1+trem))+1*0.5);                                     // tremolo
		/* Chiff and Noise */
		var noiseHP = 10;
		var noiseRq = 0.1;
		var noiseRatios = [1.0, 1.5, 2.0, 3.0, 4.0, 6.0];
		var rawNoise = Mix.ar(BPF.ar(HPF.ar(WhiteNoise.ar(),noiseHP),noiseRatios*freq,noiseRq));
		var chiffAttackScale = BrownNoise.kr().abs*1.5;   // random scale chiff attack time
		var chiffComp = 0.3;
		var chiffEnv = EnvGen.kr(Env.adsr(chiffAttack*chiffAttackScale,chiffDecay,0,0),gate);
		var chiffSig = chiffComp*rawNoise*chiffEnv*chiffAmp*LinXFade2.kr(1,velocity, chiffVelocity.linlin(0,1,-1,1));
		var noiseEnv = EnvGen.kr(Env.asr(attack*0.9,1,release*1.1),gate);
		var noiseComp = 0.3;
		var noiseSig = rawNoise*noiseEnv*noiseComp*noiseAmp*LinXFade2.kr(1,lfo2,trem.linlin(0,1,-1,1));
		/* modulator */
		var vel = LinXFade2.kr(1,velocity,velocityDepth.linlin(0,1,-1,1));
		var modFreq = f0*(1+lfo1);
		//var modEnv = EnvGen.kr(Env.adsr(attack*1.1,chiffDecay*1.1,0.75,release*0.9),gate);
		var espread = [1,envScale,envScale*envScale];
		var modEnv = EnvGen.kr(Env.adsr(espread*attack,espread*decay,0.5,espread*release),gate);
		var modAmp = modDepth*vel*LinXFade2.kr(1,lfo2,trem.linlin(0,1,-1,0));
		var modSig = modEnv*HPF.ar(SinOscFB.ar(modFreq,feedback,modAmp),modHP);
		/* Carriers */
		var carEnv = EnvGen.kr(Env.asr(attack,1,release),gate, doneAction: doneAction);
		var cfreq = [ff1/f0,ff2/f0,ff3/f0].floor*freq*(1+lfo1);  // carrier frequencies
		var camp = [amp1,amp2,amp3]*Lag2.kr(carEnv,[lag1,lag2,lag3])*vel*LinXFade2.kr(1,lfo2,trem.linlin(0,1,-1,0));
		var csig = Mix.ar(SinOsc.ar(cfreq + (modSig*cfreq),0,camp))*0.333;
		Out.ar(outbus,(csig+chiffSig+noiseSig)*amp);
}).load
)
