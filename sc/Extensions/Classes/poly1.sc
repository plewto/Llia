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
*/

Poly1 : Keymode {

	var activeNotes;

	*new {|lliaApp, synthType, oscid=nil, globalID="llia"|
		^super.new().init(lliaApp, synthType, oscid, globalID);
	}

	init {|lliaApp, synthType, oscid=nil, globalID="llia"|
		super.init(lliaApp, synthType, oscid, globalID);
		activeNotes = Array.newClear(128);
	}

	free {
		activeNotes.do({|v| v.free});
		super.free;
	}

	set_ {|param, value|
		super.set_(param, value);
		activeNotes.do({|v| v.set(param, value)});
	}

	noteOn {|keynumber, frequency, velocity|
		var params, sy, old;
		params = [\gate, 0, \freq, frequency, \keynumber, keynumber];
		params = super.mergeParameters(params);
		sy = Synth(synthType, params);
		old = activeNotes[keynumber];
		sy.set(\gate, 1);
		old.set(\gate, 0);
		activeNotes[keynumber] = sy;
	}

	noteOff {|keynumber|
		activeNotes[keynumber].set(\gate, 0);
		activeNotes[keynumber] = nil;
	}

}
		
