

(SynthDef(\Mixer, {|
	inbus1 = 128,
	inbus2 = 128,
	inbus3 = 128,
	inbus4 = 128,
	outbusA = 0,
	outbusB = 1,
	gain1 = 1.0,
	pan1 = 0.0,
	reverb1 = 0.0,
	gain2 = 1.0,
	pan2 = 0.0,
	reverb2 = 0.0,
	gain3 = 1.0,
	pan3 = 0.0,
	reverb3 = 0.0,
	gain4 = 1.0,
	pan4 = 0.0,
	reverb4 = 0.0,
	reverbReturn = 0.0,
	reverbRoomSize = 0.25,
	reverbLowpass = 16000,   // Hertz
	reverbHighpass = 40,     // Hertz
	reverbBalance = 0.09,
	reverbDamp = 0.0
	mainAmpA = 1.0,
	mainAmpB = 1.0|
	var a = Pan2.ar(In.ar(inbus1)*gain1, pan1);
	var b = Pan2.ar(In.ar(inbus2)*gain2, pan2);
	var c = Pan2.ar(In.ar(inbus3)*gain3, pan3);
	var d = Pan2.ar(In.ar(inbus4)*gain4, pan4);
	var reverbIn = ((a*reverb1) + (b*reverb2) + (c*reverb3) + (d*reverb4));
	var reverbFilterIn = FreeVerb2.ar(reverbIn[0], reverbIn[1],1,
		reverbRoomSize,reverbDamp);
	var reverbFilterOut = LPF.ar(HPF.ar(reverbFilterIn,reverbHighpass),
		reverbLowpass) * reverbReturn;
	var reverb = Balance2.ar(reverbFilterOut[0], reverbFilterOut[1], reverbBalance);
	var outA = (a[0]+b[0]+c[0]+d[0]+reverb[0])*mainAmpA;
	var outB = (a[1]+b[1]+c[1]+d[1]+reverb[1])*mainAmpB;
	Out.ar(outbusA, outA);
	Out.ar(outbusB, outB);
}).load);


