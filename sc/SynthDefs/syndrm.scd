/*
** syndrm 
**
** Multi timbarl synthetic percussion instruments:
**    hh    - (Cough) a Hi Hat using filterd tone clustes. 
**    cym   - (Cough Again) a cymbal using a different set of clusters.
**    clave - Dammed sine wave.
**    drum1 - Dammed sine wacve with "click"
**    rdrum - Risset Drum.
**    noise - Dammed filterd noise.
**
** Each instrument has a key range over which it responds.
**
** Parameters:
**
** gate      - 0|1
** amp       - Overall amplitude
** keynumber - MIDI key number
**
** **************************************************************************
** The "Hi Hat" is produced by band pass filtering a cluster of 5 pulse waves.
** The frequency of the pulse waves are realtivly prime.
**
** hhFreq    - hi hat frequency, Hz
** hhAmp     -
** hhAttack  - 
** hhDecay1  -
** hhDecay2  -
** hhRandom  - 0,1.  Randomly change one component
** hhFilter  - Hi hat band pass filter, center frequency, Hz
** hhLowKey  - MIDI key range.  Region excluded both end points.
** hhHighKey - 
** hhOutbus  - 0
**
** ****************************************************************************
** The "Cymbal" is almost identical to the Hi Hat with the exceptin that 
** the filter frequency may be modulated by the envelope.
**
** cymFreq        - Hz
** cymAmp         -
** cymAttack      -
** cymDecay1      -
** cymDecay2      -
** cymRandom      -
** cymFilter      -
** cymFilterRq    -
** cymEnvToFilter - Hz, may be inverted.
** cymLowKey      -
** cymHighKey     -
** cymOutbus      - 
**
** ****************************************************************************
** The clave is a dammep sine wave
**
** claveFreq
** claveAmp
** claveLowKey
** claveHighKey
** claveOutbus
**
** ****************************************************************************
** Drum1 is a dammep sine wave with a "click" component.  The main sine wave
** frequency may be modulated by the envelope.
**
** drum1Freq
** drum1Amp
** drum1Click
** drum1Attack
** drum1Decay1
** drum1Decay2
** drum1Bend
** drum1LowKey
** drum1HighKey
** drum1Outbus
**
** ****************************************************************************
** RDrum is a Risset Drum
**
** rdrumFreq
** rdrumAttack
** rdrumDecay1
** rdrumDecay2
** rdrumAmp
** rdrumLowKey
** rdrumHighKey
** rdrumOutbus
**
** ****************************************************************************
** Noise is bandpass filterd whiotre noise with percussive decay.
** The filter may be modulated by the envelope.
**
** noiseFreq
** noiseAmp
** noiseAttack
** noiseDecay
** noiseEnvToFreq
** noiseRq
** noiseLowKey
** noiseHighKey
** noiseOutbus
*/

