
/*
 * CarnalDelay - An unclean mono delay
 * Mono delay line with compromised feedback path.
*/

(SynthDef (\CarnalDelay,
	{|inbus = 128,
		outbus = 0,
		efxbus = 1024,         // external control bus for efx mix
		dlybus = 1024,         // external control bus for delay time
		delayTime = 0.125,     // mean delay time, seconds
		wow = 0.0,             // periodic delay time modulation, normalized
		wowFreq = 1.0,         // wow signal frequency, Hertz
		flutter = 0.0,         // noise delay time modulation, normalized
		xDelayMod = 0.0,       // external delay time modulation, normalized assuming (0..1) signal amplitude
		feedback = 0.0,        // delay feedback,normalized
		gain = 1.0,            // feedback path gain (pre clipper)
		threshold = 1.0,       // feedback clipping threshold, normalized
		lowcut = 10000,        // feedback lowpass cutoff, Hertz
		highcut = 100,         // feedback highpass cutoff, Hertz
		efxMix = 0.5,          // wet/dry signal mix, 0 -> dry, 1 -> wet
		xEfxMix = 0.0,         // external efx mix modulation, normalized
		amp = 1.0|             // overall gain
		var drysig = In.ar(inbus, 1);
		var xefx = In.kr(efxbus,1);
		var xdly = In.kr(efxbus,1);
		var fb = LocalIn.ar(1) * (feedback.max(0).min(1));
		var clipperIn = fb * gain;
		var clipperOut = clip2(clipperIn,threshold.max(0).min(1));
		var eqout = HPF.ar(LPF.ar(clipperOut, lowcut.max(20).min(16000)), highcut.max(20).min(16000));
		var delayIn = drysig + eqout;
		var maxDelayTime = 1.5;
		var wowsig = LFCub.kr(wowFreq) * wow.linlin(0,1,0,0.01);
		var fluttersig = Lag2.kr(BrownNoise.kr(delayTime*flutter.linlin(0,1,0,0.01)), 0.1);
		var xdlysig = xdly*xDelayMod.linlin(0,1,0,0.1);
		var dlyTime = (delayTime * (1 + wowsig) * (1 + fluttersig) * (1 + xdlysig)).max(0).min(maxDelayTime);
		var wetsig = DelayC.ar(delayIn, maxDelayTime, dlyTime);
		var wetLevel = (efxMix + (xefx * xEfxMix)).linlin(0, 1, -1, 1);
		var outsig = XFade2.ar(drysig, wetsig, wetLevel) * amp;
		LocalOut.ar(wetsig);
		Out.ar(outbus, outsig);
}).load;
)


