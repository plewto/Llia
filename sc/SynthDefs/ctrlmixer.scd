/*
 * Control mixer
*/


(SynthDef (\ControlMixer, {
	|inbusA = 1024
	inbusB = 1024
	inbusC = 1024
	inbusD = 1024
	outbus = 1023
	scaleA = 1.0
	biasA = 0.0
	muteA = 0        // 0 -> enable   1 -> mute
	scaleB = 1.0
	biasB = 0.0
	muteB = 0
	scaleC = 1.0
	biasC = 0.0
	muteC = 0
	scaleD = 1.0
	biasD = 0.0
	muteD = 0
	masterScale = 1.0
	masterBias = 0.0
	masterMute = 0|
	var scaleArray = [scaleA,scaleB,scaleC,scaleD];
	var biasArray = [biasA,biasB,biasC,biasD];
	var inputs  = In.kr([inbusA,inbusB,inbusC,inbusD],1)*scaleArray+biasArray;
	var a = Select.kr(muteA, [inputs[0],0]);
	var b = Select.kr(muteB, [inputs[1],0]);
	var c = Select.kr(muteC, [inputs[2],0]);
	var d = Select.kr(muteD, [inputs[3],0]);
	var mixed = Select.kr(masterMute, [(a+b+c+d)*masterScale+masterBias, 0]);
	Out.kr(outbus,mixed);
}).load)


