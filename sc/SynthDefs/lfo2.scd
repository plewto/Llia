/*
 * A "gated" LFO using 3 internal oscillators:
 *   - clock
 *   - sawtooth
 *   - pulse
 * The sawtooth and pulse waves are optionally gated by the clock signal.
 *
 * outbusSaw           - 
 * outbusPulse         -
 * clkFreq             - clock frequency in Hz.
 * clkPw               - clock pulse width
 * clkAmp              - clock signal amp (applies to output bus only)
 * sawRatio            - saw frequency ratio relative to clock
 * sawSlew             - saw wave shape, 0.0 -> saw,  0.5 -> tri, 1.0 -> +saw
 * sawAmp              - saw wave amplitude
 * sawBleed            - saw wave gate bleed, 0.0 -> gated, 1.0 -> continuous
 * pulseRatio          - pulse wave frequency ratio relative to clock
 * pulseWidth          - 
 * pulseAmp            -
 * pulseBleed          -
 * lag                 - 
 * sawBias             - fixed value added to saw wave
 * pulseBias           - 
 *
 * The gated saw and pulse waves have opposite gate senses. When used
 * together the output alternates between saw and pulse.
*/ 
 
(
SynthDef (\LFO2, {
	|outbusSaw = 1024,
	outbusPulse = 1024,
	clkFreq = 1.00, 
	clkPw = 0.5,    
	clkAmp = 1.0,   
	sawRatio = 4.00,
	sawSlew = 0.0,  
	sawAmp = 1.0,   
	sawBleed = 0.0, 
	pulseRatio = 4.00,
	pulseWidth = 0.5,
	pulseAmp = 1.0,
	pulseBleed = 0.0,
	lag = 0.0,
	sawBias = 0,
	pulseBias = 0|
	var clk = LFPulse.kr(clkFreq, 0, clkPw);
	var sawGate = XFade2.kr(clk,1,sawBleed.linlin(0,1,-1,1));
	var saw = VarSaw.kr(clkFreq*sawRatio,0, sawSlew, sawGate*sawAmp);
	var pclk = -1*(clk-1);
	var pulseGate = XFade2.kr(pclk, 1,pulseBleed.linlin(0,1,-1,1));
	var pulse = LFPulse.kr(clkFreq*pulseRatio,0,pulseWidth,pulseGate*pulseAmp);
	lag = lag.linlin(0,1,0,0.15);
	saw = Lag2.kr(saw, lag);
	pulse = Lag2.kr(pulse, lag);
	Out.kr(outbusSaw, saw+sawBias);
	Out.kr(outbusPulse, pulse+pulseBias);
}).load;
)


