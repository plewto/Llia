/*
 * Mus converts mouse events to control signals.
 * Provided signals:
 *     mouse x-coordinaet
 *     mouse y-coordinate
 *     mouse button state
 *     ADSR envelope triggerd on mouse button
 */ 

(SynthDef (\Mus, {|
	xbus = 1023,
	ybus = 1023,
	buttonBus = 1023,
	envBus = 1023,
	xmin = 0.0,
	xmax = 1.0,
	xcurve = 0,    // 0 -> linear   1 -> exponential
	xlag = 0.2,
	ymin = 0.0,
	ymax = 1.0,
	ycurve = 0,
	ylag = 0.2,
	buttonOff = 0.0,
	buttonOn = 1.0,
	attack = 0.0,
	decay = 0.0,
	sustain = 1.0,
	release = 1.0,
	envScale = 1.0,
	envBias = 0.0|
	var x = MouseX.kr(xmin, xmax, xcurve, xlag);
	var y = MouseY.kr(ymin,ymax,ycurve, ylag);
	var b = MouseButton.kr(buttonOff, buttonOn);
	var gate = MouseButton.kr(0, 1);
	var env = EnvGen.kr(Env.adsr(attack, decay, sustain, release,
			curve: \linear, bias: 0.000), gate, 1, 0, 1, 0);
	Out.kr(xbus, x);
	Out.kr(ybus, y);
	Out.kr(buttonBus, b);
	Out.kr(envBus, env*envScale+envBias);
}).load)



