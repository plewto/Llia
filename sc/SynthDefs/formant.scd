/*
** Defines Formant synth
** 4 band parametric EQ
*/

(SynthDef (\Formant,{
	|
	inbus = 128
	outbus = 0
	hp = 10            // highpass cutoff
	lp = 20000         // lowpass cutoff
	f1 = 220           // center freq filer 1
	q1 = 1             // q filter (0..1) -> q(1..100)
	gain1 = 0          // gain filter 1 in db
	enable1 = 1        // 0|1  mute/enable channel
	f2 = 660
	q2 = 1
	gain2 = 0
	enable2 = 1
	f3 = 990
	q3 = 1
	gain3 = 0
	enable3 = 1
	f4 = 1200
	q4 = 1
	gain4 = 0
	enable4 = 1
	amp = 0         // main amp in db
	bleed = 0       // dry signal bypass 0..1  1 -> bypass filter
    |
	var dry = In.ar(inbus);
	var low = LPF.ar(dry,lp);
	var high = HPF.ar(low,hp);
	var rq = 1/([q1,q2,q3,q4].linexp(0,1,1,100));
	var ampcomp = -12.dbamp;
	var eq = MidEQ.ar(high, [f1,f2,f3,f4],rq,[gain1,gain2,gain3,gain4])*[enable1,enable2,enable3,enable4];
	var outsig = XFade2.ar(Mix.ar(eq)*ampcomp,dry,bleed.linlin(0,1,-1,1))*amp.dbamp;
	Out.ar(outbus,outsig);
}).load)



