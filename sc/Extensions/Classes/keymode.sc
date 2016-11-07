/*
** keymode.sc 2016.02.21
** 
*/

Keymode : Object {

	var lliaApp;
	var synthID;
	var <netAddress;
	var <synthType;
	var fixedParameters;
	var currentProgram;
	var oscHandlers;
	var <isDead;

	/* 
    ** Zip list into 2-element sublist
    ** zip([a,b,c,d,e,f]) --> [[a,b],[c,d],[e,f]]
	*/
	*zip {|lst|
		var acc = List.new;
		var i = 0;
		while ({i < lst.size},
			{
				var a, b;
				a = lst.at(i);
				b = lst.at(i+1);
				acc.add([a,b]);
				i = i+2;
			});
		^acc;
	}
	
	*new {
		^super.new;
	}

	init {|app, stype, sid|
		lliaApp = app;
		synthType = stype;
		synthID = sid;
		fixedParameters = IdentityDictionary.new();
		currentProgram = Program.new();
		oscHandlers = [];
		isDead = false;
		this.netAddress_("127.0.0.1", 57120);
	}
		
	netAddress_ {|addr="localhost", port=57120|
		netAddress = NetAddr.new(addr, port);
		this.initOSCFunctions;
	}

	path {|tail|
		var globalID, rs;
		globalID = lliaApp.oscID;
		rs = "/Llia/";
		rs = rs ++ globalID;
		rs = rs ++ "/" ++ synthType ++ "/" ++ synthID.asString;
		rs = rs ++ "/" ++ tail.asString;
		^rs;
	}

	initOSCFunctions {
		var ary;
		oscHandlers.do.free;
		ary = [

			OSCFunc({|msg|
				postf("PING Synth % %\n", synthType, synthID);
				lliaApp.respond("ping-response", "")},
				this.path("ping")),

			OSCFunc({|msg|
				this.reset()},
				this.path("reset")),

			OSCFunc({|msg|
				this.free},
				this.path("free")),

			OSCFunc({|msg|
				this.lliaDump},
				this.path("dump")),

			OSCFunc({|msg|
				var keynumber = msg[1];
				var frequency = msg[2];
				var velocity = msg[3];
				this.noteOn(keynumber, frequency, velocity)},
				this.path("note-on")),

			OSCFunc({|msg|
				var keynumber = msg[1];
				var velocity = msg[2];
				this.noteOff(keynumber, velocity)},
				this.path("note-off")),

			OSCFunc({|msg|
				this.allNotesOff()},
				this.path("all-notes-off")),

			OSCFunc({|msg|
				this.allNotesOff()},
				this.path("panic")),
			
			OSCFunc({|msg|
				var param = msg[1];
				var value = msg[2];
				this.set_(param, value)},
				this.path("synth-param")),
		];
		oscHandlers = ary;
	}


	free {
		isDead = true;
		oscHandlers.do({|h| h.free;})
	}
	
	synthParams {
		var plst = currentProgram.synthParams;
		^plst;
		//^(plst ++ fixedParameters);
	}

	allNotesOff {
		128.do{|kn| this.noteOff(kn, 0)};
	}

	reset {
		this.allNotesOff;
		currentProgram = Program.new();
	}

	set_ {|param, value|
		currentProgram.set_(param.asSymbol, value);
	}

	setBusParameter {|param, rate, busName, offset=0|
		var index;
		index = lliaApp.getBusIndex(rate, busName, offset);
		fixedParameters.put(param.asSymbol, index);
		this.set_(param.asSymbol, index);
		^index;
	}

	setBufferParameter {|param, bufferName|
		var buffer = lliaApp.getBuffer(bufferName);
		fixedParameters.put(param.asSymbol, buffer);
	}

	/*
     * Merge transient parameters from note-on event and currentProgram
     * with fixed parameters (mostly bus and buffer assignments).
     *
     * ARGS:     
     *    alist argument is associatein list from note-on event.
     *    [\gate, 1, \freq, n, \keynumber, n ...]
     *
     * RETURNS: merged parameter/value association liet
     *   [\param1, value1, \param2, value2, ...]
	*/
	mergeParameters {|alist|
		var alist1 = currentProgram.getPairs;
		var alist2 = fixedParameters.getPairs;
		^ alist ++ alist1 ++ alist2;
	}

		
	// Abstract method
	// velocity "normalized" [0.0, 1.0]
	noteOn {|keynumber, frequency, velocity|
	}

	// Abstract method
	noteOff {|keynumber|
	}

	lliaDump {|pad=""|
		postf("ISSUE: Fix me: Keymode.lliaDump\n");
	}
	

} // end class
		
		
	
	
	

