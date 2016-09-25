/*
** A 4x2 mixer with optional external amplitude modulation.
** 
*/


(SynthDef (\Mixer, {
	|inbusA = 128
	inbusB = 128
	inbusC = 128
	inbusD = 128
	outbus1 = 0
	outbus2 = 0
	xbus = 1024
	gainA = 1.0
	muteA = 0     // 0 -> enable  1 -> mute
	modA = 0.0
	panA = 0.0
	gainB = 1.0
	muteB = 0
	modB = 0.0
	panB = 0.0
	gainC = 1.0
	muteC = 0
	modC = 0.0
	panC = 0.0
	gainD = 1.0
	muteD = 0
	modD = 0.0
	panD = 0.0
	gain1 = 1
	gain2 = 1|
	var a = In.ar(inbusA,1);
	var b = In.ar(inbusB,1);
	var c = In.ar(inbusC,1);
	var d = In.ar(inbusD,1);
	var x = In.kr(xbus);

	var amA = XFade2.kr(1,x,modA.linlin(0,1,-1,1));
	var amB = XFade2.kr(1,x,modB.linlin(0,1,-1,1));
	var amC = XFade2.kr(1,x,modC.linlin(0,1,-1,1));
	var amD = XFade2.kr(1,x,modD.linlin(0,1,-1,1));

	var ampA = gainA * muteA.linlin(0,1,1,0) * amA;
	var ampB = gainB * muteB.linlin(0,1,1,0) * amB;
	var ampC = gainC * muteC.linlin(0,1,1,0) * amC;
	var ampD = gainD * muteD.linlin(0,1,1,0) * amD;
	var out1, out2;

	a = Pan2.ar(a*ampA,panA);
	b = Pan2.ar(b*ampB,panB);
	c = Pan2.ar(c*ampC,panC);
	d = Pan2.ar(d*ampD,panD);

	out1 = (a[0]+b[0]+c[0]+d[0])*gain1;
	out2 = (a[1]+b[1]+c[1]+d[1])*gain2;
	Out.ar(outbus1, out1);
	Out.ar(outbus2, out2)
}).load)
