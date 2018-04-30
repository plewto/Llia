/*
 * Equal power pan signal to one of two buses
 *
 * Pan control sources:
 *   static value
 *   internal triangle LFO
 *   external signal
 *
 * Audio outpus:  2
 * Control outputs: internal LFO
*/


(SynthDef (\Panner, {
	|inbus = 128,
	outbusA = 0,
	outbusB = 1,
	lfoOutbus = 1024,
	xbus = 1024,
	pos = 0.0
	lfoFreq = 1.0,
	lfoDepth = 0.0
	xscale = 0.0,
    xbias = 0.0,
    amp = 1.0|
	var dry = In.ar(inbus)*amp;
	var x = In.kr(xbus) * xscale + xbias;
	var lfo = LFTri.kr(lfoFreq);
	var position = pos + (lfo * lfoDepth) + x;
	var outsig = Pan2.ar(dry, position);
	Out.ar(outbusA, outsig[0]);
	Out.ar(outbusB, outsig[1]);
	Out.kr(lfoOutbus,lfo);
}).load)



