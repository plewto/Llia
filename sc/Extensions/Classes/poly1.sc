/*
** poly1.sc 2016.02.21
**
** Defines Poly1 keyboard mode
**
** Pros:
**    - Simple
**    - Unlimited polyphony
**
** Cons: 
**    - May not be fast enough for some complex instruments.
**    - Effects which require continuity between voices, such as
**      portamento are not supported. 
**    - Complex synths with long decays may consume too many
**      resources.
*/

Poly1 : Keymode {

	var activeNotes;
	
	*new {|lliaApp, synthType, oscid=nil, globalID="llia"|
		^super.new().init(lliaApp, synthType, oscid, globalID);
	}

	init {|lliaApp, synthType, oscid=nil, globalID="llia"|
		super.init(lliaApp, synthType, oscid, globalID);
		activeNotes = Array.newClear(128);
		128.do({|i|
			activeNotes.put(i, LinkedList.new())});
	}

	free {
		activeNotes.do({|ll|
			ll.do({|v| v.free})});
		super.free;
	}

	set_ {|param, value|
		super.set_(param, value);
		//activeNotes.do({|v| v.set(param, value)});
	}

	noteOn {|keynumber, frequency, velocity|
		var params, sy, old;
		params = [\gate, 0, \freq, frequency, \keynumber, keynumber, \velocity, velocity, \doneAction, 2];
		params = super.mergeParameters(params);
		sy = Synth(synthType, params);
		sy.set(\gate, 1);
		activeNotes[keynumber].add(sy);
	}

	noteOff {|keynumber|
		var sy;
		sy = activeNotes[keynumber].popFirst;
		sy.set(\gate, 0);
	}
	
}
		
