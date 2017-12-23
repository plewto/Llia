/*
** keymode.sc 2016.02.21
**
** The Keymode class is not used directly. Several classes extend Keymode
** to define specific key response.  At this time (2017.12.23) the
** following classes extend Keymode:
**
**    EfxKeymode
**    Mono1
**    MonoExclusive
**    Poly1
**    PolyN
**    Rotate
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

	/*
	** Construct OSC message path.
    ** ARGS:
    **   msg - String, message type
    **
    ** The resulting message has format:
    **
	**         /Llia/gid/stype/id/msg
    **
    ** Where:
    **    gid   - Is the global OSC ID 
    **    stype - Synth type
    **    id    - int synth serial number
    **    msg   - message type
	*/
	path {|msg|
		var globalID, rs;
		globalID = lliaApp.oscID;
		rs = "/Llia/";
		rs = rs ++ globalID;
		rs = rs ++ "/" ++ synthType ++ "/" ++ synthID.asString;
		rs = rs ++ "/" ++ msg.asString;
		^rs;
	}

	initOSCFunctions {
		var ary;
		oscHandlers.do.free;
		ary = [

			/*
            ** 'ping' 
            ** Diagnostic message to check connectivity to specific sid.
			*/
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

			/*
			** 'note-on' kn freq vel
            ** Turn note on.
            ** ARGS:
            **   kn   - int, MIDI keynumber.
            **   freq - float, frequency in Hz.
            **   vel  - float, normalized key velocity, 0 <= vel <= 1.
			*/	
			OSCFunc({|msg|
				var keynumber = msg[1];
				var frequency = msg[2];
				var velocity = msg[3];
				this.noteOn(keynumber, frequency, velocity)},
				this.path("note-on")),

			/*
            ** 'note-off' kn vel
            ** Turn note off.
            ** ARGS:
            **   kn  - MIDI key number
            **   vel - float, release velocity (not otherwise supported)
            */
			OSCFunc({|msg|
				var keynumber = msg[1];
				var velocity = msg[2];
				this.noteOff(keynumber, velocity)},
				this.path("note-off")),

			/*
            ** 'all-notes-off'
            */
			OSCFunc({|msg|
				this.allNotesOff()},
				this.path("all-notes-off")),
			/*
            ** 'panic' same as 'all-notes-off'
			*/
			OSCFunc({|msg|
				this.allNotesOff()},
				this.path("panic")),

			/*
            ** 'synth-param'  param value
		    ** Change synth parameter.
            ** ARGS:
			**	param - String, parameter name
            **  value - Float, new value.
            */
			OSCFunc({|msg|
				var param = msg[1];
				var value = msg[2];
				this.set_(param, value)},
				this.path("synth-param")),

			OSCFunc({|msg|
				var vindex = msg[1].asInt;
				var param = msg[2];
				var value = msg[3];
				this.set_voice_parameter_(vindex,param,value)},
				this.path("voice-param")),
		];
		oscHandlers = ary;
	}

	/*
	** Free all managed synths.
	*/
	free {
		isDead = true;
		oscHandlers.do({|h| h.free;})
	}

	/*
	** Returns a list of parameters.
    */
	synthParams {
		var plst = currentProgram.synthParams;
		^plst;
		//^(plst ++ fixedParameters);
	}

	/*
    ** Turn all notes off.
	*/
	allNotesOff {
		128.do{|kn| this.noteOff(kn, 0)};
	}

	/*
    ** Turn all notes off and initialize program.
    */
	reset {
		this.allNotesOff;
		currentProgram = Program.new();
	}

	/*
    ** Set synth parameter value.
    ** ARGS:
    **   param - String, parameter name
    **   value - float, new value
	*/
	set_ {|param, value|
		currentProgram.set_(param.asSymbol, value);
	}

	/*
    ** Set synth parameter for specific voice.
    ** ARGS:
    **   vindex - voice array index 
    **   param  - String, parameter name
    **   value  - float, 
    **
    ** Unless overridden set_voice_parameter  has the same effect as 
    ** calling set_ and ignoring the vindex argument.
    ** However set_voice_parameter should only be used with sub classes
    ** which implement it.  Calling the default implementation is 
    ** if highly inefficient.
    */
	set_voice_parameter_ {|vindex,param,value|
		this.set_(param,value)
	}
	
	/*
    ** Assign a bus number to synth parameter.
    ** Bus related parameters are not effected by program changes.
	*/
	setBusParameter {|param, rate, busName, offset=0|
		var index;
		index = lliaApp.getBusIndex(rate, busName, offset);
		fixedParameters.put(param.asSymbol, index);
		this.set_(param.asSymbol, index);
		^index;
	}

	/*
    ** Assign buffer number to synth parameter.
	*/
	setBufferParameter {|param, bufferName|
		var buffer = lliaApp.getBuffer(bufferName);
		fixedParameters.put(param.asSymbol, buffer);
	}

	/*
     * Merge transient parameters from note-on event and currentProgram
     * with fixed parameters (mostly bus and buffer assignments).
     *
     * ARGS:     
     *    alist argument is association list from note-on event.
     *    [\gate, 1, \freq, n, \keynumber, n ...]
     *
     * RETURNS: merged parameter/value association list
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
	

} // end Keymode
