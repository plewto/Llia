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

	var stack, keyMap, activeVoice;

	/*
     * keyMap maps MIDI key number to frequency.
     * The map is initially empty, as new key numbers are encountered, their 
     * frequencies are added to the map.  This information is used on keyUp 
     * events.  If there are keys still being help the synths frequency parameter
     * is updated with the frequency of the "freshest" held key.
    */

	
	*new {|lliaApp, synthType, oscid=nil, globalID="llia"|
		^super.new().init(lliaApp, synthType, oscid, globalID);
	}

	init {|lliaApp, synthType, oscid=nil, globalID="llia"|
		super.init(lliaApp, synthType, oscid, globalID);
		stack = Stack.new;
		keyMap = IdentityDictionary.new(32);
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
		keyMap.put(keynumber, frequency);
	}

	noteOff {|keynumber|
		stack.pop(keynumber);
		if(stack.isEmpty, {
			activeVoice.set(\gate, 0);
		},{
			var freq = keyMap.at(stack.top());
			activeVoice.set(\freq, freq);
		})
	}
	
}