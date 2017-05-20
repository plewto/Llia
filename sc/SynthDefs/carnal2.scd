/*
** Carnal2
*/

(SynthDef (\Carnal2, {
    |outbus1 = 0            // Audio out
	outbus2 = 1
	inbus1 = 8              // Audio in
	inbus2 = 9
	xbus = 1023             // external control bus -> delay time
	timebase = 1.00         // LFO referance freq. >0.
	gate=1   // FOR DEBUG ONLY
	delayTime1 = 0.1        // Delay time 0..1
	modDepth1 = 0.0         // LFO -> delay time 0..1
	xmodDepth1 = 0.0        // xbus -> delay time 0..1
	lfoRatio1 = 1.0         // LFO frequency realtive to time base >0
	feedback1 = 0.0         // -1..+1
	efxMix1 = 0.5           // Wet mix 0..1
	efxPan1 = 0.5           // Wet pan -1..+1
	dryMix1 = 0.5           // Dry mix 0..2
	dryPan1 = 0.5           //
	lowcut1 = 16000         // Feedback lowpass cutoff in Hz   20..16k
	highcut1 = 20           // Feedback highpass cutoff in Hz
	clipEnable1 = 0         // 0=disabled 1=feedback clipper enabled.
	clipGain1 = 1.0         // Feedback clipper input gain 0..4
	clipThreshold1 = 1.0    // Feedback clipper threshold 0..1
	xfeedback1 = 0.0        // Cross feedback from other line -1..+1
	delayTime2 = 0.1
	modDepth2 = 0.0
	xmodDepth2 = 0.0
	lfoRatio2 = 1.0
	feedback2 = 0.0
	efxMix2 = 0.5
	efxPan2 = 0.5
	dryMix2 = 0.5
	dryPan2 = 0.5
	lowcut2 = 16000
	highcut2 = 20
	clipEnable2 = 0
	clipGain2 = 1.0
	clipThreshold2 = 1.0
	xfeedback2 = 0.0|
	var maxdelay = 1.00;
	var drysig = In.ar([inbus1,inbus2]);
	var lfo = LFCub.kr([lfoRatio1,lfoRatio2]*timebase,[0,0.667],0.5*[delayTime1,delayTime2]*[modDepth1,modDepth2]);
	var xsig = In.kr(xbus)*(0.1*maxdelay*[xmodDepth1,xmodDepth2]);
	var delayTime = ([delayTime1,delayTime2]+lfo+xsig).min(maxdelay).max(0);
	var fbsig = LocalIn.ar(2)*[feedback1,feedback2];
	var xfbsig = [fbsig[1]*xfeedback1,fbsig[0]*xfeedback2];
	var delayin = drysig+fbsig+xfbsig;
	var wetsig = DelayC.ar(delayin,maxdelay,delayTime);
	var clip1 = Select.ar(clipEnable1,[wetsig[0],(wetsig[0]*clipGain1).clip2(clipThreshold1)]);
	var clip2 = Select.ar(clipEnable2,[wetsig[1],(wetsig[1]*clipGain2).clip2(clipThreshold2)]);
	var hp1 = highcut1.min(16000).max(20);
	var hp2 = highcut2.min(16000).max(20);
	var lp1 = lowcut1.min(16000).max(20);
	var lp2 = lowcut2.min(16000).max(20);
	var fbsend1 = LPF.ar(HPF.ar(clip1,hp1),lp1);
	var fbsend2 = LPF.ar(HPF.ar(clip2,hp2),lp2);
	var outsig = Pan2.ar(wetsig*[efxMix1,efxMix2],[efxPan1,efxPan2])+Pan2.ar(drysig*[dryMix1,dryMix2],[dryPan1,dryPan2]);
	LocalOut.ar([fbsend1,fbsend2]);
	Out.ar([outbus1,outbus2],outsig);
}).load)
