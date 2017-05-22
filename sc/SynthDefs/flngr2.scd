/*
** Flngr2
*/

(SynthDef (\Flngr2, {
    |outbus1 = 0
	outbus2 = 1
	inbus1 = 8
	inbus2 = 9
	xbus = 1024
	timebase = 1.0
	delay1 = 0.5
	xmod1 = 0.0
	depth1 = 0.5
	lfoRatio1 = 1.0
	feedback1 = 0.0
	xfeedback1 = 0.0
	lowpass1 = 16000
	efxMix1 = 1.0
	efxPan1 = 0.0
	dryMix1 = 1.0
	dryPan1 = 0.0
	delay2 = 0.5
	xmod2 = 0.0
	depth2 = 0.5
	lfoRatio2 = 1.0
	feedback2 = 0.0
	xfeedback2 = 0.0
	lowpass2 = 16000
	efxMix2 = 1.0
	efxPan2 = 0.0
	dryMix2 = 1.0
	dryPan2 = 0.0|
	var maxdelay = 0.01;
	var drysig = In.ar([inbus1, inbus2]);
	var xsig = In.kr(xbus);
	var fbcutoff = [lowpass1,lowpass2].max(50).min(16000);
	var fbsig = LocalIn.ar(2);
	var xfbsig = [fbsig[1],fbsig[0]];
	var fb1 = LPF.ar((fbsig[0]*feedback1)+(xfbsig[1]*xfeedback1),fbcutoff[0]);
	var fb2 = LPF.ar((fbsig[1]*feedback2)+(xfbsig[0]*xfeedback2),fbcutoff[1]);
    var dlytime = [delay1, delay2].max(0).min(maxdelay);
	var lfo = LFCub.kr([lfoRatio1*timebase,lfoRatio2*timebase],[0,0.6667],dlytime*0.25*[depth1,depth2]);
	var xmod = xsig*dlytime*0.25*[xmod1,xmod2];
	var delaytime = (dlytime+lfo+xmod).max(0).min(maxdelay);
	var wetsig = DelayC.ar(drysig+[fb1,fb2],maxdelay,delaytime);
	//var out = Pan2.ar((wetsig*[efxMix1,efxMix2])+(drysig*[dryMix1,dryMix2]),[efxPan1,efxPan2,dryPan1,dryPan2]);
	var dryout1 = Pan2.ar(drysig[0]*dryMix1,dryPan1);
	var dryout2 = Pan2.ar(drysig[1]*dryMix2,dryPan2);
	var wetout1 = Pan2.ar(wetsig[0]*efxMix1,efxPan1);
	var wetout2 = Pan2.ar(wetsig[1]*efxMix2,efxPan2);
	LocalOut.ar(wetsig);
	Out.ar(outbus1, dryout1[0]+dryout2[0]+wetout1[0]+wetout2[0]);
	Out.ar(outbus2, dryout1[1]+dryout2[1]+wetout1[1]+wetout2[1]);
}).load)
