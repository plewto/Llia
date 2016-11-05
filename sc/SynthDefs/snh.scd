

(SynthDef (\SnH, {
	|outbus = 1024
	sawbus = 1024
	noisebus = 1024
	clockoutbus = 1024
	xbus = 1023
	clockbus = 1023
	clockSource = 0     // 0 -> internal, 1 -> external
	clockRate = 1.0
	sawFreq = 3.0
	sawMix = 0.0
	noiseMix = 1.0
	externalMix = 0.0
	lag = 0.0
	scale = 1.0
	bias = 0.0|
	var saw = LFSaw.kr(sawFreq);  // *sawMix;
	var noise = WhiteNoise.kr();  // *noiseMix;
	var x = In.kr(xbus)*externalMix;
	var srcSig = (saw*sawMix) + (noise*noiseMix) + x;
	var xclock = In.kr(clockbus);
	var iclock = LFPulse.kr(clockRate);
	var clock = Select.kr(clockSource,[iclock,xclock]);
	var sh = Latch.kr(srcSig,clock);
	var outsig = Lag2.kr(sh,lag.linlin(0,1,0.0,0.3))*scale+bias;
	Out.kr(sawbus,saw);
	Out.kr(noisebus, noise);
	Out.kr(clockoutbus,clock);
	Out.kr(outbus,outsig);
}).load)
	