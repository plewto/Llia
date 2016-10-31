(
SynthDef(\Crusher, {
	|inbus = 8
	outbus = 0
	clockFreq = 20000       // clock freq
	low = 20000             // lowpass cutoff
	wet = 0.5
	dry = 0.5
	amp = 1.0|
	var drysig = In.ar(inbus, 1);
	var clock = LFPulse.ar(clockFreq);
	var latchout = Latch.ar(drysig,clock);
	var wetsig = LPF.ar(latchout,low)*wet;
	var outsig = (drysig*dry) + wetsig;
	Out.ar(outbus,outsig*amp);
}).load
)

	