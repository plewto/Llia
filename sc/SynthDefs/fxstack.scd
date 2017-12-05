/*
** Fxstack
** Effects Stack: --+-->[distortion]-->[filter]-->[flanger]-->[dual delay]-->[reverb]-->
**                  |
**                  +-->[env follow]
**                            [lfo1]
**                            [lfo2]
*/

(SynthDef (\Fxstack, {
	|outbus0 = 0
	outbus1 = 1
	inbus = 8
	inputGain = 1.0
	outputGain = 1.0
	// Envelope Follower
	envGain = 1.0   // 1..100?
	attack = 0.0    // 0..2
	release = 0.0   // 0..2
	// LFOs
	lfo1Freq = 1.0
	lfo2Freq = 1.0
	lfo2Mod = 0.0   // LFO1 mod of LFO2
	// Distortion & Tremolo
	clipDrive = 1.0
	clipLfo1 = 0.0
	clipMix = 0.0      // Asymetric shape above 0.5
	// Filter
	filterFreq = 0.5   // 0..1
	filterEnv = 0.0    // env -> filter
	filterLfo2 = 0.0
	filterRes = 0.0
	filterMix = 0.0
	// Flanger
	flangerDelay1 = 0.5    // 0..1
	flangerDelay2 = 0.6    // 0..1
	flangerLfo1 = 0.0      // 0..1
	flangerFeedback = 0.0
	flangerMix = 0.0
	// Delay 1
	delay1Time = 0.1
	delay1Lfo1 = 0.0
	delay1Feedback = 0.0
	delay1XFeedback = 0.0
	delay1Lowpass = 1.0
	delay1Mix = 0.0
	delay1Pan = -0.75
	// Delay 2
	delay2Time = 0.1
	delay2Lfo2 = 0.0
	delay2Feedback = 0.0
	delay2XFeedback = 0.0
	delay2Highpass = 0.0
	delay2Mix = 0.0
	delay2Pan = 0.75
	// Reverb
	reverbRoomSize = 0.5
	reverbDamping = 0.5
	reverbEnv = 0.0           // env -> reverb amp
	reverbLfo2 = 0.0          // lfo2 -> reverb amp
	reverbMix = 0.0|
	var minFilter = 200;       // Minimum filter cutoff
	var maxFilter = 20000;
	var insig = In.ar(inbus);

	// Envelope Follower
	var envTrig = insig.abs.min(0.25)*envGain;
	var env = Lag2.kr(Amplitude.kr(envTrig,attack,release),0.05);
	// var env=0;  // Env Bypass

	// LFOs
	var lfo1 = LFCub.kr(lfo1Freq);
	var lfo2Amp = LinXFade2.kr(1,lfo1,lfo2Mod.linlin(0,1,-1,1));
	var lfo2 = LFCub.kr(lfo2Freq,0,lfo2Amp);

	// Audio input & Clipper

	var dry = insig*inputGain;
	var clipGain = clipDrive.linexp(0,1,1,80).max(1);
	var clipA = (insig*clipGain);
	var clipB = (-1.2)*clipA;
	var clipC = (-1.0)*clipA;
	var clipAmp = LinXFade2.kr(1,lfo1,clipLfo1.linlin(0,1,-1,1));
	var clipIn = (((clipA.exp-clipB.exp)/(clipA.exp+clipC.exp))/clipGain).max(-50).min(50);
	var clipWet = Limiter.ar(clipIn,0.9,0.01)*clipAmp;
	var clipOut = XFade2.ar(dry,clipWet,clipMix.linlin(0,1,-1,1));
	//var clipOut = insig;   // ISSUE: Clipper Bypass

	// Feedback signals
	var fb = LocalIn.ar(2);
	var fb0 = fb[0];  // Delay 1
	var fb1 = fb[1];  // Delay 2

	// Filter
	var filterIn = clipOut;
	var filterMod = 1 + (env*filterEnv) + (lfo2*filterLfo2);
	var filterCutoff = (filterFreq.linexp(0,1,minFilter,maxFilter) * filterMod).min(maxFilter).max(minFilter);
	var res = filterRes.linlin(0,1,0,3.99);
	var filterWet = MoogFF.ar(filterIn,filterCutoff,res);
	var filterOut = XFade2.ar(filterIn,filterWet,filterMix.linlin(0,1,-1,1));
	// var filterOut = clipOut;   // ISSUE: Filter Bypass

	// Flanger
	var flangerIn = filterOut;
	var maxFlangerDelay = 0.001;
	var flangerMod1 = 1 + (lfo1*flangerLfo1);
	var flangerMod2 = DelayL.kr(flangerMod1,0.1, 0.1);
	var flangerDelayTime1 = (flangerDelay1.linlin(0,1,0,maxFlangerDelay)*flangerMod1).min(maxFlangerDelay);
	var flangerDecay = flangerFeedback.linlin(-1,1,-0.1,0.1);
	var flangerWet1 = CombC.ar(flangerIn,maxFlangerDelay,flangerDelayTime1,flangerDecay)+flangerIn;
	var flangerDelayTime2 = (flangerDelay2.linlin(0,1,0,maxFlangerDelay)*flangerMod2).min(maxFlangerDelay);
	var flangerWet2 = CombC.ar(flangerIn,maxFlangerDelay,flangerDelayTime2,flangerDecay);
	var flangerWet = (flangerWet1+flangerWet2)*0.5;
	var flangerOut = XFade2.ar(flangerIn,flangerWet,flangerMix.linlin(0,1,-1,1));
	// var flangerOut = filterOut;   // ISSUE: Flanger Bypass


	// Dealy1
	var maxDelay = 1.0;
	var dly1Mod = 1 + (lfo1*delay1Lfo1*0.01);
	var dly1Time = (delay1Time*dly1Mod).min(maxDelay).max(0);
	var dly1In = flangerOut+(fb0*delay1Feedback)+(0.5*fb1*delay1XFeedback);
	var dly1Wet = DelayC.ar(dly1In,maxDelay,dly1Time);
	var dly1Out = XFade2.ar(flangerOut,dly1Wet,delay1Mix.linlin(0,1,-1,1));
	// Delay2
	var dly2Mod = 1 + (lfo2*delay2Lfo2*0.01);
	var dly2Time = (delay2Time*dly2Mod).min(maxDelay).max(0);
	var dly2In = flangerOut+(fb1*delay2Feedback)+(0.5*fb0*delay2XFeedback);
	var dly2Wet = DelayC.ar(dly2In,maxDelay,dly2Time);
	var dly2Out = XFade2.ar(flangerOut,dly2Wet,delay2Mix.linlin(0,1,-1,1));
	// var dly1Out = flangerOut;    // ISSUE: Delay1 Bypass
	// var dly2Out = flangerOut;    // ISSUE: Delay2 Bypass

	// Reverb
	var reverbIn = Pan2.ar([dly1Out,dly2Out],[delay1Pan,delay2Pan]);
	var reverbMod = (1 + (env*reverbEnv) + (lfo2*reverbLfo2)).abs.min(1);
	var reverbWet = FreeVerb.ar(reverbIn,1.0,reverbRoomSize,reverbDamping)*reverbMod;
	var reverbOut = XFade2.ar(reverbIn,reverbWet,reverbMix.linlin(0,1,-1,1));
	// var reverbOut = dly1Out;     // ISSUE: Reverb Bypass

	// Feedback sends
	var fbsig0 = LPF.ar(dly1Wet,delay1Lowpass.linexp(0,1,minFilter,maxFilter));
	var fbsig1 = HPF.ar(dly2Wet,delay2Highpass.linexp(0,1,20,maxFilter));
	LocalOut.ar([fbsig0,fbsig1]);
	Out.ar(0,reverbOut*outputGain);
}).load)
