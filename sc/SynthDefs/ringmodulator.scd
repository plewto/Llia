(
SynthDef(\RingModulator, {
	|carin = 8        // carrier input bus
	xmodin = 9        // external modulator input
	outbus = 0
	imodfreq = 1000   // internal modulator frequency
	imodamp = 1       // internal modulator amplitude
	xmodamp = 0       // external modulator amplitude
	xmodbleed = 0     // external modulation signal bleed to output
	carbleed = 0      // carrier signal bleed to output
	amp = 1|          // output amplitude
	var c = In.ar(carin,1);
	var xmod = In.ar(xmodin,1) * xmodamp;
	var imod = SinOsc.ar(imodfreq) * imodamp;
	var outsig = c*(xmod+imod);
	outsig = outsig + (c*carbleed) + (xmod*xmodbleed);
	Out.ar(outbus, outsig*amp);
}).load
)