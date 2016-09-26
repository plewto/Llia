






(SynthDef (\Rumklang, {
	|inbus = 0
	outbus1 = 8
	outbus2 = 9
	xbus = 1024
	gate = 1
	gatted = 0       // 0 -> disabled, 1 -> enabled
	preDelay = 0.01
	roomSize = 0.5
	damp = 0.5
	lpcutoff = 16000
	hpcutoff = 10
	modDepth = 0.0   // external sig -> wet amp
	wetAmp = 1.0
	wetPan = 0.75
	dryAmp = 1.0
	dryPan = 0.25|
	var dry = In.ar(inbus,1);
	var x = In.kr(xbus,1);
	var maxDelay = 0.33;
	var delayTime = preDelay.abs.min(maxDelay);
	var delayOut = DelayL.ar(dry,maxDelay,delayTime);
	var verbOut = FreeVerb.ar(delayOut,1.0,roomSize,damp);
	var minHP = 20;
	var hpout = HPF.ar(verbOut,hpcutoff.max(minHP));
	var lpout = LPF.ar(hpout,lpcutoff);
	var modSig = XFade2.kr(x,1,modDepth.linlin(0,1,1,-1));
	var gateSig = XFade2.kr(gate,1,gatted.linlin(0,1,1,-1));
	var outSig = Pan2.ar(dry*dryAmp, dryPan)+Pan2.ar(lpout*modSig*gateSig*wetAmp,wetPan);
	Out.ar(outbus1, outSig[0]);
	Out.ar(outbus2, outSig[1]);
}).load)