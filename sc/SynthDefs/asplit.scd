/*
** An audio signal splitter.
** Splits source audio signal to up to 4 buses with 
** gain and mute controls on each bus.
**
*/

(SynthDef (\ASplit, {
	|inbus = 0
	outbusA = 128
	outbusB = 128
	outbusC = 128
	outbusD = 128
	gainA = 1.0
	gainB = 1.0
	gainC = 1.0
	gainD = 1.0
	unmuteA = 1       // 0 -> mute   1 -> unmute
	unmuteB = 1
	unmuteC = 1
	unmuteD = 1
	gain = 1.0
	unmute = 1|
	var src = In.ar(inbus);
	var amp = gain * unmute;
	var a = src * gainA * unmuteA * amp;
	var b = src * gainB * unmuteB * amp;
	var c = src * gainC * unmuteC * amp;
	var d = src * gainD * unmuteD * amp;
	Out.ar(outbusA, a);
	Out.ar(outbusB, b);
	Out.ar(outbusC, c);
	Out.ar(outbusD, d);
}).load)
	