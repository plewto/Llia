/*
** llia.sc 2016.04.20
**
** Error numbers:
** 1 - Attempt to add bus with existing bus name.
** 2 - Attempt to add synth with existing synth id.
**
*/

LliaHandler : Object {

	var lliaClient;						// NetAddr
	var lliaHost;						// NetAddr
	var <oscID;							// String
	var synths;							// Dictionary
	var audioBuses;						// Dictionary
	var controlBuses;					// Dictionary
	var oscHandlers;					//
	var <dead;							// flag

	// See Llia/docs/keymodes
	*validKeyModes {
		^"Poly1 Mono1 EFX";
	}

	// See Llia/docs/synthtypes
	*validSynthTypes {
		^"Orgn Saw3 Echo1";
	}
	
	/*
	** Predicate test if argument is integer bus number.
    ** ARGS:
    **   n - Object.
    ** RETURNS:
    **   true if n is an integer or string representation of an integer
    */
	*isIntegerBusNumber {|n|
		if(n.isInteger,
			{
				^true;
			},{
				var q = n.asInteger;
				if(q == 0,
					{
						^(n=="0");
					},{
						^true;
					})
			})
	}


	/*
    ** Create new instance of LliaHandler.
	** ARGS:
    **   oscid - String, root OSC id 
    **   clientAddress - String, ip address for client
    **   clientPort    - int, Port number number
    **   ip   - String, ip address for this.
    **   port -	int, port number for this.
	*/
	*new {|oscid = "llia",
		   clientAddress = "127.0.0.1",
		   clientPort = 58000,
		   ip = "127.0.0.1",
		   port = 57120|
		^super.new.init(clientAddress, clientPort, ip,port, oscid);
	}

	init {|clientAddress, clientPort, ip, port, oscid|
		this.setClient(clientAddress, clientPort);
		lliaHost = NetAddr.new(ip, port);
		oscID = oscid.asString;
		synths = Dictionary.new(8);
		audioBuses = Dictionary.new(8);
		controlBuses = Dictionary.new(8);
		this.initOscHandlers;
	}

	lliaDump {|pad=""|
		var pad2 = pad++"    ";
		var pad3 = pad2++"    ";
		var isDead = "";
		if(dead==true, {isDead="+DEAD+ "});
		postf("\n%%LliaHandler   oscID: '%'\n", pad, isDead, oscID);
		postf("%client: %\n", pad2, lliaClient);
		postf("%self  : %\n", pad2, lliaHost);
		postf("%Audio Buses  :", pad2);
		this.audioBusNames.do({|n| postf(" %",n)});
		postf("\n");
		postf("%Control Buses:", pad2);
		this.controlBusNames.do({|n| postf(" %",n)});
		postf("\n");
		postf("%Synths:\n", pad2);
		synths.values.do({|si| si.lliaDump(pad3)});
		postf("\n");
	}

	/*
    ** Free this and all resources under it.
    ** Once freed further OSC communication is not possible.
	*/
	free {
		dead = true;
		oscHandlers.do({|h| h.free});
		synths.values.do({|si| si.free});
		postf("Freed LliaHandler %\n", oscID);
	}

	/*
    ** Set client address and port.
    */
	setClient {|ip, port|
		lliaClient = NetAddr.new(ip, port);
	}

	/*
	** Return a list OSC id's for all managed synths.
	*/
	synthNames {
		^synths.keys;
	}

	/*
	** Predicate returns true if Synth with osc id exists.
	*/
	synthExists {|id|
		var flag = true;
		synths.atFail(id, {flag=false});
		^flag;
	}

	/*
	** Free the synth with matching OSC id.
	*/
	freeSynth {|id|
		if(this.synthExists(id),
			{
				var info = synths.at(id);
				info.panic;
				info.free;
				^true;
			},{
				^false;
			});
	}


	/*
	** Add new synth.
    ** ARGS:
    ** synthType    - String, the synth name.  See Llia/docs/synthtypes
    ** id           - int, synth OSC id
    **                id must be unique for any given sunth type.
    **                The OSC path to this synth becomes /llia/aynthType/id/
    **                If an identical synth is already in use it is 
    **                resources are first freed and then replaced by 
    **                a new synth.
    **   keymode    - Sting, see Llia/docs/keymodes
    **                See Llia/docs/keymodes for possible values.
    **   outbus     - String or int, sets audio outbus bus.
    **                The bus maybe specified as an absolute bus number
    **                or as a bus name alias. See audioBusNames
    **   inbus      - String or int, sets input bus names.
    **                inbus is mostly used for effects synths.  For synths
    **                which do not use an input bus this value is ignored.
    **                The bus maybe specified as an absolute bus number
    **                or by bus alias. See audioBusNames. 
    **   voiceCount - int, sets number of allocated synth voices.
    **                voiceCount is only used by keymodes which have a
    **                fixed number of voices and ignored otherwise.
    **                Currently all keymodes ignore voiceCount. 
	*/
	addSynth {|synthType, id, keymode, outbus, inbus, voiceCount|
		var outb, inb, sinfo;
		outb = this.audioBus(outbus);
		inb = this.audioBus(inbus);
		//postf("DEBUG synthType '%'  outbus='%' outb='%'  \n", synthType, outbus, outb);
		sinfo = LliaSynthInfo(synthType, id, oscID, keymode, outb, inb, voiceCount);
		id = synthType++"_"++id;
		this.freeSynth(id);
		synths.add(id -> sinfo);
		postf("Added % synth oscID %\n", oscID, id) 
	}

	/*
    ** A convenience method for adding effects synths.
    ** All arguments have same usage as with addSynth.
    */
	addEfx {|synthType, id, outbus, inbus|
		^this.addSynth(synthType, id, "EFX", outbus, inbus, 1);
	}

	/*
    ** Get info for indicated synth
    ** ARGS:
    **   id - String, the synths OSC id.
	**
    ** RETURNS: 
    **   LliaSynthInfo or nil.
    */
	getSynthInfo {|id|
		if(this.synthExists(id),
			{
				^synths.at[id];
			},{
				^nil;
			})
	}

	/*
    ** Returns a list of audio bus aliases.
	*/
	audioBusNames {
		^audioBuses.keys;
	}

	/*
    ** Predicate test if audio bus alias exists.
    ** If name is an integer >= 0 the bus is assumed to exists.
	*/
	audioBusExists {|name|
		if(LliaHandler.isIntegerBusNumber(name),
			{
				^true;
			},{
				var flag = true;
				audioBuses.atFail(name, {flag=false});
				^flag;
			})
	}

	/*
    ** Add an new audio bus alias
    ** ARGS:
    **  id       - String, the bus name. If a bus with the same name already
    **             exists a new bus with the same name may not be created.
    **  numchans - int, number of channels.
    **
    ** RETURNS:
    **   false -> A bus with identical name already exits.
    **   int -> the bus index.
	*/
	addAudioBusAlias {|id, numchans=1|
		id = id.asString;
		if(this.audioBusExists(id),
			{
				postf("WARNING: Audio bus '%' already exists!\n", id);
				^false;
			},{
				// var b = Bus.audio(nil, numchans);
				// var index = b.index;
				var b, index;
				id = id.asString;
				numchans = numchans.asInteger.max(1);
				b = Bus.audio(nil, numchans);
				index = b.index;
				audioBuses.add(id -> b);
				postf("Created % audio bus alias [%] -> %\n", oscID, id, index);
				^index;
			})
	}

	/*
	** Return audio bus.
    ** ARGS:
    **   id - String or int
    ** RETURN:
    **   bus index or nil.
    */
	audioBus {|id|
		if(id == nil, {id=0});
		if(LliaHandler.isIntegerBusNumber(id),
			{
				^id
			},{
				if(this.audioBusExists(id),
				{
					^audioBuses.at(id);
				},{
					postf("WARNING: Audio bus '%' does not exists!\n", id);
					^0;
				})
			})
	}


	/* ****************************************************************
    ** All control bus methods have the same name and usage as with 
    ** audio buses:   'controlBusBlahBlah' instead of 'audioBusBlahBlah'.
    **
    ** Control buses have been added for completeness, currently they 
    ** are not actually used for anything.
	*/

	controlBusNames {
		^controlBuses.keys;
	}

	controlBusExists {|name|
		if(LliaHandler.isIntegerBusNumber(name),
			{
				^true;
			},{
				var flag = true;
				controlBuses.atFail(name, {flag=false});
				^flag;
			})
	}

	addControlBusAlias {|id, numchans=1|
		id = id.asString;
		if(this.controlBusExists(id),
			{
				postf("WARNING: Control bus '%' already exists!\n", id);
				^false;
			},{
				var b, index;
				id = id.asString;
				numchans = numchans.asInteger.max(1);
				b = Bus.control(nil, numchans);
				index = b.index;
				controlBuses.add(id -> b);
				postf("Created % control bus alias [%] -> %\n", oscID, id, index);
				^index;
			})
	}

	controlBus {|id|
		if(LliaHandler.isIntegerBusNumber(id),
			{^id},
			{if(this.controlBusExists(id),
				{
					^controlBuses.at(id);
				},{
					postf("WARNING: Audio bus '%' does not exists!\n", id);
					^nil;
				})})
	}

	/*
    ** Return SuperCollider server
    ** ARGS:
    **   s - Server name, may be "local", "internal" or "default"
    */
	getServer {|s|
		var rs;
		s = s.asString.toLower;
		case {s == "local"}{rs = Server.local}
		     {s == "internal"}{rs = Server.internal}
		     {true}{rs = Server.default};
		^rs;
	}

	/*
    ** Send panic (all-notes-off) message to all manged synths.
	*/
	panic {
		synths.do({|si| si.panic;});
		postf("% PANIC\n", oscID);
	}

	/*
    ** Generate and send an OSC response message to the Llia client app.
    ** msg - The OSC address 
    ** payload - additional values.
    */
	respond {|msg, payload|
		var id = oscID.asString;
		var addr = "/Llia/"++id++"/"++msg;
	    //postf("Response:  addr = '%'\n", addr); // DEBUG
		lliaClient.sendMsg(addr, payload);
	}

	/*
    ** Send OSC response message to the Llia client app indicating 
    ** there is an error.
	*/
	respondWithError {|errnumber, errmsg|
		var msg = errnumber.asString+", "+errmsg;
		this.respond("ERROR", msg);
	}

	path {|tail|
		var id = oscID.asString;
		var rs;
		tail = tail.asString;
		rs = "/Llia/"++id++"/"++tail;
		^rs;
	}
	
	/* used internally - do not use */
	
	initOscHandlers {
		oscHandlers.do.free;
		oscHandlers = [

			/*
            ** ping 
            ** Post message indicating ping message reception
            ** -> llia-ping-response
            */
			OSCFunc({|msg|
				"LliaHandler.ping".postln;
				this.respond("llia-ping-response", [])},
				this.path("ping")),

			/*
            ** dump
            ** Post diagnostic info on this.
            ** -> (none)
			*/
			OSCFunc({|msg|
				this.lliaDump;
				this.respond("llia-dump-response", [])},
				this.path("dump")),

			/*
			** post [lines...]
            ** Display lines in post window
			** -> llia-post-response
			*/
			OSCFunc({|msg|
				var s = msg.size;
				var i = 1;
				while({i<s},
					{
						msg[i].post;
						i = i + 1;
					});
				this.respond("llia-post-response", [])},
				this.path("post")),

			/*
            ** set-llia-client [ip port]
            ** Set Llia client app ip address and port number
            ** -> set-llia-client [oscId, ip, port]
            */
			OSCFunc({|msg|
				var ip = msg[1];
				var port = msg[2];
				lliaClient = NetAddr.new(ip.asString, port);
				this.respond("set-llia-client", [oscID, ip, port])},
				this.path("set-llia-client")),

			/*
            ** query-keymodes
            ** Display list of valid keymodes.
            ** -> llia-keymodes [...]
            */
			OSCFunc({|msg|
				postf("Llia keymodes: %\n", LliaHandler.validKeyModes);
				this.respond("llia-keymodes", LliaHandler.validKeyModes)},
				this.path("query-keymodes")),

			/*
            ** query-synthtypes
            ** Display list of known synthtypes.
            ** -> llia-synthtypes [...]
            ** ISSUE: Is this message necessary?
            */
			OSCFunc({|msg|
				postf("Llia synthtypes: %\n", LliaHandler.validSynthTypes);
				this.respond("llia-synthtypes", LliaHandler.validSynthTypes)},
				this.path("query-synthtypes")),

			/*
			** query-active-synths
            ** Display list of all active synths
            ** -> llia-active-synths [...]
			*/
			OSCFunc({|msg|
				var acc = "";
				postf("active synths:\n");
				synths.do({|si|
					//var bcc = "<synth>" + si.synthType + si.oscID.asString + si.buses.asString;
					var bcc = "<synth>" + si.synthType + si.oscID.asString;
					var ib = "inbus: " + si.buses[0].asString;
					var ob = "outbus: " + si.buses[1].asString;
					bcc = bcc + ib + ob;
					acc = acc ++ bcc;
					postf("  %\n", bcc)});
				this.respond("llia-active-synths", acc)},
				this.path("query-active-synths")),
					
			/*
            ** query-audio-buses
            ** Display list of audio bus aliases
            ** -> llia-audio-buses [...]
			*/
			OSCFunc({|msg|
				var names = this.audioBusNames;
				var acc = "";
				names.do({|n| acc = acc + n.asString});
				postf("Audio buses: %\n", acc);
				this.respond("llia-audio-buses", acc)},
				this.path("query-audio-buses")),

			/*
			** add-audio-bus [name, numchans]
            ** Add new audio bus alias.
            ** -> llia-audio-buses [...]
            ** -> ERROR: bus already exists.
			*/
			OSCFunc({|msg|
				var name = msg[1];
				var numchans = msg[2];
				var flag = this.addAudioBusAlias(name, numchans);
				if(flag == false,
					{
						var errmsg = "Audio bus '"++name++"' already exists!";
						this.respondWithError(1, errmsg);
					},{
						this.respond("llia-audio-buses", this.audioBusNames);
					})},
				this.path("add-audio-bus")),

			/*
			** query-control-buses
            ** Display list of control bus aliases.
            ** -> llia-control-buses [...]
			*/
			OSCFunc({|msg|
				var names = this.controlBusNames;
				var acc = "";
				names.do({|n| acc = acc + n.asString});
				postf("Control buses: %\n", acc);
				this.respond("llia-control-buses", acc)},
				this.path("query-control-buses")),

			/*
            ** add-control-bus [name numchans]
            ** Add new control bus alias.
            ** -> llia-control-buses [...]
            ** -> ERROR: bus already exists.
			*/
			OSCFunc({|msg|
				var name = msg[1];
				var num = msg[2];
				var flag = this.addControlBusAlias(name, num);
				if(flag == false,
					{
						var errmsg = "Control bus '"++name++"' already exists!";
						this.respondWithError(1, errmsg);
					},{
						this.respond("llia-control-buses", this.controlBusNames);
					})},
				this.path("add-control-bus")),

			/*
            ** add-synth [synthType, id, keymode, outbus, inbus, vcount]
            ** Adds new synth.  See addSynth method.
            ** ARGS:
            **   synthType - String
            **   id - OSC id for this synth, must be unique.
            **   keymode - See Llia/docs/keymodes
            **   outbus - int or bus name alias
            **   inbus - int or bus name alias
            **   vcount - int, voice count.
            **
            ** -> llia-added-synth id
            ** -> ERROR: Synth with identical id already exists.
			*/
			OSCFunc({|msg|
				var synthType = msg[1].asString;
				var id = msg[2].asString;
				var keymode = msg[3].asString;
				var outbus = msg[4].asString;
				var inbus = msg[5].asString;
				var vcount = msg[6].asInteger.max(1);
				if(this.synthExists(id),
					{
						var errmsg = "Synth '"++id++"' already exists!";
						postf("WARNING: %\n", errmsg);
						this.respondWithError(2, errmsg);
					},{
						this.addSynth(synthType, id, keymode, outbus, inbus, vcount);
						this.post("Added synth: %\n", id);
						this.respond("llia-added-synth", id.asString);
					})},
				this.path("add-synth")),

			/*
            ** llia-add-efx-synth [synthType, id, outbus,inbus]
            ** Convenience message same as add-syhth with keymode = "EFX"
            ** and voiceCount = 1
            ** -> llia-added-efx-synth
            ** -> ERROR: synth with identical id already exists.
			*/
			OSCFunc({|msg|
				var synthType = msg[1].asString;
				var id = msg[2].asString;
				var outbus = msg[3].asString;
				var inbus = msg[4].asString;
				if(this.synthExists(id),
					{
						var errmsg = "EFX Synth '"++id++"' already exists!";
						postf("WARNING: %\n", errmsg);
						this.respondWithError(2, errmsg);
					},{
						this.addEfx(synthType, id, outbus, inbus);
						this.post("Added efx synth: %\n", id);
						this.respond("llia-added-efx-synth", id.asString);
					})},
				this.path("add-efx-synth")),

			/*
            ** query-all-running-servers
            ** Display list of all running SuperCollider servers.
            ** -> all-running-servers [...]
			*/
			OSCFunc({|msg|
				var acc = "";
				var s = Server.allRunningServers; 
				s.do({|srv| acc=acc+srv.asString});
				postf("All running servers: %\n", acc);
				this.respond("all-running-servers", acc)},
				this.path("query-all-running-servers")),

			/*
            ** boot-server [name]
            ** Boot a SuperCollider server. Name may be one of
            ** 'local', 'internal' or 'default'.
            ** -> llia-booting-server [name]
			*/
			OSCFunc({|msg|
				var n = msg[1];
				var s = this.getServer(n);
				postf("Llia booting server: %\n", s);
				s.boot;
				this.respond("llia-booting-server", s)},
				this.path("boot-server")),

			/*
            ** quit-server [name]
            ** Send quit message to SuperCollider server. 
            ** name may be one of 'local', 'internal or 'default'.
            ** -> llia-server-quit [name]
			*/
			OSCFunc({|msg|
				var n = msg[1];
				var s = this.getServer(n);
				postf("Llia server quit: %\n", s);
				s.quit;
				this.respond("llia-server-quit", s.asString)},
				this.path("quit-server")),

			/*
            ** kill-all-servers
            ** -> llia-kill-all-servers
            */
			OSCFunc({|msg|
				"Llia server killAll".postln;
				Server.killAll;
				this.respond("llia-kill-all-servers")},
				this.path("kill-all-servers")),
								
		]
	}
}
					
