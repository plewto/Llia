/*
** Fxstack
*/


(SynthDef (\Fxstack, {
	|

	/** Start Test Arguments **/
	ttfreq=440
	ttamp = 1.0
	gate = 1
	/** End Test Arguments **/

	outbus0 = 0
	outbus1 = 1
	inbus = 8
	inputGain = 1.0
	outputGain = 1.0
	// Envelope Follower
	envGain = 1.0   // 1..400?
	attack = 0.0    // 0..2
	release = 0.0   // 0..2
	// LFOs
	lfo1Freq = 1.0
	lfo2Freq = 1.0
	lfo2mod = 0.0   // LFO1 mod of LFO2
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
	flangerDelay = 0.5     // 0..1
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

	/** Start Test Tones **/
	var testtone = SinOsc.ar(ttfreq,0,gate*ttamp);
	//var testtone = Pluck.ar(Saw.ar(ttfreq),LFPulse.kr(1)*gate,0.2,1/ttfreq,1,0.5,ttamp);


	var minFilter = 30;       // Minimum filter cutoff
	var maxFilter = 20000;
	// var insig = In.ar(inbus); /* ISSUE: Uncomment after testing */
	var insig = testtone;        /* ISSUE: Remove after testing */
	// Envelope Follower
	var envTrig = insig*envGain;
	var env = Lag2.kr(Amplitude.kr(envTrig,attack,release),0.05);
	// LFOs
	var lfo1 = LFCub.kr(lfo1Freq);
	var lfo2Amp = LinXFade2.kr(1,lfo1,lfo2mod.linlin(0,1,-1,1));
	var lfo2 = LFCub.kr(lfo2Freq,0,lfo2Amp);
	// Audio input & Clipper
	var dry = insig*inputGain;
	var clipGain = clipDrive.linexp(0,1,1,80).max(1);
	var clipA = (insig*clipGain);
	var clipB = (-1.2)*clipA;
	var clipC = (-1.0)*clipA;
	var clipAmp = LinXFade2.kr(1,lfo1,clipLfo1.linlin(0,1,-1,1));
	var clipIn = ((clipA.exp-clipB.exp)/(clipA.exp+clipC.exp))/clipGain;
	var clipWet = Limiter.ar(clipIn,0.9,0.01)*clipAmp;
	var clipOut = LinXFade2.ar(dry,clipWet,clipMix.linlin(0,1,-1,1));

	Out.ar(0,clipOut*0.5);

}).send)

/* *** START TEST *** */


(
q.free;
q = Synth(\Fxstack, [\ttfrq, 440]);
q.set(\clipDrive, 0.0);
q.set(\clipMix, 1.0);
q.set(\clipLfo1, 1.0);
q.set(\lfo1Freq, 1.0);
)





