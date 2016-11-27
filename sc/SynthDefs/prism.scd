/*
** Defines Prism synth
*/

(SynthDef (\Prism,{
	|
	inbus = 8
	outbusLow = 0
	outbusCenter = 1
	outbusHigh = 3
	fLow = 400         // lowpass cutoff
	fHigh = 1200       // highpass cutoff
	bwScale = 1        // center filter band width scale
	gainLow = 0        // lowpass gain in db
	gainCenter = 0     //
	gainHigh = 0
	|
	var dry = In.ar(inbus);
	var flp = min(fLow,fHigh).min(20000).max(10);
	var fhp = max(fLow,fHigh).min(20000).max(10);
	var bw = (fhp-flp)*bwScale;
	var fc = (fhp+flp)/2;
	var rq = bw/fc;
	var lp = LPF.ar(dry,flp)*(gainLow.dbamp);
	var hp = HPF.ar(dry,fhp)*(gainHigh.dbamp);
	var bp = BPF.ar(dry,fc,rq)*(gainCenter.dbamp);
	Out.ar(outbusLow,lp);
	Out.ar(outbusCenter,bp);
	Out.ar(outbusHigh,hp);
}).load)