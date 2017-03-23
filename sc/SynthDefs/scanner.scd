/*
** Scanner
*/

(SynthDef (\Scanner, {
    |
	outbus1 = 0
	outbus2 = 1
	inbus = 8
	xbus = 1024       // external control sig input
	lfobus = 1023     // lfo output bus
	scanRate = 7.0
	wave = 0.5        // 0.0 .. 0.5  .. 1.0   (saw,tri,saw)
	delay = 0.1       //  0 .. 1
	feedback = 0.0    // -1.0 < fb < +1
	lowpass = 16000   // feedback lowpass in Hz
	dryMix = 1.0
	wet1Mix = 1.0
	wet2Mix = 1.0
	modDepth = 1.0    // 0 <= modDepth <= 1
	xmodDepth = 0.0   // external mod depth
    |
	var maxDelay = 0.05;
	var nStages = 9;
	var maxStageDelay = maxDelay/nStages;
	var drysig = In.ar(inbus);
	var fbsig = LocalIn.ar(1);
	var dtime = max(0,min( maxStageDelay,delay/nStages));
	var delay01 = DelayL.ar(drysig+fbsig,maxStageDelay,dtime);
	var delay02 = DelayL.ar(delay01,maxStageDelay,dtime);
	var delay03 = DelayL.ar(delay02,maxStageDelay,dtime);
	var delay04 = DelayL.ar(delay03,maxStageDelay,dtime);
	var delay05 = DelayL.ar(delay04,maxStageDelay,dtime);
	var delay06 = DelayL.ar(delay05,maxStageDelay,dtime);
	var delay07 = DelayL.ar(delay06,maxStageDelay,dtime);
	var delay08 = DelayL.ar(delay07,maxStageDelay,dtime);
	var delay09 = DelayL.ar(delay08,maxStageDelay,dtime);
	var taps = [delay01, delay02, delay03,
		delay04, delay05, delay06,
		delay07, delay08, delay09,
		delay08, delay07, delay06,
		delay05, delay04, delay03,
		delay02];
	var scanScale = (taps.size-1);
	var lfo1a = VarSaw.kr(scanRate,0,wave).linlin(-1,1,0,1);
	var lfo1 = lfo1a*modDepth;
	var lfo2 = lfo1.linlin(0,1,1,0);
	var x1 = In.kr(xbus,1)*xmodDepth;
	var x2 = x1.linlin(0,1,1,0);
	var mod1 = (lfo1+x1)*scanScale;
	var mod2 = (lfo2+x2)*scanScale;
	var wet1 = LinSelectX.ar(mod1,taps);
	var wet2 = LinSelectX.ar(mod2,taps);
	var fbSend = LPF.ar(wet1,max(lowpass,10))*feedback;
	var dry = drysig*dryMix;
	var out1 = dry+(wet1*wet1Mix);
	var out2 = dry+(wet2*wet2Mix);
	LocalOut.ar(fbSend);
	Out.ar(outbus1,out1);
	Out.ar(outbus2,out2);
	Out.kr(lfobus, lfo1a);
}).load)
