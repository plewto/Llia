




(SynthDef (\Cascade, {
	|clkin = 1023          // External clock input
	xgate = 1023           // External gate input
	outbus = 1024          // Main out bus
	out1 = 1024            // out div 1
	out2 = 1024            // out div 2
	out3 = 1024            // out div 3
	out4 = 1024            // out div 4
	out5 = 1024            // out div 5
	out6 = 1024            // out div 6
	outn = 1024            // out div n
	clkfreq = 1.000        // internal clock frequency
	clksrc = 0             // 0 = internal 1 = external
	hold = 1.0             // trigger hod time (scaled by quotient)
	n = 8                  // general quotient
	amp1 = 1.000
	amp2 = 0.500
	amp3 = 0.333
	amp4 = 0.250
	amp5 = 0.200
	amp6 = 0.167
	ampn = 0.125
	gate1 = 0              // 0 = not gated, 1 = gated
	gate2 = 0
	gate3 = 0
	gate4 = 0
	gate5 = 0
	gate6 = 0
	gaten = 0
	scale = 1.0           // main out scale
	bias = 0.0            // main out bias
	lag = 0.0 |           // main out lag (normalized)
	var iclk = LFPulse.kr(clkfreq);
	var clock = Select.kr(clksrc,[iclk,In.kr(clkin)]);
	var pArray = PulseDivider.kr(clock,[1,2,3,4,5,6,n]);
	var tArray = (Trig.kr(pArray,[1,2,3,4,5,6,n]*hold)*2)-1;
	var gArray = tArray*In.kr(xgate);      // externallay gatted version of TArray
	var ampArray = [amp1,amp2,amp3,amp4,amp5,amp6,ampn];
	var uArray = Select.kr([gate1,gate2,gate3,gate4,gate5,gate6,gaten],[tArray,gArray])*ampArray;
	var mixed = (Mix.kr(uArray)*scale)+bias;
	var outsig = Lag2.kr(mixed,lag.linlin(0,1,0,0.1));
	Out.kr(out1, tArray[0]);
	Out.kr(out2, tArray[1]);
	Out.kr(out3, tArray[2]);
	Out.kr(out4, tArray[3]);
	Out.kr(out5, tArray[4]);
	Out.kr(out6, tArray[5]);
	Out.kr(outn, tArray[6]);
	Out.kr(outbus,outsig);
}).load;
)











	