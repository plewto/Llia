/*
** TTone - Test Tone generator.
*/

(SynthDef (\TTone, {
    |outbus = 0            // Audio out bus
	gate = 1               //
	doneAction = 2         //
	freq = 440             //
	ratio = 1.0            // Freq ratio
	bias = 0.0             // Freq bias (Hz)
	wave = 0               // 0=sine, 1=square, 2=saw, 3=white noise
	amp = 0.1|             // linear amplitude
	var frequency = (freq*ratio)+bias;
	var snsig = SinOsc.ar(frequency);
	var sqrsig = Pulse.ar(frequency, 0.5);
	var sawsig = Saw.ar(frequency);
	var nse = WhiteNoise.ar();
	var out = Select.ar(wave,[snsig,sqrsig,sawsig,nse]);
	Out.ar(outbus,out*gate*amp);
	}).load)
