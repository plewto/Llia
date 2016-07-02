/*
 * StepFilter effect.
 *
 * Two indenpendent band-bass filters with complex control sources.
*/

(SynthDef (\StepFilter,
	{|inbus = 128,
		outbus = 0,
		dryAmp = 0.0,
		dryPan = 0.0,
		amp = 1.0,
		// pulse generators
		clockFreq = 1,
		r1 = 0.5,
		r2 = 0.75,
		r3 = 1.00,
		r4 = 2.00,
		r5 = 3.00,
		r6 = 4.00,
		r7 = 5.00,
		r8 = 6.00,
		// Filter A
		a1 = 0.00,
		a2 = 0.00,
		a3 = 1.00,
		a4 = 0.00,
		a5 = 0.00,
		a6 = 0.00,
		a7 = 0.00,
		a8 = 0.00,
		aLag = 0.00,   // 0...1
		aMin = 100,
		aMax = 2000,
		aRes = 0.0,
		aPan = -0.75,
		aAmp = 1.0,
		// Filter B
		b1 = 0.00,
		b2 = 0.00,
		b3 = 0.00,
		b4 = 1.00,
		b5 = 0.00,
		b6 = 0.00,
		b7 = 0.00,
		b8 = 0.00,
		bLag = 0.00,   // 0...1
		bMin = 100,
		bMax = 2000,
		bRes = 0.0,
		bPan = -0.75,
		bAmp = 1.0,
		// Panner
		panLfoFreq = 1.00,
		panLfoDry = 0.00,
		panLfoA = 0.00,
		panLfoB = 0.00,
		panLfoBRatio = 1.00|
		var drysig = In.ar(inbus, 1);
		var rary = [r1,r2,r3,r4,r5,r6,r7,r8] * clockFreq;
		var pulsesig = LFPulse.kr(rary, 0, 0.5, 0.5, 0.5);
		var aary = [a1,a2,a3,a4,a5,a6,a7,a8];
		var asig = Lag2.kr(Mix.kr(pulsesig*aary)/(aary.sum),aLag.linlin(0,1,0,0.2));
		var bary = [b1, b2, b3, b4, b5, b6, b7, b8];
		var bsig = Lag2.kr(Mix.kr(pulsesig*bary)/(bary.sum), bLag.linlin(0,1,0,0.2));
		// Filter A
		var afreq = asig.linexp(0, 1, aMin, aMax).clip(100, 16000);
		var arq = aRes.linlin(0, 1, 1, 0.05);
		var awet = BPF.ar(BPF.ar(drysig, afreq, arq), afreq, arq);
		// Filter B
		var bfreq = bsig.linexp(0, 1, bMin, bMax).clip(100, 16000);
		var brq = bRes.linlin(0, 1, 1, 0.05);
		var bwet = BPF.ar(BPF.ar(drysig, bfreq, brq), bfreq, brq);
		// Panner
		var lfo1 = LFTri.kr(panLfoFreq);
		var lfo2 = LFTri.kr(panLfoFreq*panLfoBRatio);
		var drypan = (dryPan+(panLfoDry*lfo1)).clip(-1, 1);
		var apan  = (aPan+(panLfoA*lfo1)).clip(-1, 1);
		var bpan = (bPan+(panLfoB*lfo2)).clip(-1, 1);
		var outsig;
		outsig = dryAmp * Pan2.ar(drysig, drypan);
		outsig = outsig + (aAmp * Pan2.ar(awet, apan));
		outsig = outsig + (bAmp * Pan2.ar(bwet, bpan));
		outsig = amp*outsig;
		Out.ar(outbus, outsig);
}).load)