(SynthDef (\SynDrm,
	{|gate = 1,
		amp = 0.05,
		keynumber = 69,
		// High Hat
		hhFreq = 220,
		hhAmp = 1.0,
		hhAttack = 0.0,
		hhDecay1 = 0.01,
		hhDecay2 = 0.01,
		hhRandom = 0.1,
		hhFilter = 9000,
		hhLowKey = 0,
		hhHighKey = 10,
		hhOutbus = 0
		// Cymbal
		cymFreq = 220,
		cymAmp = 1.0,
		cymAttack = 0.0,
		cymDecay1 = 0.01,
		cymDecay2 = 5.00,
		cymRandom = 1.0,
		cymFilter = 1000,
		cymFilterRq = 0.5,
		cymEnvToFilter = 8000,
		cymLowKey = 10,
		cymHighKey = 20,
		cymOutbus = 0,
		// Clave
		claveFreq = 1760,
		claveAmp = 0.5,
		claveLowKey = 20,
		claveHighKey = 30,
		claveOutbus = 0
		// Drum 1
		drum1Freq = 110,
		drum1Amp = 1.0,
		drum1Click = 0.33,
		drum1Attack = 0.001,
		drum1Decay1 = 0.001,
		drum1Decay2 = 1.0,
		drum1Bend = 0.01,
		drum1LowKey = 30,
		drum1HighKey = 40,
		drum1Outbus = 0
		// rdrum
		rdrumFreq = 110,
		rdrumAttack = 0.001,
		rdrumDecay1 = 0.001,
		rdrumDecay2 = 2.0,
		rdrumAmp = 1.0,
		rdrumLowKey = 40,
		rdrumHighKey = 50,
		rdrumOutbus = 0,
		// noise
		noiseFreq = 1000,
		noiseAmp = 1.0,
		noiseAttack = 0.01,
		noiseDecay = 0.2,
		noiseEnvToFreq = 0,
		noiseRq = 0.5,
		noiseLowKey = 60,
		noiseHighKey = 70,
		noiseOutbus = 0|
		var eq12 = 2**(1/12.0);
		// hh
		var hhGate = ((keynumber-hhLowKey).clip(0,1)) * ((hhHighKey-keynumber).clip(0,1)) * gate;
		var hhEnv = EnvGen.kr(Env([0.001, 1.00, 0.70, 0.001],[hhAttack, hhDecay1, hhDecay2],\exp,3),hhGate);
		var hhRnd = 1.194+LPF.kr(BrownNoise.kr()*hhRandom, 1.0);
		var hhKeyOffset = (keynumber-hhLowKey).abs.clip(0, 35);
		var hhKeyFreq = eq12**hhKeyOffset;
		var hhFreqArray = [1, hhRnd, 1.323, 1.387, 1.516]*(hhFreq*hhKeyFreq);
		var hhPulse = Mix.ar(Pulse.ar(hhFreqArray,0.5))*hhEnv*hhAmp;
		var hh = BPF.ar(hhPulse, hhFilter,0.5);
		// cym
		var cymGate = ((keynumber-cymLowKey).clip(0,1)) * ((cymHighKey-keynumber).clip(0,1)) * gate;
		var cymEnv = EnvGen.kr(Env([0.001, 1.00, 0.70, 0.001],[cymAttack, cymDecay1, cymDecay2],\exp,3),cymGate);
		var cymRnd = 1.211+LPF.kr(BrownNoise.kr()*cymRandom, 1.0);
		var cymKeyOffset = (keynumber-cymLowKey).abs.clip(0, 35);
		var cymKeyFreq = eq12**cymKeyOffset;
		var cymFreqArray = [1, cymRnd, 1.526,1.631,2.631,1.947]*cymFreq*cymKeyFreq;
		var cymPulse = Mix.ar(Pulse.ar(cymFreqArray,0.5))*cymEnv*cymAmp;
		var cymFilterFreq = ((cymEnv*cymEnvToFilter)+cymFilter).clip(100,16000);
		var cym = BPF.ar(cymPulse, cymFilterFreq, cymFilterRq);
		// clave
		var claveGate = ((keynumber-claveLowKey).clip(0,1)) * ((claveHighKey-keynumber).clip(0,1)) * gate;
		var claveDecay = 0.04;
		var claveEnv =  EnvGen.kr(Env([0.000, 1.000, 0.000],[0.0, claveDecay], \lin, 2),claveGate);
		var claveKeyOffset = (keynumber-claveLowKey).abs.clip(0, 35);
		var claveKeyFreq = eq12**claveKeyOffset;
		var clave = SinOsc.ar(claveFreq*claveKeyFreq, pi/4)*claveEnv*claveAmp;
		// Drum 1
		var drum1Gate = ((keynumber-drum1LowKey).clip(0,1)) * ((drum1HighKey-keynumber).clip(0,1)) * gate;
		var drum1Env = EnvGen.kr(Env([0.001, 1.00, 0.70, 0.001],[drum1Attack, drum1Decay1, drum1Decay2],\exp,3),drum1Gate);
		var drum1ClickEnv = EnvGen.kr(Env([0.000, 1.00, 0.70, 0.000],[0.0, 0.003, 0.003], \lin,3), drum1Gate);
		var drum1ClickSig = LFPar.ar(1750,0.25)*drum1ClickEnv*(drum1Click.linlin(0,1,0,0.1));
		var drum1KeyOffset = (keynumber-drum1LowKey).abs.clip(0, 35);
		var drum1BendRatio = drum1Bend.linlin(0, 1, 1, 2);
		var drum1KeyFreq = eq12**drum1KeyOffset;
		var drum1Frequency = (drum1Freq*drum1KeyFreq)*drum1BendRatio;
		var drum1Tone = SinOsc.ar(drum1Frequency, pi/4)*drum1Env;
		var drum1 = (drum1Tone+drum1ClickSig)* drum1Amp;
		// RDrum
		var rdrumGate = ((keynumber-rdrumLowKey).clip(0,1)) * ((rdrumHighKey-keynumber).clip(0,1)) * gate;
		var rdrumEnv1 = EnvGen.kr(Env([0.001, 1.00, 0.70, 0.001],[rdrumAttack, rdrumDecay1, rdrumDecay2],\exp,3),rdrumGate);
		var rdrumEnv2 = EnvGen.kr(Env([0.001, 1.00, 0.70, 0.001],[rdrumAttack, rdrumDecay1, rdrumDecay2/2],\exp,3),rdrumGate);
		var rdrumKeyOffset = (keynumber-rdrumLowKey).abs.clip(0, 35);
		var rdrumKeyFreq = eq12**rdrumKeyOffset;
		var rdrumFrequency = rdrumFreq*rdrumKeyFreq;
		var rdrumTone1 = SinOsc.ar(rdrumFrequency, pi/4)*rdrumEnv1;
		var rdrumTone2 = Mix.ar(SinOsc.ar([1.6, 2.2, 2.3]*rdrumFrequency,pi/4, [1.0, 1.333, 1.0])) * rdrumEnv2*0.17;
		var rdrum = (rdrumTone1 + rdrumTone2) * rdrumAmp;
		// noise
		var nseGate = ((keynumber-noiseLowKey).clip(0,1)) * ((noiseHighKey-keynumber).clip(0,1)) * gate;
		var nseEnv = EnvGen.kr(Env([0.001, 1.00, 0.70, 0.001],[noiseAttack, 0.01, noiseDecay],\exp,3),nseGate);
		var nseKeyOffset = (keynumber-noiseLowKey).abs.clip(0, 35);
		var nseKeyFreq = eq12**nseKeyOffset;
		var nseFreq = ((noiseFreq*nseKeyFreq) + (noiseEnvToFreq.linlin(0,1,0,2*noiseFreq)*nseEnv)).clip(100, 12000);
		var nse = BPF.ar(WhiteNoise.ar(), nseFreq, noiseRq)*nseEnv*noiseAmp;
		Out.ar(hhOutbus, hh*amp);
		Out.ar(cymOutbus, cym*amp);
		Out.ar(claveOutbus, clave*amp);
		Out.ar(drum1Outbus, drum1*amp);
		Out.ar(rdrumOutbus, rdrum*amp);
		Out.ar(noiseOutbus, nse*amp);
}).load;
)

