/*
 * Simple mono tremolo effect
*/


(
SynthDef(\Tremolo, {
	|inbus = 128,
	outbus = 0,
	xbus = 1024,      // external control bus
	lfoFreq = 5.0,    // internal LFO freq
	lfoOutbus = 1023, // internal LFO -> control bus
	modDepth = 0.0,   // internal LFO modulation depth, normalized
	limit = 1.0,      // absolute maximum modulation amplitude
	amp = 1.0,        // overall amplitude
	xDepth = 0.0,     // external sig scale factor
	xLfoAmp = 0.0,    // exrternal sig to internal LFO amp
	xLfoFreq = 0.0|   // external sig to internal LFO freq (Hz)
	var dry = In.ar(inbus, 1);
	var x = In.kr(xbus,1);
	var xToLfoAmp = XFade2.kr(1, x, xLfoAmp.linlin(0,1,-1,1));
	var xToLfoFreq = x * xLfoFreq;
	var lfo = LFCub.kr(lfoFreq+xToLfoFreq, 0, 0.5, 0.5) * xToLfoAmp;
	var ctrl = ((x*xDepth) + XFade2.kr(1, lfo, modDepth.linlin(0,1,-1,1))).max(0).min(limit);
	var outsig = dry * ctrl * amp;
	Out.ar(outbus, outsig);
	Out.kr(lfoOutbus, lfo);
}).load;
)