/*
 * Orgn
 *
 * An Fm Organ using 3 carrier/modulator pairs.
 *
 *    [m1]-->[c1]------------+
 *                           |
 *    [m2]-->[c2]------------+----> out
 *                           |
 *    [m3]-->[c3]---[adsr]---+
 *
 * Parameters:
 *   c1, c2, c3  - carrier frequencies.
 *   m1, m2, m3  - modulator frequencies.
 *   mod1, mod2, mod3 - Modulation depths, normalized.
 *   amp1, amp2, amp3 - linear carrier amplitudes.
 *
 *   vfreq   - vibrato frequency.
 *   vsens   - vibrato sensitivity, normalized
 *   vdelay  - programed vibrato onset delay
 *   vdepth  - programed vibrato depth, normalized
 *   vibrato - manual vibrato depth, normalized
 *
 *   chorus      - chorus depth, normalized.
 *   chorusDelay - chorus onset delay.
 *                 The chorus effect is produced by adding offset 
 *                 values to carriers 2 and 3 frequencies.
 *
 *   attack3  - carrier 3 attack time
 *   decay3   - carrier 3 decay time
 *   sustain3 - carrier 3 sustain level
 *   release3 - carrier 3 release time
 *
 *   brightness - scales mod depths for all modulators, normalized.
 *                
*/

(SynthDef (\Orgn,
	{|freq = 440,
		detune = 1.0,
		gate = 1,
		doneAction = 2,
		outbus = 0,
		amp = 0.05,
		vfreq = 5.0,
		vdelay = 2.0,
		vsens = 1.00,
		vdepth = 1.0,
		vibrato = 0.0,
		chorus = 0.0,
		chorusDelay = 2.0,
		c1 = 0.5,
		m1 = 0.5,
		mod1 = 1.0,
		amp1 = 1.0,
		c2 = 1.0,
		m2 = 1.0,
		mod2 = 1.0,
		amp2 = 1.0,
		c3 = 2.0,
		m3 = 2.0,
		mod3 = 1.0,
		amp3 = 1.0,
		attack3 = 1.0,
		decay3 = 0.0,
		sustain3 = 1.0,
		release3 = 3.0,
		brightness = 1.0|
		var vibEnv = EnvGen.kr(Env([0.001, 0.001, 1.0, 1.0],
			[vdelay, vdelay, 0.5], \linear, 2), gate, doneAction: 0);
		var chorusEnv = EnvGen.kr(Env([0.001, 0.001, 1.0, 1.0],
			[chorusDelay, chorusDelay, 0.5], \linear, 2), gate, doneAction: 0);
		var env3 = EnvGen.kr(Env.adsr(attack3, decay3, sustain3, release3,
			1.0, \exp, 0.001),gate, 1, 0, 1, doneAction);
		var vib = 1 + ((LFCub.kr(vfreq)*(vibrato+vdepth*vibEnv))*linlin(vsens, 0, 1, 0, 0.03));
		var chorusBias = chorus.linlin(0,1,0,7) * chorusEnv;
		var f0 = freq*detune*vib;
		var f1c = f0*c1;
		var f1m = f0*m1;
		var f2c = (f0*c2)-chorusBias;
		var f2m = f0*m2;
		var f3c = (f0*c3)+chorusBias;
		var f3m = f0*m3;
		var modsig1 = f1c * SinOsc.ar(f1m) * (linlin(mod1, 0,1,0,4) * brightness);
		var carsig1 = SinOsc.ar(f1c+modsig1);
		var modsig2 = f2c * SinOsc.ar(f2m) * (linlin(mod2, 0,1,0,4) * brightness);
		var carsig2 = SinOsc.ar(f2c+modsig2);
		var modsig3 = f3c * SinOsc.ar(f3m) * (linlin(mod3, 0,1,0,4) * brightness);
		var carsig3 = SinOsc.ar(f3c+modsig3);
		var outsig = (carsig1*amp1*gate) + (carsig2*amp2*gate) + (carsig3*amp3*env3);
		Out.ar(outbus, outsig*amp);
}).load;)

