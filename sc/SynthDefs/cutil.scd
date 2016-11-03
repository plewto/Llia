/*
** Defines CUtil synth
*/

(SynthDef (\CUtil, {
	|outbus = 1024
	inbus = 1023
	wave = 0			      // [0,1,2] -> [None,abs,cube]
	polarityComp = 0          // [0,1,2] ->[none,pos->bi,bi->pos]
	clipMin = -1.0            // minimum
	clipMax = 1.0             // maximum
	lag = 0.0
	scale = 1.0
	bias = 0|
	var a0 = In.kr(inbus,1);
	var a1 = a0.abs;
	var a2 = a0.cubed;
	var b0 = Select.kr(wave,[a0,a1,a2]);
	var b1 = b0*2-1;
	var b2 = b0+1*0.5;
	var b = Select.kr(polarityComp,[b0,b1,b2]);
	var clipout = b.min(clipMax).max(clipMin);
	var lagout = Lag2.kr(clipout,lag);
	var outsig = lagout*scale+bias;
	Out.kr(outbus, outsig);
}).load)
