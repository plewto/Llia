/*
 * Simple sine/FM Feedback LFO with integrated envelope.
 * outbus      - Control output bus
 * gate        - Envelope gate signal.
 * lfoFreq     - Frequency in Hertz.
 * lfoFeedback - FM Feedback, normalized
 * lfoDelay    - Onset delay in seconds
 * lfoAttack   - Onset attack time after delay segment
 * lfoHold     - Envelope hold time after gate goes low
 * lfoRelease  - Envelope release time after hold segment
 * lfoBleed    - Amount of LFO signal which "bleeds" through envelope.
 *               For bleed = 1 the envelope has no effect.
 * lfoScale    - Amplitude scale factor.
 * lfoBias     - Bias value added to lfo signal.
*/

(SynthDef (\LFO1, {
	|outbus = 1024,
	gate = 1,
	lfoFreq = 1.0,
	lfoFeedback = 0.0,
	lfoDelay = 0.0,
	lfoAttack = 0.0,
	lfoHold = 0.5
	lfoRelease = 0.5,
	lfoBleed = 0.0,
	lfoScale = 1.0,
	lfoBias = 0.0|
	var env, fb, sine, outsig;
	env = EnvGen.kr(Env([0,0,1,1,0],[lfoDelay,lfoAttack,lfoHold,lfoRelease],
		\lin, 2) ,gate, doneAction: 0);
	env = XFade2.kr(env, 1, lfoBleed.linlin(0,1,-1,1));
	fb = lfoFeedback.linlin(0, 1, 0, 4);
	sine = SinOscFB.kr(lfoFreq, fb) * env;
	outsig = sine * lfoScale + lfoBias;
	Out.kr(outbus, outsig);
}).load;
)




