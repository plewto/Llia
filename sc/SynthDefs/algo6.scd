/*
 * Basic FM Synth loosly based onYamaha DX7 Algorithm 6
 *
 *   [m1]-->[c1]---+
 *                 |
 *   [m2]-->[c2]---+---> out
 *                 |
 *   [m3]-->[c3]---+
 *
 * Features and omissions:
 *  -2) No pitch envelope.
 *  -1) Single ADSR envelope shared by each modulator/carrier pair.
 *  +1) Lag processor on modulator envelope.
 *  +2) External control bus input for vibrato/pitch env and modulator depths.
 *  +3) Frequency bias parameter for each modulator.
 *  +4) Envelope to feedback depth.
*/
(
SynthDef(\Algo6, {|freq = 440,
	keynumber = 69,
	detune = 1.0,
	gate = 1,
	doneAction = 2,
	amp = 0.1,
	port = 0.0,
	outbus = 0,
	aBus = 1024,
	aToFreq = 0,
	brightness = 1.0,
	vfreq = 4.0,
	vdelay = 0.0,
	vsens = 0.1,
	vdepth = 0.0,
	vibrato = 0.0,
	// ------ Sig1
	c1 = 1.0,
	c1Enable = 1.0, // mute flag  0=mute, 1=unmute
	c1Mix = 1.0,
	m1 = 1.0,
	m1Bias = 0,
	aToMod1 = 0.0,
	modDepth1 = 0.5,
	envToMod1 = 1.0,
	envMod1Lag = 0.0,
	m1Enable = 1.0,
	attack1 = 0.0,
	decay1 = 0.0,
	sustain1 = 1.0,
	release1 = 0.0,
	keyBreak1 = 60, // MIDI key number
	c1LowKeyScale = 0,  // db per octave
	c1HighKeyScale = 0,
	m1LowKeyScale = 0,
	m1HighKeyScale = 0,
	// ------ Sig2
	c2 = 1.0,
	c2Enable = 1.0, // mute flag  0=mute, 1=unmute
	c2Mix = 1.0,
	m2 = 1.0,
	m2Bias = 0,
	aToMod2 = 0.0,
	modDepth2 = 0.5,
	envToMod2 = 1.0,
	envMod2Lag = 0.0,
	m2Enable = 1.0,
	attack2 = 0.0,
	decay2 = 0.0,
	sustain2 = 1.0,
	release2 = 0.0,
	keyBreak2 = 60, // MIDI key number
	c2LowKeyScale = 0,  // db per octave
	c2HighKeyScale = 0,
	m2LowKeyScale = 0,
	m2HighKeyScale = 0,
	// ------ Sig3
	fb3 = 0,
	envToFb3 = 0,
	c3 = 1.0,
	c3Enable = 1.0, // mute flag  0=mute, 1=unmute
	c3Mix = 1.0,
	m3 = 1.0,
	m3Bias = 0,
	aToMod3 = 0.0,
	modDepth3 = 0.5,
	envToMod3 = 1.0,
	envMod3Lag = 0.0,
	m3Enable = 1.0,
	attack3 = 0.0,
	decay3 = 0.0,
	sustain3 = 1.0,
	release3 = 0.0,
	keyBreak3 = 60, // MIDI key number
	c3LowKeyScale = 0,  // db per octave
	c3HighKeyScale = 0,
	m3LowKeyScale = 0,
	m3HighKeyScale = 0|
	var a = In.kr(aBus, 1);
	var b = brightness.linlin(0,1,0,4);
	var maxRelease = [release1+release2+release3].max;
	var vibEnv = EnvGen.kr(Env([0.001, 0.001, 1.0, 1.0],[vdelay, vdelay, maxRelease*2], \linear, 2), gate, doneAction: 0);
	var vibAmp = (vibrato + (vibEnv*vdepth))*vsens;
	var vibSig = LFCub.kr(vfreq, 0, vibAmp)+1;
	var aFreqMod = XFade2.kr(1,a, aToFreq.linlin(0,1,-1,1));
	var f0 = Lag2.kr(freq, port) * detune * aFreqMod * vibSig;
	var env1Lin = EnvGen.kr(Env.adsr(attack1, decay1, sustain1, release1, curve: \linear), gate, 1, 0, 1, 0);
	var env2Lin = EnvGen.kr(Env.adsr(attack2, decay2, sustain2, release2, curve: \linear), gate, 1, 0, 1, 0);
	var env3Lin = EnvGen.kr(Env.adsr(attack3, decay3, sustain3, release3, curve: \linear), gate, 1, 0, 1, 0);
	var env1 = env1Lin * env1Lin;
	var env2 = env2Lin * env2Lin;
	var env3 = env3Lin * env3Lin;
	var envHold = EnvGen.kr(Env.adsr(0,0,1,maxRelease),gate, 1, 0, 1, doneAction);
	// Sig 1
	var octaveDiff1 = (keynumber-keyBreak1)/12;
	var c1LowScale = c1LowKeyScale * octaveDiff1.min(0).abs;
	var c1HighScale = c1HighKeyScale * octaveDiff1.max(0);
	var c1Scale = dbamp(c1LowScale + c1HighScale);
	var m1LowScale = m1LowKeyScale * octaveDiff1.min(0).abs;
	var m1HighScale = m1HighKeyScale * octaveDiff1.max(0);
	var m1Scale = dbamp(m1LowScale + m1HighScale);
	var c1Freq = f0*c1;
	var m1Freq = f0*m1+m1Bias;
	var aMod1 = XFade2.kr(1, a, aToMod1.linlin(0,1,-1,1));
	var m1Env = XFade2.kr(1, Lag2.kr(env1Lin, envMod1Lag.linlin(0,1,0,3)), envToMod1.linlin(0,1,-1,1));
	var m1Amp = c1Freq * aMod1 * b * (modDepth1.linexp(0, 1, 0.1, 8)-0.1).max(0) * m1Env * m1Enable * m1Scale;
	var m1Sig = SinOsc.ar(m1Freq,0,m1Amp);
	var c1Amp = c1Mix * env1 * c1Scale * c1Enable;
	var c1Sig = SinOsc.ar(c1Freq+m1Sig, 0, c1Amp);
	// Sig 2
	var octaveDiff2 = (keynumber-keyBreak2)/12;
	var c2LowScale = c2LowKeyScale * octaveDiff2.min(0).abs;
	var c2HighScale = c2HighKeyScale * octaveDiff2.max(0);
	var c2Scale = dbamp(c2LowScale + c2HighScale);
	var m2LowScale = m2LowKeyScale * octaveDiff2.min(0).abs;
	var m2HighScale = m2HighKeyScale * octaveDiff2.max(0);
	var m2Scale = dbamp(m2LowScale + m2HighScale);
	var c2Freq = f0*c2;
	var m2Freq = f0*m2+m2Bias;
	var aMod2 = XFade2.kr(1, a, aToMod2.linlin(0,1,-1,1));
	var m2Env = XFade2.kr(1, Lag2.kr(env2Lin, envMod2Lag.linlin(0,1,0,3)), envToMod2.linlin(0,1,-1,1));
	var m2Amp = c2Freq * aMod2 * b * (modDepth2.linexp(0, 1, 0.1, 8)-0.1).max(0) * m2Env * m2Enable * m2Scale;
	var m2Sig = SinOsc.ar(m2Freq,0,m2Amp);
	var c2Amp = c2Mix * env2 * c2Scale * c2Enable;
	var c2Sig = SinOsc.ar(c2Freq+m2Sig, 0, c2Amp);
	// Sig 3
	var octaveDiff3 = (keynumber-keyBreak2)/12;
	var c3LowScale = c3LowKeyScale * octaveDiff3.min(0).abs;
	var c3HighScale = c3HighKeyScale * octaveDiff3.max(0);
	var c3Scale = dbamp(c3LowScale + c3HighScale);
	var m3LowScale = m3LowKeyScale * octaveDiff3.min(0).abs;
	var m3HighScale = m3HighKeyScale * octaveDiff3.max(0);
	var m3Scale = dbamp(m3LowScale + m3HighScale);
	var c3Freq = f0*c3;
	var m3Freq = f0*m3+m3Bias;
	var aMod3 = XFade2.kr(1, a, aToMod3.linlin(0,1,-1,1));
	var m3Env = XFade2.kr(1, Lag2.kr(env3Lin, envMod3Lag.linlin(0,1,0,3)), envToMod3.linlin(0,1,-1,1));
	var m3Amp = c3Freq * aMod3 * b * (modDepth2.linexp(0, 1, 0.1, 8)-0.1).max(0) * m3Env * m3Enable * m3Scale;
	var mod3Feedback = fb3 * (env3Lin * envToFb3 + 1);
	var m3Sig = SinOscFB.ar(m3Freq, mod3Feedback, m3Amp);
	var c3Amp = c3Mix * env3 * c3Scale * c3Enable;
	var c3Sig = SinOsc.ar(c3Freq+m3Sig, c3Amp);
	var outsig = Mix.ar(c1Sig+c2Sig+c3Sig)*amp;
	Out.ar(0, outsig);
}).load
)


