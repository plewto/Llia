/*
 * SuperCollider Test Tones
 *
 * A440
 * PulseTone
 * SimpleSynth
 * BufferSynth
*/


/*
 * A440
 * Generates simple 2-channel sine wave.
*/
(SynthDef (\A440,
    {|freq = 440,
		gate = 1,
		amp = 0.1,
		outbus = 0,
		pan = 0.0|

		var sig = SinOsc.ar(freq)*amp*gate;
		sig = Pan2.ar(sig, pan);
		Out.ar(outbus, sig);
	}).send;
)


/*
 * Produces a pulsed sine wave.
*/
(SynthDef (\PulseTone,
    {|freq = 440,
		gate = 1,
		amp = 0.1,
		outbus = 0,
		pan = 0.0,
		pulseFreq = 1.0,
		pulseWidth = 0.5|

		var psig = LFPulse.kr(pulseFreq,0,pulseWidth);
		var sig = SinOsc.ar(freq)*psig*amp*gate;
		sig = Pan2.ar(sig, pan);
		Out.ar(outbus, sig);
	}).send;
)


/*
 * About as simple as it gets.
 * Single sawtooth osc with vibrato and detune
 * 3-stage ASR stye envelope
*/
(SynthDef (\SimpleSynth,
    {|freq = 440,
		detune = 1.0,
		gate = 1,
		doneAction = 2,
		outbus = 0,
		pan = 0.0,
		amp = 0.1,
		vibFreq = 5.0,
		vibrato = 0.0,
		attack = 0.01,
		release = 0.01|
		var env = EnvGen.kr(Env([0, 1, 0],[attack, release], \linear, 1),gate, doneAction);
		var vsens = 0.01;   // vibrato sensitivity
		var vibsig = LFTri.kr(vibFreq)*vsens*vibrato;
		var f = freq*detune*(1 + vibsig);
		var saw = Saw.ar(f)*env*amp;
		var sig = Pan2.ar(saw, pan);
		Out.ar(outbus, sig);
	}).send;
)


/*
 * Create a few test buffers
 *
*/

(
~sine.free;
~sine = Buffer.alloc(nil, 1024);
~sine.sine1([1.0]);
["Buffer ~sine   ", ~sine.bufnum].postln;


~saw.free;
~saw = Buffer.alloc(nil, 1024);
~saw.sine1([1.0, 0.5, 0.3, 0.25, 0.2, 0.17, 0.14, 0.13]);
["Buffer ~saw    ", ~saw.bufnum].postln;

~square.free;
~square = Buffer.alloc(nil, 1024);
~square.sine1([1.0, 0.0, 0.3, 0.0, 0.2, 0.0, 0.14, 0.0, 0.1]);
["Buffer ~square ", ~square.bufnum].postln;

~highpass.free;
~highpass = Buffer.alloc(nil, 1024);
~highpass.sine1([0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.2, 0.2, 0.2]);
["Buffer ~highpass ", ~highpass.bufnum].postln;
nil;
)


/*
 * Play simple wavetable buffer
*/
(SynthDef (\BufferTest1,
    {|freq = 440,
		gate = 1,
		doneAction = 2,
		outbus = 0,
		amp = 0.1,
		buffer = 1|
		var attack = 0.01;
		var release = 0.01;
		var env = EnvGen.kr(Env([0, 1, 0],[attack, release], \linear, 1),gate, doneAction);
		var sig = Osc.ar(buffer, freq)*amp*env;
		Out.ar(outbus, sig);
	}).send;
)

/*
 * Crossfade through buffers
*/

(SynthDef (\BufferTest2,
    {|freq = 440,
		gate = 1,
		doneAction = 2,
		outbus = 0,
		amp = 0.1,
		b1 = 0,
		b2 = 1,
		attack = 2.0,
		release = 2.0|
		var env1 = EnvGen.kr(Env([0, 1, 0],[0, release], \linear, 1),gate, doneAction);  // amp env
		var env2 = EnvGen.kr(Env([0, 1, 0],[attack, release], \linear, 1),gate, doneAction);  // crossfade env
		var scansig = env2.linlin(0, 1, b1, b2);
		var sig = VOsc.ar(scansig, freq)*amp*env1;
		Out.ar(outbus, sig);
	}).send;
)
		
		
		