/*
 * Simple LFO control synth with integrated envelope.
 * 
 * lfoFreq    - Frequency ion Hertz.
 * lfoWave    - Wave selection 0 -> sine, 1 -> sine^2
 * lfoBias    - Value added to wave
 * lfoScale   - Wave scale factor
 * lfoAmp     - Output amplitude
 * lfoDelay   - Onset delay in seconds.
 * lfoAttack  - Onset attack in seconds (after initial delay)
 * lfoHold    - Hold time after gate goes low.
 * lfoRelease - Release time after hold seconds.
*/

(
SynthDef (\LFO1, {|ctrlOutbus = 1024,
	gate = 1,
	lfoFreq = 2.0,
	lfoWave = 0, // 0 -> sine, 1 -> sine**2
	lfoAmp = 1.0,
	lfoScale = 1.0,
	lfoBias = 0.0,
	lfoDelay = 0.0,
	lfoAttack = 0.0,
	lfoHold = 1.0,
	lfoRelease = 1.0|
	var env = EnvGen.kr(Env([0,0,1,1,0],[lfoDelay,lfoAttack,lfoHold,lfoRelease],\lin, 2)
		,gate, doneAction: 0);
	var sine = SinOsc.kr(lfoFreq);
	var sine2 = sine*sine*2-1;
	var wave = XFade2.kr(sine, sine2, lfoWave.linlin(0,1,-1,1));
	wave = (wave*lfoScale+lfoBias)*env*lfoAmp;
	Out.kr(ctrlOutbus, wave);
}).load;
)

