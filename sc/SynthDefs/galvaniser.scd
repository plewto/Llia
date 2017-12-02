/*
** Galvaniser
**
** Adopted after Cubase "Metalizer" effect.
**
**  -->[static comb filter]-->[bandpass filter]-->
**                              ^
**                              |
**                            [LFO]
**
*/

(SynthDef (\Galvaniser, {
    |inbus = 128
     outbus = 0
     xbus = 1023
     lfobus = 1024
     feedback = 0.0
     tone = 0.5
     filter = 0.5
     res = 0.0
     lfoFreq = 0.1
     modDepth = 0.1
	 xmodDepth = 0.0
     efxmix = 0.5
     amp = 1.0|
    var minFilterFreq = 200;
	var maxFilterFreq = 4000;
	var maxDelayTime = 1/minFilterFreq;
	var lfo = SinOsc.kr(lfoFreq);
	var cfreq = max(tone.linexp(0,1,minFilterFreq,maxFilterFreq),minFilterFreq);
	var cdelay = min(1/cfreq, maxDelayTime);
	var cdecay = feedback.linlin(-1,1,-0.3,0.3);
	var drysig = In.ar(inbus);
	var cfilter = CombC.ar(drysig,maxDelayTime,cdelay,cdecay);
	var xfreq = min(max(In.kr(xbus),0),1)*xmodDepth;
	var bfreq = filter.linexp(0,1,minFilterFreq,maxFilterFreq)*(1 + (lfo*modDepth) + xfreq);
	var bwr = res.linlin(0,1,1,0.05);
	var wetsig = Resonz.ar(cfilter,bfreq,bwr);
	var outsig = LinXFade2.ar(drysig,wetsig,efxmix.linlin(0,1,-1,1));
	Out.ar(outbus,outsig*amp);
	Out.kr(lfobus, lfo);
}).load)
