/*
** M, a Subtractive synth with esoteric tone generators.
** A - Pulse divider
** B - Buzz (Blip)
** C - Delay line
*/

(SynthDef (\M,
   {|
        outbus1 = 0
		outbus2 = 0
        xbus = 1024
        gate = 1
        doneAction = 2
        freq = 440
        port = 0.0
        keynumber = 60
	    amp = 0.1
        detune = 1.0
		vfreq = 5.00             // Primary (vibrato) LFO frequency
        vdelay = 0.0             //    all other LFO frequencies relative to vfreq
        vsens = 0.1              // vibrato sensitivity
        vdepth = 0.0             // programmed vibrato depth
		xPitch = 0.0             // external -> pitch
		tremoloLag = 0.1         // Common lag applied to A,B|C tremolo LFOs
        /* A Pulse Divider */
        aAttack = 0.0
        aDecay1 = 0.0
        aDecay2 = 0.0
        aRelease = 0.0
        aBreakpoint = 1.0
        aSustain = 1.0
        aTrigMode = 0            // 0 env gate, 1 env trig
        aLfoRatio = 1.0
        aLfoDelay = 0.0
        aRatio = 1.0             // A Freq relative to freq
        aKey = 60                // Keyscale ref MID keynumber
        aKeyscaleLeft = 0        // db/octave
        aKeyscaleRight = 0       // db/octave
        aQuotient = 1            // pulse divider quotient
        aQLfo = 0                // LFO -> divider quotient
        aQEnv = 0                // Env -> divider quotient
        aQExternal = 0           // external -> divider quotient
        aPulseWidth = 0.5        // divider output width (may be greater then 1)
        aPwmLfo = 0.0            // LFO -> pw
        aPwmEnv = 0.0            // env -> pw
        aPwmExternal = 0.0       // external -> pw
		aClkMix = 0.0            // mix clk source with divider signal (0,1)
		aLfo = 0.0               // lfo -> a amp
		aEnvPitch = 0.0          // env -> pitch bend
        /* B Dual Buzz */
        bAttack = 0.0
        bDecay1 = 0.0
        bDecay2 = 0.0
        bRelease = 0.0
        bBreakpoint = 1.0
        bSustain = 1.0
        bTrigMode = 0
        bLfoRatio = 1.0
        bLfoDelay = 0.0
        bRatio1 = 1.0            // Freq ratio 1
        bRatio2 = 1.0            // Freq ratio 2
        bKey = 60
        bKeyscaleLeft = 0
        bKeyscaleRight = 0
        bN1 = 32                // harmonic count 1 ( > 0)
        bN2 = 24                // harmonic count 2 ( > 0)
        bNLfo = 0               // LFO -> harmonic count (n1 & n2)
        bNEnv = 0               // Env -> harmonic count (n1 & n2)
		bNExternal = 0          // External -> harmonic count (n1 & n2)
        bN2Lag = 0.0            // lag time n2 LFO and Env
		b2Polarity = 1          // -1|+1
		bLfo = 0.0              // lfo -> b amp
		bEnvPitch = 0            // env -> pitch bend
		/* Noise */
		noiseLP = 16000          // Noise static lowpass cutoff (Hz)
		noiseHP = 10             // Noise static highpass cutoff (Hz)
		noiseLfo = 0.0           // LFO B -> noise amp
		noiseLag = 0.0
		/* C Delay Line */
		cAttack = 0.0
		cDecay1 = 0.0
		cDecay2 = 0.0
		cRelease = 0.0
		cBreakpoint = 1.0
		cSustain = 1.0
		cTrigMode = 0
		cLfoRatio = 1.0
		cLfoDelay = 0.0
		cRatio = 1.0             // Delay line tuning
		cKey = 60
		cKeyscaleLeft = 0
		cKeyscaleRight = 0
		cFb = -1                 // feedback -1, 0, +1
		cPulseRatio = 1.0        // incite pulse freq ratio
		cPw = 0.5                // incite pulse width
		cPulseRatioLfo = 0.0      // LFO -> incite pulse frequency
		cPulseRatioEnv = 0.0     // env -> incite pulse frequency
		cPulseRatioExternal =0.0 // external -> incite pulse frequency
		cPwmLfo = 0.0            // LFO -> incite pulse width
		cPwmEnv = 0.0            // env -> incite pulse width
		cPwmExternal = 0.0       // external -> incite pulse width
		cInciteSelect = -1       // -1 -> pulse   +1 -> Noise
		cLfo = 0.0               // lfo -> c amp
		cEnvPitch = 0
		/* Filter input mixer */
		aAmp = 0.333
		bAmp = 0.333
		cAmp = 0.333
		noiseAmp = 0.00
		aFilter = -1             // -1 -> lowpass   +1 -> bandpass
		bFilter = -1
		cFilter = -1
		noiseFilter = -1
		/* Filter 1 (Lowpass)
		 * LFOA, LFOB, ENVA, ENVB
		*/
		f1Freq = 16000           // static cutoff in Hz
		f1Keytrack = 0           // key -> cutoff  (0,0.5,1,1.5,2)
		f1Res = 0.0              // resonace (0..1)
		f1FreqLfoA = 0           // LFO A -> freq
		f1FreqEnvA = 0           // env A -> freq
		f1FreqLfoB = 0           // LFO B -> freq
		f1FreqEnvB = 0           // env B -> freq
		f1FreqExternal = 0       // external -> freq
		f1Pan = 0                // Output pan (-1,+1)
		/* Filter 2 (bandpass)
		 * LFOB, LFOC, ENVB, ENVC
		*/
		f2Freq = 400
		f2Keytrack = 0
		f2Res = 0.0
		f2FreqLfoB = 0
		f2FreqEnvB = 0
		f2FreqLfoC = 0
		f2FreqEnvC = 0
		f2FreqExternal = 0
		f2Pan = 0
		|
		var x = In.kr(xbus);
		var holdtime = max(cRelease,max(aRelease,bRelease));
		/* lfo array 0->A  1->B  2->C  3->Vibrato */
		var lfoEnv = EnvGen.kr(Env([0,0,1,1],
			[[aLfoDelay,bLfoDelay,cLfoDelay,vdelay],[aLfoDelay,bLfoDelay,cLfoDelay,vdelay],holdtime],\lin,3),gate);
		var lfo = LFCub.kr([vfreq*aLfoRatio, vfreq*bLfoRatio, vfreq*cLfoRatio, vfreq])*lfoEnv;
		var envGate = Select.kr([aTrigMode,bTrigMode,cTrigMode],
			[gate, Trig.kr(gate, [(aAttack+aDecay1+aDecay2),(bAttack+bDecay1+bDecay2),(cAttack+cDecay1+cDecay2)])]);
		var env_floor = 0.01;
		var env = EnvGen.kr(Env([env_floor,1,[aBreakpoint,bBreakpoint,cBreakpoint].max(env_floor),[aSustain,bSustain,cSustain].max(env_floor),env_floor],
			[[aAttack,bAttack,cAttack],[aDecay1,bDecay1,cDecay1],[aDecay2,bDecay2,cDecay2],[aRelease,bRelease,cRelease]],-4,3), envGate)-env_floor;
		var f0 = Lag2.kr(freq,port)*detune*(1+(vsens.linlin(0,1,0,0.2)*((vdepth*lfo[3]) + (x * xPitch))));
	    /* Key scales */
		var left_octave = ([aKey-keynumber,bKey-keynumber,cKey-keynumber]/12).max(0);
		var right_octave = ([keynumber-aKey,keynumber-bKey,keynumber-cKey]/12).max(0);
		var keyscale = dbamp(left_octave*[aKeyscaleLeft,bKeyscaleLeft,cKeyscaleLeft])+(right_octave*[aKeyscaleRight,bKeyscaleRight,cKeyscaleRight]);
		/* Tone A - Pulse Divider */
		var fa = f0*aRatio*(1 + (aEnvPitch * env[0]));
		var aClk = SinOsc.ar(fa);
		var aWidth = (aPulseWidth+(lfo[0]*aPwmLfo)+(env[0]*aPwmEnv)+(x*aPwmExternal)).abs;
		var aQuo = (aQuotient+(lfo[0]*aQLfo)+(env[0]*aQEnv)+(x*aQExternal)).max(0.1);
		var aPeriod = ((aQuo*aWidth)/fa).abs;
		var aPulse = Trig1.ar(PulseDivider.ar(aClk,aQuo),aPeriod);
		var asig_1 = XFade2.ar(aPulse,aClk,aClkMix.linlin(0,1,-1,1))*env[0]*keyscale[0];
		var asig = asig_1*LinXFade2.kr(1,Lag2.kr(lfo[0],tremoloLag),aLfo.linlin(0,1,-1,1));
		/* Tone B - dual blip */
		var bnmod = (lfo[1].abs*bNLfo)+(env[1]*bNEnv)+(x*bNExternal);
		var bn1 = bN1+bnmod;
		var bn2 = bN2+Lag2.kr(bnmod,bN2Lag);
		var bblip1 = Blip.ar(f0*bRatio1*(1+(bEnvPitch*env[1])),bn1);
		var bblip2 = Blip.ar(f0*bRatio2*(1+(bEnvPitch*env[1])),bn2,b2Polarity);
		var bsig_1 = (bblip1+bblip2)*env[1]*keyscale[1];
		var bsig = bsig_1*LinXFade2.kr(1,Lag2.kr(lfo[1],tremoloLag),bLfo.linlin(0,1,-1,1));
		/* Noise, shares env and LFO with B */
		var nsemod = Lag2.kr(env[1]+XFade2.kr(1,lfo[1],noiseLfo.linlin(0,1,-1,1)),noiseLag);
		var nse = LPF.ar(HPF.ar(WhiteNoise.ar(),noiseHP.max(10)),noiseLP.max(100))*nsemod*keyscale[1]*env[1];

		/* Tone C - delay line feedback */
		var cmaxdelay = 0.025;  // 40hz floor
		var fc = f0*cRatio*(1 + (cEnvPitch*env[2]));
		var clfo = lfo[2];
		var cenv = env[2];
		var cifreq = ((fc*cPulseRatio)*(1+(clfo *cPulseRatioLfo)+(cenv*cPulseRatioEnv)+(x*cPulseRatioExternal))).abs.min(16000);
		var ciwidth = (cPw+(clfo*cPwmLfo)+(cenv*cPwmEnv)+(x*cPwmExternal)).max(0.01).min(0.99);
		var cpulse = Pulse.ar(cifreq,ciwidth);
		var cincite = XFade2.ar(cpulse,PinkNoise.ar(),cInciteSelect);
		var cdlyin = cincite + LocalIn.ar(1);
		var cperiod = (1.0/fc).abs.min(cmaxdelay);
		var cdlyout = DelayC.ar(cdlyin,cmaxdelay,cperiod).clip(-1,1);
		var csig_1 = cdlyout*cenv*keyscale[2];
		var csig = csig_1*LinXFade2.kr(1,Lag2.kr(clfo,tremoloLag),cLfo.linlin(0,1,-1,1));

		/* Filter input mixer */
		var filterin = Pan2.ar(asig*aAmp,aFilter) + Pan2.ar(bsig*bAmp,bFilter) + Pan2.ar(csig*cAmp,cFilter) + Pan2.ar(nse*noiseAmp,noiseFilter);
		/* Lowpass filter */
		var lpfreq = f1Freq+(f0*f1Keytrack)+(lfo[0]*f1FreqLfoA)+(lfo[1]*f1FreqLfoB)+(env[0]*f1FreqEnvA)+(env[1]*f1FreqEnvB)+(x*f1FreqExternal);
		var lpgain = f1Res.linexp(0,1,0.5,3.99);
		var filter1 = MoogFF.ar(filterin[0],lpfreq.max(20).min(16000),lpgain);
		/* Bandpass filter */
		var bpfreq = f2Freq+(f0*f2Keytrack)+(lfo[1]*f2FreqLfoB)+(lfo[1]*f2FreqLfoC)+(env[1]*f2FreqEnvB)+(env[2]*f2FreqEnvC);
		var brq = f2Res.linexp(0,1,1,0.1);
		var filter2 = BPF.ar(filterin[1],bpfreq.max(20).min(16000),brq);
		var outsig = (Pan2.ar(filter1,f1Pan) + Pan2.ar(filter2,f2Pan))*amp;
		Linen.kr(gate,0.01,1, holdtime, doneAction);  // voice hold envelope
		LocalOut.ar(cdlyout*cFb);
		Out.ar([outbus1,outbus2],outsig);

}).load)

