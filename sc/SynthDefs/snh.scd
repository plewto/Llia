(
SynthDef (\SnH, {
	|outbus = 1024, 
	gate = 1             //
	shRate = 1.0,        // sample rate
	srcFreq = 3.0,       // internal LFO freq
	srcSelect = 0,       // sample source, 0 -> saw  1 -> noise
	shLag = 0.0,         // lag time
	shBleed = 0.0,       // envelope bypass, 0 -> use env. 1-> ignore env
	shDelay = 0.0,       // env onset delay
	shAttack = 0.0,      // env onset attack time
	shHold = 1.0,        // env hold time after gate low
	shRelease = 1.0,     // env release after hold segment
	shScale = 1.0,       // output scale factor
	shBias = 0.0|        // output bias
	var env = EnvGen.kr(Env([0,0,1,1,0],[shDelay,shAttack,shHold,shRelease],
		\lin, 2) ,gate, doneAction: 0);
	var saw = LFSaw.kr(srcFreq);
	var srcsig = XFade2.kr(saw, WhiteNoise.kr(), srcSelect.linlin(0,1,-1,1));
	var clock = LFPulse.kr(shRate);
	var sh = Latch.kr(srcsig, clock);
	env = XFade2.kr(env, 1, shBleed.linlin(0,1,-1,1));
	sh = Lag3.kr(sh, shLag.linlin(0,1,0,0.5))*env*shScale+shBias;
	Out.kr(outbus, sh);
}).load;
)

