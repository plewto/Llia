/*
** efxkeymode.sc   2016.04.19
** 
** A special 'keymode' for use with effects.
**
*/

EfxKeymode : Keymode {

	var activeVoice;
	var keyDownCounter;

	*new {|lliaApp, synthType, id, globalID, inbus, outbus|
		^super.new().init(synthType, id, globalID);
	}

	init {|lliaApp, synthType, id, globalID, inbus, outbus|
		super.init(lliaApp, synthType, id, globalID);
		activeVoice = Synth(synthType, [\gate, 0, \doneAction, 0, 
			\inbus, inbus, \outbus, outbus]);
		keyDownCounter = 0;
	}

	free {
		activeVoice.free;
		super.free;
	}

	set_ {|param, value|
		activeVoice.set(param, value);
	}

	noteOn {|keynumber, frequency, velocity|
		activeVoice.set(\gate, 1, \freq, frequency, \keynumber, keynumber,
		\velocity, velocity);
		keyDownCounter = keyDownCounter - 1;
	}

	noteOff {|keynumber|
		keyDownCounter = (keyDownCounter-1).max(0);
		if(keyDownCounter == 0,
			{
				activeVoice.set(\gate, 0);
			});
	}
}
		
		
		
			