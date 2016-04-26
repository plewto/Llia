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

	*new {|synthType, oscid=nil, globalID="llia"|
		^super.new().init(synthType, oscid, globalID);
	}

	init {|synthType, oscid=nil, globalID="llia"|
		super.init(synthType, oscid, globalID);
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
		var paramlist = super.synthParams ++ [\gate, 0, \freq, frequency,
			\keynumber, keynumber, \outbus, super.outbus];
		var sy = Synth(synthType, paramlist);
		var old = activeNotes[keynumber];
		//postf("DEBUG Poly1 super.outbus --> %\n", super.outbus);
		sy.set(\gate, 1);
		old.set(\gate, 0);
		activeNotes[keynumber] = sy;
	}

	noteOff {|keynumber|
		activeNotes[keynumber].set(\gate, 0);
		activeNotes[keynumber] = nil;
	}

} // end Poly1
		
	
		
	