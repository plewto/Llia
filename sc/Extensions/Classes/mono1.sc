/*
** mono1.sc   2015.11.29
**
** A monophonic MIDI event handler with last key priority.
** Mono1 keeps a single Synth active at all times.
**
** Pros:
**    - Fast
**    - Allows for effects which require synth persistence (such as portamento)
**    - Monophonic trills.
**
** Cons:
**    - Monophonic 
*/

Mono1 : Keymode {

	var stack, activeVoice;

	*new {|lliaApp, synthType, oscid=nil, globalID="llia"|
		^super.new().init(lliaApp, synthType, oscid, globalID);
	}

	init {|lliaApp, synthType, oscid=nil, globalID="llia"|
		super.init(lliaApp, synthType, oscid, globalID);
		stack = Stack.new;
		activeVoice = Synth(synthType, [\gate, 0, \doneAction, 0]);
	}
		
	free {
		activeVoice.free;
		super.free;
	}

	set_ {|param, value|
		activeVoice.set(param, value);
	}

	noteOn {|keynumber, frequency, velocity|
		var params;
		params = [\gate, 1, \freq, frequency, \keynumber, keynumber, \velocity, velocity];
		params = super.mergeParameters(params);
		Keymode.zip(params).do({|q|
			var param = q[0];
			var value = q[1];
			activeVoice.set(param, value)});
		stack.push(keynumber);
	}

	noteOff {|keynumber|
		stack.pop(keynumber);
		if(stack.isEmpty, {
			activeVoice.set(\gate, 0);
		});
		
	}
	
}