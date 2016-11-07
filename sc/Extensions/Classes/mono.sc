/*
** mono1.sc   2015.11.29
** changed gilrname to mono.sc 2016.11.07
*/


/*
** Mono1
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



/*
** MonoExclusive
**
** Highly limited keymode where only the inital keydown is articulated.
** Once a key is down, all additional keys are ignored until all
** keys are lifted.
**
** The intended use is for MonoExclusive to be layerd with some other,
** more typical, keymode to provide variation on the first notes played.
**
** A "real" world example is on antique electric organs where clicks 
** were produced only on the first key down.
*/

MonoExclusive : Keymode {

	var keyCount, keyHeld, activeVoice;

	*new {|lliaApp, synthType, oscid=nil, globalID="llia"|
		^super.new().init(lliaApp, synthType, oscid, globalID);
	}

	init {|lliaApp, synthType, oscid=nil, globalID="llia"|
		super.init(lliaApp, synthType, oscid, globalID);
		keyCount = 0;
		keyHeld = 0;
		activeVoice = Synth(synthType, [\gate, 0, \doneAction, 0]);
	}

	free {
		activeVoice.free;
		super.free;
	}

	set_ {|param, value|
		activeVoice.set(param,value);
	}

	noteOn {|keynumber, frequency, velocity|
		if(keyCount == 0,
			{
				var params;
				params = [\gate, 1, \freq, frequency, \keynumber, keynumber, \velocity, velocity];
				params = super.mergeParameters(params);
				Keymode.zip(params).do({|q|
					var param = q[0];
					var value = q[1];
					activeVoice.set(param, value)});
				keyCount = 1;
				keyHeld = keynumber;
			},{
				keyCount = keyCount+1;
			})
	}

	noteOff {|keynumber|
		if(keyHeld == keynumber, 
			{
				activeVoice.set(\gate, 0);
			});
		keyCount = (keyCount-1).max(0);
	}
}

	
		