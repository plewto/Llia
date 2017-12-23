/*
** llia.sc 2016.04.20
**
** A LliaHandler is the primary interface between a Llia client application
** and SuperCollider.  It oversees OSC communication and maintains lists of
** resources in used by Llia.
**
** Error numbers:
** 1 - Attempt to add bus or buffer with existing bus name.
** 2 - Attempt to add synth with existing synth id.
** 3 - Bus, buffer or synth does not exist.
*/

LliaHandler : Object {

	var lliaClient;						// NetAddr
	var lliaHost;						// NetAddr
	var <oscID;							// String
	var synths;							// Dictionary
	var audioBuses, controlBuses;		// LliaBuses
	var <buffers;						// LliaBuffers
	var oscHandlers;					// Array
	var <isDead;						// flag
	var serverOptions;					//

	/* **** DEPRECIATED ****
	// See Llia/docs/keymodes
	*validKeyModes {
		^"Poly1 Mono1 EFX";
	}

	// See Llia/docs/synthtypes
	*validSynthTypes {
		^"Orgn Saw3 Echo1";
	}
		*********************** */	


	/*
    ** Create new instance of LliaHandler
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

	/*
	** Initialize instance.
    ** ARGS:
    **     clientAddress - a NetAddr
    **     clientPort    - int, client port number.
    **     ip            - ip address for this instance.
    **     port          - int, port number for this instance.
    **     oscid         - String, unique id, must match id of client app.
	*/
	init {|clientAddress, clientPort, ip, port, oscid|
		this.setClient(clientAddress, clientPort);
		lliaHost = NetAddr.new(ip, port);
		oscID = oscid.asString;
		serverOptions = ServerOptions.new;
		synths = Dictionary.new(16);
		audioBuses = LliaBuses.new(\audio);
		controlBuses = LliaBuses.new(\control);
		buffers = LliaBuffers.new;
		this.initOscHandlers;
	}

	/*
	** Free all resources used by Llia.
	*/
	free {
		oscHandlers.do({|hfn| hfn.free});
		isDead = true;
		audioBuses.freeAll;
		controlBuses.freeAll;
		buffers.freeAll;
		synths.values.do({|sy| sy.free});
		synths = Dictionary.new(16);
	}

	/*
    ** Restart Llia server.
    */
	restart {
		audioBuses.restart;
		controlBuses.restart;
		buffers.restart;
		synths.values.do({|sy| sy.free});
		synths = Dictionary.new(16);
		postf("*** Llia restarted ***\n");
	}

	//  ---------------------------------------------------------------------- 
	// 								   Buses

	/*
    ** Used internally to access managed buses. 
    ** ARGS:
    **    rate - symbol, either \audio or \control.
    **           It is an error if rate is neither \audio or \control.
    ** RETURNS:
    **    instance of LliaBus
	*/
	selectBusList {|rate|
		if (rate == \audio,
			{
				^audioBuses;
			},{
				if (rate == \control,
					{
						^controlBuses;
					},{
						var msg = "Invalid bus rate: '" ++ rate.asString ++ "'";
						Error(msg).throw;
					});
			})
	}


	/*
	** Returns number of buses.
    ** ARGS:
    **    rate - symbol, either \audio or \control
    ** RETURNS:
    **    int
    */
	busCount {|rate|
		var bl = this.selectBusList(rate);
		^bl.busCount;
	}

	/*
	** Returns list of bus names.
    ** ARGS:
    **   rate - symbol, either \audio or \control
    ** RETURNS:
    **   An unsorted list of bus names.
	*/
	busList {|rate|
		var bl = this.selectBusList(rate);
		^bl.busList;
	}

	/*
    ** Predicate, true if indicated bus exists.
    ** ARGS:
    **   rate - symbol, either \audio or \control
    **   busName - String
    ** RETURNS:
    **   Bool
	*/
	busExists {|rate, busName|
		var bl = this.selectBusList(rate);
		^bl.busExists(busName);
	}

	/*
	** Add new bus of indicated type.
    ** ARGS:
    **   rate - symbol, either \audio or \control
    **   busName - String
    **   numChannels - optional int, default 1.
    ** RETURNS:
    **   Bool
    **   If a bus with the same name already exists, post a warning message
	**   and return false.
    **   Return true if bus was created.
	*/
	addBus {|rate, busName, numChannels=1|
		var bl, rs;
		bl = this.selectBusList(rate);
		rs = bl.addBus(busName, numChannels);
		^rs;
	}


	/*
	** Returns index of named bus.
    ** ARGS:
    **   rate - symbol,either \audio or \control
    **   busName - String
    **   offset - optional int, default 0.
    ** RETURNS:
    **   int, bus number of indicated bus + offset.
	*/
	getBusIndex {|rate, busName, offset=0|
		var bl;
		bl = this.selectBusList(rate);
		^bl.getBusIndex(busName, offset);
	}

	/*
    ** Free resources used by indicated bus.
    ** ARGS:
    **   rate - symbol, either \audio or \control.
    **   busName - String.
	*/
	freeBus {|rate, busName|
		var bl = this.selectBusList(rate);
		bl.free(busName);
	}
		
	//  ---------------------------------------------------------------------- 
	// 								  Buffers
	//
    // NOTE: At this date (2017.12.23) buffers are not supported.

	bufferCount {
		^buffers.bufferCount;
	}

	bufferList {
		^buffers.bufferList;
	}

	bufferExists {|bufferName|
		bufferName = bufferName.asString;
		^buffers.bufferExists(bufferName);
	}

	addBuffer {|bufferName, frames=1024, numChannels=1|
		bufferName = bufferName.asString;
		^buffers.addBuffer(bufferName, frames, numChannels);
	}

	getBuffer {|bufferName|
		var rs;
		bufferName = bufferName.asString;
		rs = buffers.getBuffer(bufferName);
		^rs
	}

	freeBuffer {|bufferName|
		bufferName = bufferName.asString;
		buffers.free(bufferName);
	}

	
	//  ---------------------------------------------------------------------- 
	// 								  Synths

	/*
	** Returns list of currently active synths ids.
    ** A synth id ("sid") is a string of form xxx_n, where xxx
    ** is the synth type and n is a unique serial number.
	*/
	synthNames {
		^synths.keys;
	}

	/*
    ** Predicate, returns true if sid is currently in use.
    */
	synthExists {|sid|
		var flag = true;
		synths.atFail(sid, {flag=false});
		^flag
	}

	/*
    ** Frees resources for indicated synth.
    ** ARGS:
    **   sid - String, synth id.
    ** RETURNS:
    **   bool, true if synths were freed.
    */
	freeSynth {|sid|
		if(this.synthExists(sid),
			{
				var info = synths.at(sid);
				synths.removeAt(sid);
				info.panic;
				info.free;
				^true;
			},{
				^false;
			});
	}

	/*
    ** Adds new set of active synths.
    ** ARGS:
    **    stype - String, synth type. 
    **            See Llia.llia.constants.py SYNTH_TYPES
    **    id    - int, a unique serial number.
    **    km    - String, name of key mode.
    **            See Llia.llia.constants.py KEY_MODES
    **    voiceCount - int, number of "real" synths to create.
    **            voiceCount is ignored for key modes with implicit
    **            number of voices (IE Mono1, EFX, etc...)
    **
    ** NOTE: At a minimum an output bus must be established for the synth 
    **       after it has been created. 
    */
	addSynth {|stype, id, km="Poly1", voiceCount=8|
		var sid, sy;
		var frmt = "Added Synth: '%'\n";
		if (km == "EFX", {frmt = "Added EFX Synth: '%'\n"});
		sid = stype.asString ++ "_" ++ id.asString;
		sy = LliaSynthInfo.new(this, stype, id, oscID, km, voiceCount);
		if (this.synthExists(sid),
			{
				postf("WARNING: Replacing existing % synth %\n", stype, id);
			},{
				postf(frmt, sid);
			});
		this.freeSynth(sid);
		synths.put(sid, sy);
		^sy;
	}

	/*
	** Adds a new Effects or Controller synth.
    ** addEfx does little more then call addSynth.
    ** ARGS:
    **   stype - String, synth type.
    **           See Llia/llia/constants.py EFFECT_TYPES and CONTROLLER_TYPES
    **   id - unique int serial number.
	*/
	addEfx {|stype, id|
		var sy;
		sy = this.addSynth(stype, id, "EFX");
		sy.isEfx_(true);
		^sy;
	}

	getSynthInfo {|stype, id|
		var sid = (stype.asString ++ "_" ++ id.asString);
		var sy = synths.at(sid);
		^sy;
	}

	/*
	** Assign bus to a synth parameter.
    ** ARGS:
    **   stype   - String, synth type
    **   id      - int, synth serial number.
    **   param   - String, the synth parameter.
    **   rate    - Symbol, either \audio or \control
    **   busName - String
    **   offset  - optional int, default 0.
    **
    ** Post warning if either synth or bus does not exists.
    ** RETURNS:
    **    bool - true if assignment succeeded. 
	*/
	assignSynthBus {|stype, id, param, rate, busName, offset=0|
		var sy;
		sy = this.getSynthInfo(stype, id);
	    if (sy == nil,
			{
				postf("WARNING: % synth % does not exists\n", stype, id);
				^false;
			},{
				if (this.busExists(rate, busName),
					{
						var kmobj;
						kmobj = sy.keymodeObject;
						kmobj.setBusParameter(param, rate, busName, offset);
						^true;
					},{
						postf("WARNING: % bus % does not exists\n", rate, busName);
						^false;
					})
			})
	}

	assignSynthBuffer {|stype, id, param, bufferName|
		var sy;
		sy = this.getSynthInfo(stype, id);
		if (sy == nil,
			{
				posrf("WARNING: % synth % does not exists\n", stype, id);
				^false;
			},{
				if (this.bufferExists(bufferName),
					{
						var kmobj;
						kmobj = sy.keymodeObject;
						kmobj.setBufferParameter(param, bufferName);
						// postf("Buffer % -> %_% parameter %\n", bufferNAme, stype, id, param);
						^true;
					},{
						postf("WARNING: Buffer '%' does not exists\n", bufferName);
						^false;
					})
			})
	}
	
	
	//  ---------------------------------------------------------------------- 
	// 									OSC

	setClient {|ip, port|
		lliaClient.free;
		lliaClient = NetAddr.new(ip, port);
	}
	
	/*
    ** Generate and send an OSC response message to the Llia client app.
    ** msg - The OSC address 
    ** payload - additional values.
    */
	respond {|msg, payload|
		var id, addr;
		id = oscID.asString;
		addr = "/Llia/"++id++"/"++msg;
	    // postf("Response:  addr = '%'\n", addr); // DEBUG
		lliaClient.sendMsg(addr, payload);
	}

	/*
    ** Send OSC response message to the Llia client app indicating 
    ** there has been an error.
	*/
	respondWithError {|errnumber, errmsg|
		var msg = errnumber.asString+", "+errmsg;
		this.respond("ERROR", msg);
	}


	/*
    ** Construct an OSC message path.
	** ARGS:
    **   msg - String, the OSC message type
    ** RETURNS:
    **   String of form   "/Llia/id/msg" 
    **   where id is th OscId shared between this and the client app.
    */
	path {|msg|
		var id = oscID.asString;
		var rs;
		msg = msg.asString;
		rs = "/Llia/"++id++"/"++msg;
		^rs;
	}

	/*
	** Post diagnostic text.
	*/
	lliaDump {|pad=""|
		var pad2 = pad++"    ";
		postf("%LliaHandler  isDead: % :\n", pad, isDead);
		postf("%oscID  : %\n", pad2, oscID);
		postf("%host   : %\n", pad2, lliaHost);
		postf("%client : %\n", pad2, lliaClient);
		audioBuses.lliaDump(pad2);
		controlBuses.lliaDump(pad2);
		buffers.lliaDump(pad2);
		postf("%synths:\n", pad2);
		this.synthNames.do{|sid|
			postf("%   %\n", pad2, sid);
		}
	}

	/*
    ** Initialize OSC handler functions.
	*/
	initOscHandlers {
		var ary;
		oscHandlers.do.free;
		ary = [

			/*
            ** A 'ping' message is used to test connectivity between this and
			** the client app.  The client initiates by transmitting the
			** message "ping".  The server responds by:
            **   1) Display a message in the Post window.
            **   2) Transmit a "ping-response" back to the client.
			*/
			OSCFunc ({|msg|
				postf("Llia/%/ping\n", oscID);
				this.respond("ping-response", "")},
				this.path("ping")),

			/*
            ** Reception of a 'free' message indicates this should free all
		    ** managed resources. 
            */
			OSCFunc ({|msg|
				postf("Llia/%/free\n", oscID);
				this.free},
				this.path("free")),

			/*
			** A 'restart' message indicates the server handler should
			** free all resources and then reset to the initial state.
			*/
			OSCFunc ({|msg|
				postf("Llia/%/restart\n", oscID);
				this.restart},
				this.path("restart")),

			/*
            ** 'dump' - instructs server to display a diagnostic data to
		    ** the post window.
            */
			OSCFunc ({|msg|
				this.lliaDump},
				this.path("dump")),

			
			// OSCFunc ({|msg|
			// 	var sname = msg[0];
			// 	this.respond("booting-server");
			// 	case  {sname == "local"}
			// 	      {Server.local.boot}
            //
			// 	      {sname == "internal"}
			// 	      {Server.internal.boot}
            //
			// 	      {Server.default.boot}},
			// 	this.path("boot-server")),

			OSCFunc ({|msg|
				var oid = msg[1];
				var addr = msg[2].asString;
				var port = msg[3].asInt;
				oscID = oid;
				lliaClient = NetAddr.new(addr, port);
				this.initOscHandlers;
				postf("OSC client  id: '%',  address: %,  port: %\n", oid, addr, port);
				this.respond("ping-response")},
				this.path("set-client")),

			/*
            ** 'add-bus' rate bname n
            ** ARGS:
            **   rate  - string,  '\audio' or '\control'.
            **   bname - string, the bus name.
            **   n     - int, number of buses.
			*/
			OSCFunc ({|msg|
				var rate, bname, numChannels, rs;
				rate = msg[1].asSymbol;
				bname = msg[2];
				numChannels = msg[3].asInt;
				rs = this.addBus(rate, bname, numChannels);
				this.respond("bus-added", rs)},
				this.path("add-bus")),

			/*
            ** 'free-bus' rate bname
            ** ARGS:
            **   rate  - \audio or \control
            **   bname - bus name
            */
			OSCFunc ({|msg|
				var rate = msg[1].asSymbol;
				var bname = msg[2].asString;
				this.freeBus(rate, bname)},
				this.path("free-bus"));

			/*
			** 'get-bus-stats' rate
            ** ARGS:
            **   rate - \audio or\control
            ** Transmits a 'bus-stats' message back to the client.
            */
			OSCFunc ({|msg|
				var rate = msg[1].asSymbol;
				var maxBus, numOut, numIn, fpb, allocated, rsmsg;
				if (rate == \audio,
					{
						maxBus = serverOptions.numAudioBusChannels.asString;
						numOut = serverOptions.numOutputBusChannels.asString;
						numIn = serverOptions.numInputBusChannels.asString;
						fpb = serverOptions.firstPrivateBus.asString;
						allocated = audioBuses.size.asString;
						rsmsg = rate.asString + maxBus + numOut + numIn + fpb + allocated;
						this.respond("bus-stats", rsmsg)
					},{
						maxBus = serverOptions.numControlBusChannels.asString;
						allocated = controlBuses.size.asString;
						rsmsg = rate.asString + maxBus + allocated;
						this.respond("bus-stats", rsmsg);
					})},
				this.path("get-bus-stats")),
			/*
			** 'get-bus-info' rate bname
            ** ARGS:
            **   rate - \audio or \control
            **   bname - String, bus name
            **
            ** Transmits a 'bus-info' message back to client.
			*/
			OSCFunc ({|msg|
				var rate = msg[1].asSymbol;
				var name = msg[2].asString;
				var bus, acc, index, numChans;
				try {
					if (rate == \audio,
					{
						bus = audioBuses.getBus(name);
					},{
						rate = \control;
						bus = controlBuses.getBus(name);
					});
					index = bus.index.asString;
					numChans = bus.numChannels.asString;
					acc = name + rate.asString + index + numChans;
					this.respond("bus-info", acc);
				}{
					this.respond("bus-info", "DOES-NOT-EXISTS");
				}},
				this.path("get-bus-info")),

			/*
            ** 'get-bus-list rate
            ** ARGS:
            **   rate - \audio or \control
            ** Transmits a 'get-bus-list message back to client.
            ** The payload of the return message is a sorted list of bus names. 
			*/
			OSCFunc ({|msg|
				var rate, buses, acc;
				rate = msg[1];
				if (rate == \audio,
					{
						buses = audioBuses;
					},{
						buses = controlBuses;
					});
				acc = buses.busList.asList.sort.asString;
				acc = rate.asString + acc;
				this.respond("get-bus-list", acc)},
				this.path("get-bus-list")),

			OSCFunc ({|msg|
				var name, frames, numChannels, rs;
				name = msg[1].asString;
				frames = msg[2].asInt;
				numChannels = msg[3].asInt;
				rs = this.addBuffer(name, frames, numChannels);
				this.respond("buffer-added", rs)},
				this.path("add-buffer")),

			OSCFunc ({|msg|
				var name = msg[1].asString;
				this.freeBuffer(name);
				postf("Freed buffer: '%'\n", name)},
				this.path("free-buffer")),
			
			OSCFunc ({|msg|
				var maxBuffer, allocated, rsmsg;
				maxBuffer = serverOptions.numBuffers.asString;
				allocated = buffers.size.asString;
				rsmsg = maxBuffer + allocated},
				this.path("get-buffer-stats")),

			OSCFunc ({|msg|
				var acc;
				acc = buffers.bufferList.asList.sort.asString;
				this.respond("get-buffer-list", acc)},
				this.path("get-buffer-list")),

			OSCFunc ({|msg|
				var name = msg[1].asString;
				try {
					var buffer, index, frames, channels ,sr, fpath, acc;
					buffer = buffers.getBuffer(name);
					index = buffer.bufnum.asString;
					frames = buffer.numFrames.asString;
					channels = buffer.numChannels.asString;
					sr = buffer.sampleRate.asString;
					fpath = buffer.path.asString;
					acc = name + index + frames + channels + sr + fpath;
					this.respond("get-buffer-info", acc);
				}{
					var acc = name + "DOES-NOT-EXISTS";
					this.respond("get-buffer-info", acc);
				}},
				this.path("get-buffer-info")),

			/*
			** 'add-synth' stype id km vc
            ** ARGS:
            **   stype - String, synth type.
            **   id    - int, unique serial id number.
            **   km    - String, key mode.
            **   vc    - int, voice count, not used by all key modes.
			*/
			OSCFunc ({|msg|
				var stype = msg[1].asString;
				var id = msg[2].asInt;
				var km = msg[3].asString;
				var vc = msg[4].asInt;
				this.addSynth(stype, id, km, vc)},
				this.path("add-synth")),

			/*
			** 'free-synth' sid
            ** ARGS:
            **  sid - Synth id
			*/
			OSCFunc ({|msg|
				var sid = msg[1].asString;
				this.freeSynth(sid);
				postf("Freed synth: '%'\n", sid)},
				this.path("free-synth")),

			/*
            ** 'add-efx stype id
            ** ARGS:
            **   stype - String, effects of controller synth type.
            **   id    - int, unique serial id.
            */
			OSCFunc ({|msg|
				var stype = msg[1].asString;
				var id = msg[2].asInt;
				this.addEfx(stype, id)},
				this.path("add-efx")),

			/*
			** 'panic' - stop all sound.
			*/
			OSCFunc ({|msg|
				synths.do({|sy| sy.panic});
				postln("PANIC!")},
				this.path("panic")),
		
			// OSCFunc ({|msg|
			// 	var txt, i;
			// 	i = 1;
			// 	txt = "";
			// 	while({i < msg.size},
			// 		{
			// 			txt = txt ++ msg[i];
			// 			i = i + 1;
			// 		});
			// 	txt.post},
			// 	this.path("post")),

			// OSCFunc ({|msg|
			// 	var txt, i;
			// 	i = 1;
			// 	txt = "";
			// 	while({i < msg.size},
			// 		{
			// 			txt = txt ++ msg[i];
			// 			i = i + 1;
			// 		});
			// 	txt.postln},
			// 	this.path("postln")),
			
			/*
			** 'assign-synth-audio-bus' stype id param bname offset 
            ** ARGS:
            **   stype  - String, synth type
            **   id     - int, synth serial id.
            **   param  - String, synth parameter to associate to bus.
            **   bname  - String, bus name
            **   offset - int, bus number offset from bname.
            **
            ** Assign an audio bus to synth parameter.
			*/
			OSCFunc ({|msg|
				var stype, id, param, busName, offset, rate, rs;
				stype = msg[1].asString;
				id = msg[2].asInt;
				param = msg[3].asString;
				busName = msg[4].asString;
				offset = msg[5].asInt;
				rate = \audio;
				if(this.assignSynthBus(stype, id, param, rate, busName, offset),
					{
						postf("Audio bus % -> synth %_% parameter %  (offset %)\n", busName, stype, id, param, offset);
					},{
						postf("ERROR: Audio bus % -> synth %_% parameter %\n", busName, stype, id, param);
					})},
				this.path("assign-synth-audio-bus")),


			/*
            ** 'assign-synth-control-bus' stype id busName offset
			** ARGS:
            **   stype  - String, synth type
            **   id     - int, synth serial id.
            **   param  - String, synth parameter to associate to bus.
            **   bname  - String, bus name
            **   offset - int, bus number offset from bname.
            **
            ** Assign control bus to synth parameter.
			*/
			OSCFunc ({|msg|
				var stype, id, param, busName, offset, rate, rs;
				stype = msg[1].asString;
				id = msg[2].asInt;
				param = msg[3].asString;
				busName = msg[4].asString;
				offset = msg[5].asInt;
				rate = \control;
				if(this.assignSynthBus(stype, id, param, rate, busName, offset),
					{
						postf("Control bus % -> synth %_% parameter % (offset %)\n", busName, stype, id, param, offset);
					},{
						postf("ERROR: Control bus % -> synth %_% parameter %\n", busName, stype, id, param);
					})},
				this.path("assign-synth-control-bus")),

			// cmd stype id param buffer-name
			OSCFunc ({|msg|
				var stype, id, param, bufname, rs;
				stype = msg[1].asString;
				id = msg[2].asInt;
				param = msg[3].asString;
				bufname = msg[4].asString;
				if(this.assignSynthBuffer(stype, id, param, bufname),
					{
						postf("Buffer % -> synth %_% parameter %\n", bufname, stype, id, param);
					},{
						postf("ERROR: Buffer % -> synth %_% parameter %\n", bufname, stype, id, param);
					})},
				this.path("assign-synth-buffer")),
			
			// cmd buffer-name, maxharm decay skip mode cutoff depth frames
			OSCFunc ({|msg|
				var bufferName, rs;
				var maxHarm, decay, skip, mode, cutoff, depth, frames;
				bufferName = msg[1].asString;
				maxHarm = msg[2].asInt.max(1);
				decay = msg[3].asFloat.max(0).min(1);
				skip = msg[4].asInt.max(1);
				mode = msg[5].asString;
				cutoff = msg[6].asInt.max(0).min(maxHarm);
				depth = msg[7].asFloat.max(0).min(1);
				frames = msg[8].asInt;
				rs = buffers.wave(bufferName, maxHarm, decay, skip, mode, cutoff, depth, frames)},
				this.path("create-wavetable")),

			//cmd plot-buffer
			// OSCFunc ({|msg|
			// 	var bufferName, rs;
			// 	bufferName = msg[1];
			// 	rs = buffers.plot(bufferName);
			// 	if (rs,
			// 		{
			// 			postf("Ploting buffer '%'\n", bufferName);
			// 		},{
			// 			postf("Can not plot buffer '%'\n", bufferName);
			// 		})},
			// 	this.path("plot-buffer")),
			
		];
		oscHandlers = ary;
	}
	
} // end LliaHandler
					
