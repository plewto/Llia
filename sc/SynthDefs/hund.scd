/*
** Defines Hund synth
** Lowpass filter with envelope follower
*/

(SynthDef (\Hund, {
   |inbus = 128
	outbus = 0
	xbus = 1024         // external control input
	envout = 1023       // env follower output bus
	pregain = 1         // env follower input gain 0..4
	attack = 0.01
	release = 0.01
	filterFreq = 1000   // HZ
	res = 0.5           // normalize 0..1
	modDepth = 0.0      // env follower -> filter
	xmod = 0.0          // external -> filter
	dryamp = 1.0        // dry signal amp
	wetamp = 1.0|       // filter output amp
	var dry = In.ar(inbus,1);
	var x = In.kr(xbus,1);
	var env = Lag.kr(Amplitude.kr(dry*pregain,attack,release),0.1);
	var maxFilter = 20000;
	var minFilter = 100;
	var cutoff = ((env*modDepth*800) + (x*xmod * 800) + filterFreq).min(maxFilter).max(minFilter);
	var lpGain = res.linlin(0,1,0.5,3.99);
	var lpsig = MoogFF.ar(dry,cutoff,lpGain);
	var outsig = (dry*dryamp)+(lpsig*wetamp);
	Out.kr(envout,env);
	Out.ar(outbus,outsig);
}).load)