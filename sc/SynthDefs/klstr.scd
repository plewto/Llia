

(
SynthDef(\Klstr, {|freq = 440,
	detune = 1.0,
	gate = 1,
	outbus = 0,
	xbus = 1024,     // external control bus
	doneAction = 2,
	amp = 0.1,
	lfoFreq = 1.0,
	lfo2FreqRatio  = 1.0,
	lfoXMod = 0,  // LFO1 -> LFO2.freq
	lfoDelay = 0.0,
	lfoDepth = 0.0,
	vibrato = 0.0,
	attack = 0.00,
	decay = 0.10,
	sustain = 1.00,
	release = 1.00,
	envMode = 0,   // 0 = gatted ADSR,  1 = ADR trigger
	pw = 0.5,
	pwLfo = 0.0,
	spread = 0.0,  // pulse frequency spred (0,1)
	spreadLfo = 0.0,
	spreadEnv = 0.0,
	cluster = 1.0, // cluster component mix (0,1)
	clusterLfo = 0.0, // 0..16
	clusterEnv = 0.0, // 0..16
	clusterLag = 0.0, // norm 0..1
	filterMix = 0.0, // 0 = bypass, 1 = bandpass
	filterFreq = 100, // Hz
	filterLfo = 0, // Hz
	filterEnv = 7000, // Hz
	filterLag = 0.0,   // norm 0..1
	res = 0.5,         // norm 0..1
	noiseAmp = 0.0,
	xScale = 1.0,
	xBias = 0.0,
	xToSpread = 0.0,  // norm 0..1
	xToNoise = 0.00,
	xToFilter = 0.00|   // norm 0..01
	var x = (In.kr(xbus) * xScale) + xBias;
	var lfoEnv = EnvGen.kr(Env([0.0, 0.001, 1.0, 1.0],[lfoDelay, lfoDelay, release],\linear,2),gate, doneAction: 0);
	var lfoAmp = (lfoEnv + lfoDepth).clip(0, 1);
	var lfo1 = LFCub.kr(lfoFreq,0,lfoAmp);
	var lfo2 = LFCub.kr(lfo2FreqRatio*lfoFreq + (lfo1*lfoXMod).clip(0.001,1000)   ,0,lfoAmp);
	var lfo = (lfo1+lfo2)*0.5;
	var holdtime = (attack+decay+release).max(0.01);
	var trig = Trig.kr(gate, holdtime);
	var envADSR = EnvGen.kr(Env.adsr(attack,decay,sustain,release,1,\linear,0),gate, doneAction: doneAction);
	var envASR = EnvGen.kr(Env([0.0, 1.0, sustain, 0.0, 0.0],[attack, decay, release, 0.01], \linear,4), trig, doneAction: 0);
	var envLin = XFade2.kr(envADSR, envASR, envMode.linlin(0,1,-1,1));
	var env = envLin * envLin;
	//var noise = WhiteNoise.ar() * (noiseAmp * (1 + (xToNoise * x)));
	var noise = WhiteNoise.ar() * (2 * (noiseAmp + (xToNoise * x))).max(0).min(2);
	var pWidth = pw + (lfo*pwLfo.linlin(0,1,0,0.49));
	var fspread = (spread + (lfo * spreadLfo.linlin(0,1,0,0.25)) + (envLin * spreadEnv) + (xToSpread * x));
	var r1 = 1.000;
	var r2 = 0.20 * fspread + 1;
	var r3 = 0.50 * fspread + 1;
	var r4 = fspread + 1;
	var r5 = 1.50 * fspread + 1;
	var r6 = 2.00 * fspread + 1;
	var f = freq*detune*(vibrato*lfo+1);
	var fArray = [r1,r2,r3,r4,r5,r6]*f;
	var rho = Lag2.kr((cluster + (lfo * clusterLfo) + (envLin * clusterEnv))*pi, clusterLag.linlin(0,1,0,4));
	var a1 = cos(rho)*1/2;
	var a2 = sin(rho)*1/2;
	var a3 = sin(rho*1.1)*1/2;
	var a4 = sin(rho*1.2)*1/2;
	var a5 = sin(rho*1.3)*1/2;
	var a6 = sin(rho*1.4)*1/2;
	var aArray = [a1,a2,a3,a4,a5,a6];
	var pulseSig = Mix.ar(Pulse.ar(fArray,pWidth,aArray));
	var rq = res.linexp(0.0, 1.0, 1.0, 0.06);
	var xFilter = (xToFilter.linexp(0, 1, 1, 16000) * x);
	var ffreq = Lag2.kr((filterFreq + (lfo * filterLfo) + (env * filterEnv) + xFilter),filterLag.linlin(0,1,0,2)).clip(100,16000);
	var bpf = BPF.ar(pulseSig+noise, ffreq, rq);
	var filterOut = XFade2.ar(pulseSig, bpf*4, filterMix.linlin(0, 1, -1, 1));
	Out.ar(outbus, filterOut*amp*env);
}).load
)

