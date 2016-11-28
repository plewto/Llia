/*
** Notch Filter Effect with integral LFO.
*/

(SynthDef (\Notch,{
   |
	inbus = 8
	outbus = 0
	xbus = 1024
	lfoOutbus = 1023
	lfoFreq = 1.0
	cFreq = 1000
	cFreqLfo = 0     // LFO -> freq
	cFreqX = 0       // External -> freq
	filterGain = 0   // Filter gain compensatin in db
	q = 1            // Filter Q
	qLfo = 0         // LFO -> Q
	qX = 0           // External -> Q
	bleed = 0.0      // dry signal bypass
	|
	var dry = In.ar(inbus,1);
	var x = In.kr(xbus,1);
	var lfo = LFCub.kr(lfoFreq);
	var ffreq = (cFreq+(cFreqLfo*lfo)+(cFreqX*x)).max(10).min(20000);
	var fq = (q+(qLfo*lfo)+(qX*x)).abs.max(1).min(100);
	var notch = BRF.ar(dry,ffreq,1/fq)*filterGain.dbamp;
	var sigout = XFade2.ar(notch,dry,bleed.linlin(0,1,-1,1));
	Out.kr(lfoOutbus, lfo);
	Out.ar(outbus,sigout);
}).load)