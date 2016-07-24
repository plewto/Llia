/*
* An extended Risset Drum
*/

(
SynthDef(\RDrum, {
	|freq = 110,
	detune = 1.0,
	gate = 1,
	outbus = 0,
	doneAction = 2,
	amp = 0.1,
	aRatio = 1.000,
	aAttack = 0.001,
	aDecay = 0.7500,
	aAmp = 1.000,
	aBend = 0.000,
	aTone = 0.000,  // 0 Sine,  +1 Square
	bRatio = 1.000,
	bAttack = 0.001,
	bDecay = 0.50,
	bAmp = 0.750,
	bBend = 0.000,
	bTune = 1.0,    // 0 = ~Unison, 1 = Risset   >1 -> other
	noiseRatio = 1.000,
	noiseBias = 0,
	noiseAttack = 0.001,
	noiseDecay = 0.500,
	noiseAmp = 0.000,
	noiseRes = 0,
	noiseBend = 0.00|
	var envA = EnvGen.kr(Env.perc(aAttack, aDecay),gate, doneAction: 0);
	var envB = EnvGen.kr(Env.perc(bAttack, bDecay), gate, doneAction: 0);
	var envNoise = EnvGen.kr(Env.perc(noiseAttack, noiseDecay), gate, doneAction: 0);
	var holdTime = max(aAttack, max(bAttack,noiseAttack)) + max(aDecay, max(bDecay, noiseDecay));
	var voiceHoldEnv = EnvGen.kr(Env.perc(0, holdTime), gate, doneAction: doneAction);
	var f = freq*detune;
	var aFreq = (f*aRatio * (envA * aBend + 1)).abs;
	var aSine = SinOsc.ar(aFreq, pi/4, envA*aAmp);
	var aSquare = Pulse.ar(aFreq, pi/4, envA*aAmp);
	var aSig = XFade2.ar(aSine, aSquare, aTone.linlin(0, 1, -1, -0.7));
	var bFreq = (f*bRatio * (envB * bBend + 1)).abs;
	var br1 = 1;
	var br2 = 0.599*bTune + 1.001;
	var br3 = 1.198*bTune + 1.002;
	var br4 = 1.297*bTune + 1.003;
	var bSig = Mix.ar(SinOsc.ar([br1, br2, br3, br4]*bFreq, pi/4, envB*bAmp/4));
	var nFreq = ((f*noiseRatio+noiseBias) * (envNoise * noiseBend + 1)).clip(30, 16000);
	var nRq = noiseRes.linexp(0, 1, 1, 0.05);
	var nSig = BPF.ar(WhiteNoise.ar(), nFreq, nRq)*envNoise*noiseAmp;
	Out.ar(outbus, (aSig+bSig+nSig)*amp);
}).load
)


