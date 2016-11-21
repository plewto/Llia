/*
** Simple Synth 1
**    Osc -> Filter -> Amp
**    LFO ADSR
*/

(SynthDef (\SS1, {
	|outbus = 0
	xbus = 1024
	gate = 1
	doneAction = 2
	freq = 440
	port = 0.0
	detune = 1.0
	vsens = 0.1	          // vibrato sensitivity
	vdepth = 0.0	      // programmed vibrato depth
	xPitch = 0.0	      // external signal -> pitch
	chorus = 0            // 0 -> off   1 -> on (only applied when combining saw and pulse signals)
	lfoFreq = 7.0
	lfoWave = 0           // 0 -> sine   1 -> pulse     2 -> sample & hold
	lfoDelay = 0.0
	lfoAmp = 0.0
	attack = 0.0
	decay = 0.1
	sustain = 1.0
	release = 0.1
	sawMix = 0.0,
	pulseMix = 0.5,
	subOctave = 0         // 0 -> 1 octave   1 -> 2 octaves
	subMix = 0.0,
	noiseSelect = 0       // 0 -> white   1 -> pink  (effects audio and Snh LFO)
	noiseMix = 0.0,
	wave = 0.5,           // osc wave 0..1
	waveLFO = 0.0  	      // LFO -> wave
	waveEnv = 0.0	      // env -> wave
	highPass = 10	      // static highpass cutoff in Hz
	filterFreq = 10000    // LP filter cutoff in Hz
	filterTrack = 0	      // freq -> filter (0,1,2,4)
	filterLFO = 0	      // LFO -> filter  (0...10k)
	filterEnv = 0	      // env -> filter  (-10k...10k)
	xFilter = 0	          // external -> filter (-10k ... 10k)
	filterRes = 0.0       // filter resonance (0..1)
	gateMode = 0	      // VCA 0 -> env   1 -> gate
	amp = 0.3|
	var x = In.kr(xbus);
	var env = EnvGen.kr(Env.adsr(attack,decay,sustain,release),gate, doneAction: doneAction);
	var lfoEnv = EnvGen.kr(Env([0,0,1,1],[lfoDelay,lfoDelay,release],\lin,3),gate);
	var noise = Select.ar(noiseSelect, [WhiteNoise.ar(),PinkNoise.ar()*3]);
	var lfoSine = LFCub.kr(lfoFreq);
	var lfoPulse = Pulse.kr(lfoFreq);
	var lfoSH = Latch.kr(noise,lfoPulse)*3;
	var lfo = Select.kr(lfoWave,[lfoSine,lfoPulse,lfoSH]) * (lfoAmp + lfoEnv);
	var vibsig = (1 + ((lfo * vsens.linlin(0,1,0,0.1)) * ((xPitch  * x) + vdepth)));
	var f0 = Lag2.kr(freq,port)*detune;
	var width = (wave + (lfo*waveLFO*0.5) + (env*waveEnv)).min(0.95).max(0.05);
	var saw = VarSaw.ar(f0*vibsig,0,width);
	var pFreq1 = Select.kr(chorus, [f0, f0*1.003])*vibsig;
	var pulse = Pulse.ar(pFreq1,width);
	var pFreq2 = (f0*subOctave.linlin(0,1,0.5,0.25))*vibsig;
	var sub = Pulse.ar(pFreq2,0.5);
	var lpIn = HPF.ar((saw*sawMix) + (pulse*pulseMix) + (sub*subMix) + (noise*noiseMix),highPass);
	var lpCutoff = (filterFreq + (lfo*filterLFO) + (env*filterEnv) + (x*xFilter) + (f0*filterTrack)).max(50).min(16000);
	var lpRq = filterRes.linexp(0,1,1,0.05);
	var lpOut = RLPF.ar(lpIn,lpCutoff,lpRq);
	var vca = Select.kr(gateMode, [env,gate]);
	Out.ar(outbus,lpOut*vca*amp);
}).load)


