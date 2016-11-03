(
SynthDef(\Crusher, {
	|inbus = 8
	outbus = 0
	gain = 1.0              // 0..1
	wave = 0                // [0,1,2] -> [None,Softclip,Distort,Fold,Wrap]
	clockFreq = 20000       // clock freq
	resampleEnable = 0      // 0 -> bypass resample   1 -> enable resample
	low = 20000             // lowpass cutoff
	wet = 0.5
	dry = 0.5
	amp = 1.0|
	var drysig = In.ar(inbus, 1);
	var a = drysig*gain;
	var waveout = Select.ar(wave,[drysig,
		a.softclip,
		a.distort,
		a.fold2,
		a.wrap2]);
	var clock = LFPulse.ar(clockFreq);
	var latchout = Latch.ar(waveout,clock);
	var filterin = Select.ar(resampleEnable, [waveout,latchout]);
	var wetsig = LPF.ar(filterin,low)*wet;
	var outsig = (drysig*dry) + wetsig;
	Out.ar(outbus,outsig*amp);
}).load
)

	