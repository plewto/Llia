/*
 * Three coupled LFOs (A, B & C)
 * A fourth LFO is used to modulate thenthree primary oscilators.
 * 
 * outbusA       - Each LFO sent to seperate output bus                                
 * outbusB       -                                  
 * outbusC       -                                  
 * gate          -                               
 * lfoScale      - Scale values applied to all primary LFOs                                  
 * lfoBias       - Bias value added to allprimary  LFOs                                 
 * lfoFreq       - Common frequency for primary LFOs                                        
 * lfoModFreq    - Frequency of modulatin LFO  (realtive to lfoFreq)                                  
 * lfoFM         - Modulation LFO -> Primary freq                               
 * lfoAM         - Modulation LFO -> primary amp                               
 * lfoEnvToFreq  - env -> primary freq                                      
 * lfoBleed      - env amplitude bleed, 0 -> apply env,  1 => disable env                                  
 * lfoDelay      - env onset delay in seconds                                  
 * lfoAttack     - env attack time after delay segment                                   
 * lfoHold       - env hold time after gate low                                 
 * lfoRelease    - env release time adfter hold segment                                    
 * lfoRatioA     - freq ratio LFO A                                   
 * lfoRatioB     - freq ratio LFO B                                   
 * lfoRatioC     - freq ratio LFO C                                   
 * lfoAmpA       - LFO A amp                                 
 * lfoAmpB       - LFO B amp                                 
 * lfoAmpC       - LFO C amp
 *
 * LFOs A, B and C have fixed phases relationship of 0, 120 and 240 degrees.                                 
*/


(
SynthDef (\LFO3, {
	|outbusA = 1024
	outbusB = 1024
	outbusC = 1024
	gate = 1
	lfoScale = 1.0
	lfoBias = 0
	lfoFreq = 1.0
	lfoModFreq = 1
	lfoFM = 0.0
	lfoAM = 0.0
	lfoEnvToFreq = 0.0
	lfoBleed = 1.0
	lfoDelay = 0.0
	lfoAttack = 0.0
	lfoHold = 1.0
	lfoRelease = 0.0
	lfoRatioA = 1.0
	lfoRatioB = 1.0
	lfoRatioC = 1.0
	lfoAmpA = 1.0
	lfoAmpB = 1.0
	lfoAmpC = 1.0|
	var env = EnvGen.kr(Env([0,0,1,1,0],[lfoDelay,lfoAttack,lfoHold,lfoRelease],
		\lin, 2) ,gate, doneAction: 0);
	var fmEnv = 1 + (lfoEnvToFreq * env);
	var ampEnv = XFade2.kr(env, 1, lfoBleed.linlin(0,1,-1,1));
	var modSig = SinOsc.kr(lfoModFreq*lfoFreq);
	var fmMod = 1 + (lfoFM * modSig);
	var ampMod = XFade2.kr(1, modSig, lfoAM.linlin(0,1,-1,1));
	var freq = lfoFreq * fmEnv * fmMod;
	var freqArray = [lfoRatioA, lfoRatioB, lfoRatioC] * freq;
	var phaseArray = [0.0, 2.094, 4.189]; // radians
	var ampArray = ([lfoAmpA, lfoAmpB, lfoAmpC] * ampMod) * ampEnv;
	var signals = (SinOsc.kr(freqArray, phaseArray, ampArray)*lfoScale)+lfoBias;
	Out.kr(outbusA, signals[0]);
	Out.kr(outbusB, signals[1]);
	Out.kr(outbusC, signals[2]);
}).load;
)


