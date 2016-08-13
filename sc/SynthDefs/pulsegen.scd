/*
 * A Complex pulse generator.
 * 6 (non-negative) pulse waves with variable frequencies are 
 * selectivly sent to one of two control output channels.
 * 
 * outbusZ   - Output control bus for Z channel
 * outbusY   - Output control bus for Y channel
 * clockFreq - Reference frequency ibn Hertz
 * ratioA    - Pulse A frequency ratio relative to clockFreq
 * ratioB    -
 * ratioC    -
 * ratioD    -
 * ratioE    -
 * ratioF    -
 * yAmpA     - Pulse A amplitude on Y channel
 * yAmpB     -
 * yAmpC     -
 * yAmpD     -
 * yAmpE     -
 * yAmpF     -
 * yLag      - Y channel lag time (0..1)
 * yScale    - Y channel scale factor
 * yBias     - Y channel bias offset
 * zAmpA     - Z channel parameters identical to channel Y.
 * zAmpB     -
 * zAmpC     -
 * zAmpD     -
 * zAmpE     -
 * zAmpF     -
 * zLag      -
 * zScale    -
 * zBias     -
*/


(SynthDef(\PulseGen, {
	|outbusZ = 1024,
	outbusY = 1023,
	clockFreq = 1.0,
	ratioA = 1.0,
	ratioB = 2.0,
	ratioC = 3.0,
	ratioD = 4.0,
	ratioE = 5.0,
	ratioF = 6.0,
	yAmpA = 1.0,
	yAmpB = 1.0,
	yAmpC = 1.0,
	yAmpD = 0.0,
	yAmpE = 0.0,
	yAmpF = 0.0,
	yLag = 0.0,
	yScale = 1.0,
	yBias = 0.0
	zAmpA = 0.0,
	zAmpB = 0.0,
	zAmpC = 0.0,
	zAmpD = 1.0,
	zAmpE = 1.0,
	zAmpF = 1.0,
	zLag = 0.0,
	zScale = 1.0,
	zBias = 0.0|
	var farray = [ratioA, ratioB, ratioC, ratioD, ratioE, ratioF]*clockFreq;
	var yarray = [yAmpA, yAmpB, yAmpC, yAmpD, yAmpE, yAmpF] * yScale + yBias;
	var zarray = [zAmpA, zAmpB, zAmpC, zAmpD, zAmpE, zAmpF] * zScale + zBias;
	var parray = LFPulse.kr(farray, 0, 0.5);
	var ysig = Lag3.kr(Mix.kr(parray * yarray * yScale + yBias), yLag.linlin(0,1,0,0.3));
	var zsig = Lag3.kr(Mix.kr(parray * zarray * zScale + zBias), zLag.linlin(0,1,0,0.3));
	Out.kr(outbusY, ysig);
	Out.kr(outbusZ, zsig);
}).load)

