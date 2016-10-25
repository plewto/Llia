/*
 * Control signal processor
 */

(SynthDef (\Ghostbus, {
	|inbus = 1024
	outbus = 1023
	xbus = 1023
	enableMod = 0            // 0 -> no   1 -> yes
	enableHpA = 0
	lagA = 0.0
	scaleA = 1.0
	biasA = 0.0
	delay = 1.0
	feedback = 0.0
	lagDelay = 0.0
	enableHpDelay = 0
	scaleDelay = 1.0
	biasDelay = 0.0|
	var cutoff = 1;
	var maxdelay = 4;
	var src = In.kr(inbus);
	var x = In.kr(xbus);
	var a1 = Select.kr(enableMod, [src,x*src]);
	var a2 = Select.kr(enableHpA, [a1,HPF.kr(a1,cutoff)]);
	var a3 = Lag2.kr(a2, lagA.linlin(0,1,0.0,0.2));
	var fb = LocalIn.kr(1)*feedback;
	var d1 = DelayL.kr(a1+fb,maxdelay,delay.min(maxdelay).max(0));
	var d2 = Select.kr(enableHpDelay, [d1, HPF.kr(d1, cutoff)]);
	var d3 = Lag2.kr(d2, lagDelay.linlin(0,1,0.0,0.2));
	LocalOut.kr([d1]);
	a3 = (a3*scaleA)+biasA;
	d3 = (d3*scaleDelay)+biasDelay;
	Out.kr(outbus, a3+d3);
}).load)



