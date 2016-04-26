/*
** keymode.sc 2016.02.21
** 
** OSC messages:
**   
**    /llia/synthType/oscID/ping 
**    /llia/synthType/oscID/reset 
**    /llia/synthType/oscID/free
**    /llia/synthType/oscID/dump
**
**    /llia/synthType/oscID/note-on  [keynumber, frequency, velocity]
**       keynumber - MIDI key number 0,1,2,...,127
**       frequency - floatin Hz
**       velocity  - float 'normalized' 0.0 <= velocity <= 1.0
**
**    /llia/synthType/oscID/note-off [keynumber]
**    /llia/synthType/oscID/all-notes-off
**    /llia/synthType/oscID/synth-param [param, value]
**
*/

Keymode : Object {

	var <oscID;
	var <globalAppID; 
	var <synthType;
	var <netAddress;
	var <>outbus;
	var <>inbus;
	var currentProgram;
	var oscHandlers;
	var <dead;

	*new {
		^super.new;
	}

	init {|sid, oscid=nil, globalOscID="llia"|
		if (oscid == nil, {oscid = sid});
		globalAppID = globalOscID;
		oscID = oscid;
		synthType = sid;
		currentProgram = Program.new();
		oscHandlers = [];
		dead = false;
		this.netAddress_("127.0.0.1", 57120);
		this.outbus_(0);
	}

	netAddress_ {|address="localhost", port=57120|
		netAddress = NetAddr.new(address, port);
		this.initOSCFunctions
	}

	path {|tail|
		var rs = "/Llia/"++globalAppID++"/"++synthType++"/"++oscID++"/"++tail;
		//postf("DEBUG keymode.path('%') -> '%'\n", tail, rs);
		^rs
	}
		
	initOSCFunctions {
		var ary;
		oscHandlers.do.free;
		ary = [

			OSCFunc({|msg, time, addr, port|
				["PING", oscID, msg, time, addr, port].postln},
				this.path("ping")),

			OSCFunc({|msg, time, addr, port|
				this.reset()},
				this.path("reset")),
			
			OSCFunc({|msg, time, addr, port|
				this.free},
				this.path("free")),

			OSCFunc({|msg, time, addr, port|
				this.lliaDump()},
				this.path("dump")),

			OSCFunc({|msg, time, addr, port|
				var keynumber = msg[1];
				var frequency = msg[2];
				var velocity = msg[3];
				this.noteOn(keynumber, frequency, velocity)},
				this.path("note-on")),
			
			OSCFunc({|msg, time, addr, port|
				var keynumber = msg[1];
				var velocity = msg[2];
				this.noteOff(keynumber, velocity)},
				this.path("note-off")),
		
			OSCFunc({|msg, time, add, port|
				this.allNotesOff()},
				this.path("all-notes-off")),

			OSCFunc({|msg, time, add, port|
				var param = msg[1];
				var value = msg[2];
				this.set_(param, value)},
				this.path("synth-param")) ];
		oscHandlers = ary;
	}

	lliaDump {|pad=""|
		var pad2 = pad++"    ";
		postf("%% keymode\n", pad, this.class);
		postf("%isDead: %\n", pad2, dead);
		postf("%netAddress: %\n", pad2, netAddress);
		postf("%synthType: %,   oscID: %\n", pad2, synthType, oscID);
		postf("%inbus  : %\n", pad2, inbus);
		postf("%outbus : %\n", pad2, outbus);
	}

	synthParams {
		^currentProgram.synthParams
	}

	allNotesOff {
		128.do{|kn| this.noteOff(kn, 0)};
	}
	
	/*
	 * subclasses should override all functions below
     * 
	*/

	free {
		dead = true;
		oscHandlers.do({|h| h.free})
	}
	
	reset {
		currentProgram = Program.new();
	}

	
	set_ {|param,  value|
		currentProgram.set_(param.asSymbol, value);
	}

	/* velocity normalized to (0.0, 1.0) */

	noteOn {|keynumber, frequency, velocity|
	}

	noteOff {|keynumber|
	}



} // end Keymode