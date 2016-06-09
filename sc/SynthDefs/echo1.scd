/*
 * Echo1
 * A single delay line with dirty feedback path.
 *
 * Parameters:
 *    inbus        - Input audio bus.
 *    outbus       - Output audio bus.
 *    maxDelayTime - Maximum delay time.
 *    delayTime    - Delay time in seconds, 
 *    gain         - Feedbnack gain.
 *    threshold    - Feedback clipping threshold.  Lower values produce.
 *                   greater clipping.  threshold and gain interact. 
 *    lowcut       - Lowpass cutoff in Hertz.
 *    highcut      - Highpass cutoff in Hewrtz.
 *    feedback     - Feedback amount.  Feedback ointeracts with gain and 
 *                   threshold.  0 <= feedback < 1.
 *    flutter      - Amount of random flutter added to delay time.
 *                   0 <= flutter <= 1.
 *    wow          - Amount of periodic variation added to delay time.
 *                   0 <= wow <= 1.
 *    wowFreq      - Frequency of "wow" signal in Hertz.
 *    wetAmp       - Delay signal linear amplitude.
 *    dryAmp       - Dry signal linear ampliude.
 *    wetPan       - Delay signal pan position.
 *    dryPan       - Dry signal pan position.
 *    volume       - General linear amplitude.
*/

(SynthDef (\Echo1,
	{|inbus = 128,
		outbus = 0,
		maxDelayTime = 1.5,
		delayTime = 0.125,
		gain = 1.0,
		threshold = 1.0,
		lowcut = 10000,
		highcut = 100,
		feedback = 0.8,
        flutter = 0.1,
		wow = 0.1,
		wowFreq = 1.0,
		wetAmp = 0.5,
		dryAmp = 1.0,
		wetPan = 0.25,
		dryPan = -0.25,
		volume = 1.0|
		var drysig, fbsig, dlyin, wetsig, outsig, lfo;
		lfo = LFCub.kr(wowFreq);
		flutter = flutter.linlin(0, 1, 0, 0.01);
		wow = wow.linlin(0, 1, 0, 0.01);
		delayTime = delayTime + (lfo*wow*delayTime);
		delayTime = delayTime + BrownNoise.kr(delayTime*flutter);
		delayTime = delayTime.clip(0, maxDelayTime);
		drysig = In.ar(inbus);
		feedback = feedback.clip(0, 0.95);
		fbsig = LocalIn.ar(1) * feedback;
		dlyin = drysig+fbsig;
		dlyin = clip2(dlyin*gain, threshold);
		dlyin = HPF.ar(LPF.ar(dlyin, lowcut), highcut);
		wetsig = DelayC.ar(dlyin, maxDelayTime, delayTime);
		outsig = Pan2.ar(drysig*dryAmp, dryPan) + Pan2.ar(wetsig*wetAmp, wetPan);
		LocalOut.ar(wetsig);
		Out.ar(outbus, outsig*volume);
}).load;)

