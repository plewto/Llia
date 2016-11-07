/*
** rotate.sc 2016.09.05
**
** Defines PolyRoate key mode where a fixed number of synth voices
** are used in strict rotation.
**
** Pros:
**   - Simple, only slightly more complex then Poly1
**   - Fast, all synths are created ahead of time.
**   - Resource load is fixed. For complex synths, particularly 
**     ones with long release times, the total load can be significantly
**     less then Poly1.
**   - Portamento works (in a fashion)
**
** Cons:
**   - Fixed number of voices. If key-down count exceeds voice count, 
**     a playing note will be dropped to service the new note.
**
*/

PolyRotate : Keymode {

	var voiceCount;
	var synths;
	var voicePointer;
	var keyStates;

	*new {|lliaApp, synthType, oscid=nil, globalID="llia", vcount=8|
		^super.new().init(lliaApp, synthType, oscid, globalID, vcount);
	}

	init {|lliaApp, synthType, oscid=nil, globalID="llia", vcount=8|
		super.init(lliaApp, synthType, oscid, globalID);
		voiceCount = vcount;
		synths = Array.newClear(vcount);
		voicePointer = 0;
		keyStates = Array.newClear(128);
		vcount.do({|n|
			var sy = Synth(synthType, [\doneAction, 0, \gate, 0]);
			synths.put(n, sy);
		});
	}

	free {
		synths.do({|s| s.free});
		super.free;
		keyStates = Array.newClear(128);
	}

	set_ {|param, value|
		synths.do({|sy|
			sy.set(param, value);
		});
	}

	// setBusParameters {|param, rate, busName, offset=0|
	// 	var index = super.setBusParameters(param,rate,busName,offset);
	// 	this.set_(param.asSymbol,index);
	// 	^index;
	// }
		
	noteOn {|keynumber, frequency, velocity|
		var ptr, sy, old;
		old = keyStates.at(keynumber);
		if(old != nil,
			{
				sy = synths.at[old];
				sy.set(\gate, 0);
				keyStates.put(keynumber, nil);
			});
		ptr = voicePointer;
		voicePointer = (voicePointer + 1).wrap(0, voiceCount-1);
		sy = synths.at(ptr);
		sy.set(\gate, 0);
		sy.set(\keynumber, keynumber);
		sy.set(\velocity, velocity);
		sy.set(\freq, frequency);
		sy.set(\gate, 1);
		keyStates.put(keynumber, ptr);
	}
		
	noteOff {|keynumber|
		var sy;
		var ptr = keyStates.at(keynumber);
		
		if( ptr != nil,
			{
				sy = synths.at(ptr);
				sy.set(\gate, 0);
				keyStates.put(keynumber, nil);
			});
	}
	
}
		