/*
** Defines Envgen synth
*/

(SynthDef (\Envgen,
   {|outbusA = 1024
		outbusB = 1024
		gate = 0
		aAttack = 0.0
		aDecay1 = 0.0
		aDecay2 = 0.0
		aRelease = 0.0
		aBreakpoint = 1.0
		aSustain = 1.0
		aEnvmode = 0         // 0 -> gate  1 -> triggerd
		aInvert = 0          // 0 -> normal 1 -> inverted
		bAttack = 0.0
		bDecay1 = 0.0
		bDecay2 = 0.0
		bRelease = 0.0
		bBreakpoint = 1.0
		bSustain = 1.0
		bEnvmode = 0         // 0 -> gate  1 -> triggerd
		bInvert = 0|         // 0 -> normal 1 -> inverted
		var aGate = Select.kr(aEnvmode,[gate,Trig1.kr(gate,(aAttack+aDecay1+aDecay2))]);
		var a0 = EnvGen.kr(Env([0,1,aBreakpoint,aSustain,0],[aAttack,aDecay1,aDecay2,aRelease],\lin,3),aGate);
		var ai = (-1*a0)+1;
		var a = Select.kr(aInvert,[a0,ai]);
		var bGate = Select.kr(bEnvmode,[gate,Trig1.kr(gate,(bAttack+bDecay1+bDecay2))]);
		var b0 = EnvGen.kr(Env([0,1,bBreakpoint,bSustain,0],[bAttack,bDecay1,bDecay2,bRelease],\lin,3),bGate);
		var bi = (-1*b0)+1;
		var b = Select.kr(bInvert,[b0,bi]);
		Out.kr(outbusA,a);
		Out.kr(outbusB,b);
}).load)