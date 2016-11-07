/*
** polyn.sc 2016.11.07
**
** Defines Polyn keymode with a fixed number of active voices.
** 
** Pros:
**   - Fixed resource load
**   - Fast, voices are allocated ahead of time, no need to 
**     create complex synths on the fly.
**
** Cons:
**   - limited polphony
**
*/

PolyN : Keymode {

	var voiceCount;     // int
	var synths;         // array
    var keymap;         // array keynumber -> synth pointer
	var freeSynths;     // queue
	var busySynths;     // queue

	*new {|lliaApp,synthType,oscid=nil,globalID="llia",vcount=8|
		^super.new().init(lliaApp,synthType,oscid,globalID,vcount);
	}

	init {|lliaApp, synthType, oscid=nil, globalID="llia",vcount=8|
		super.init(lliaApp,synthType,oscid,globalID);
		voiceCount = vcount;
		synths = Array.newClear(vcount);
		keymap = Array.newClear(128);
		freeSynths = Queue.new();
		busySynths = Queue.new();
		vcount.do({|n|
			var sy = Synth(synthType, [\doneAction, 0, \gate, 0]);
			synths.put(n,sy);
			freeSynths.push(n);
		});
	}

	free {
		synths.do({|s| s.free});
		super.free;
	}

	set_ {|param, value|
		synths.do({|sy|
			sy.set(param,value);
		});
	}

	
	noteOn {|keynumber, frequency, velocity|
		var ptr,sy;
		ptr = keymap.at(keynumber);
		if(ptr == nil,
			{
				if(freeSynths.depth > 0,
					{
						ptr = freeSynths.pop;
					},{
						ptr = busySynths.pop;
					});
				keymap.put(keynumber,ptr);
				busySynths.push(ptr);
				sy = synths.at(ptr);
				sy.set(\gate, 0);
				sy.set(\keynumber, keynumber, \velocity, velocity,
					\freq, frequency, \gate, 1);
			});
	}

	noteOff {|keynumber|
		var sy;
		var ptr = keymap.at(keynumber);
		if(ptr != nil,
			{
				sy = synths.at(ptr);
				busySynths.pop(ptr);
				freeSynths.push(ptr);
				keymap.put(keynumber, nil);
				sy.set(\gate, 0);
			});
	}

}
				
