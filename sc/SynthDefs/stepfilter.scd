/*
 * StepFilter effect.
 * 
 * Bandpass filter with summed pulse control 
 * 
 * Parameters:
 * inbus    - Audio input bus, 1 channel                
 * outbus   - Audio output bus, 2, channels                   
 * volume   - Overall linear gain                    
 * pan      - Pan position (-1,+1)                 
 * wet      - Wet signal mix (-1=Dry, +1=Wet)                 
 * sub1     - Control signal component amp 1/2                    
 * sub2     - Control signal component amp 3/4                   
 * n1       - Control signal component amp 1                  
 * n2       - Control signal component amp 2
 * n3       - Control signal component amp 3                 
 * n4       - Control signal component amp 4                 
 * n5       - Control signal component amp 5                 
 * n6       - Control signal component amp 6                 
 * shFreq   - Sample and hold clock frequency                    
 * sh       - Sample and hold component amp                
 * clkFreq  - LFO frequency                     
 * minFreq  - Minimum filter frequency in Hertz                     
 * maxFreq  - Maximum filter frequency in Hertz                      
 * rq       - Filter 1/q parameter, (0.1,...,1.0)                
 * lag      - Filter control lag time (0,1)                 
*/

(SynthDef (\StepFilter,
	{|inbus = 128,
		outbus = 0,
		volume = 1,
		pan = 0.0,
		wet = 0.0,
		sub1 = 0.000,   // 0.50
		sub2 = 0.000,   // 0.75
		n1 = 1.000,
		n2 = 0.000,
		n3 = 0.000,
		n4 = 0.000,
		n5 = 0.000,
		n6 = 0.000,
		shFreq = 1.000,    // Sample and Hold
		sh = 1.000,
		clkFreq = 1.000,
		minFreq = 100,
		maxFreq = 2000,
		rq = 1.0,
		lag = 0.1|
		var shsig;
		var fary, pary, aary, pamp, pls, ffreq;
		var insig, outsig;
		pamp = sub1+sub2+n1+n2+n3+n4+n5+n6+sh;
		fary = [0.50, 0.75, 1,2,3,4,5,6]*clkFreq;
		pary = [0];
		aary = [sub1, sub2, n1,n2,n3,n4,n5,n6];
		shsig = (Latch.kr(BrownNoise.kr(), LFPulse.kr(shFreq))*sh).abs;
		pls = Mix.kr(LFPulse.kr(fary,pary,0.5,aary)) + shsig;
		pls = Lag2.kr(pls.linlin(0, pamp, 0 ,1), lag);
		ffreq = pls.linexp(0, 1, minFreq, maxFreq).clip(10, 12000);
		insig = In.ar(inbus, 1);
		rq = rq.clip(0.1, 1.0);
		outsig = BPF.ar(BPF.ar(insig, ffreq, rq), ffreq, rq);
		outsig = XFade2.ar(insig, outsig, wet);
		outsig = Pan2.ar(outsig*volume, pan);
		Out.ar(outbus, outsig);
}).load;
)

