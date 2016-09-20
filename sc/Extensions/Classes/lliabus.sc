/*
** lliabus.sc
** LliaBuses, a helper class to manage bus assignments
*/


LliaBuses : Object {
	
	var sopts;							// ServerOptions
	var <rate;							// Symbol 'audio' or 'control'
	var <busCount;						// int
	var buses;							// Dictionary
	var protectedControlBuses = 2;

	*busDoesNotExistsException {|srate, id|
		var msg = srate.asString + "bus '";
		msg = msg ++ id.asString ++"' does not exists.";
		Error(msg).throw;
	}

	/*
    ** Creates new instance of LliaBuses
    ** ARGS:
    **   srate - symbol, either \audio or \control.
    **           any other value throws an exception.
	**
    ** For audio rate the first n "public" buses are automatically 
    ** included.  These buses have names in_x and out_x where x
    ** is an integer.
	*/
	*new {|srate|
		^super.new.init(srate);
	}
	
	init {|srate|
		sopts = ServerOptions.new;
		if (srate == \audio,
			{
				busCount = sopts.numAudioBusChannels;
				rate = srate;
			},{
				if (srate == \control,
					{
						busCount = sopts.numControlBusChannels;
						rate = srate;
					},{
						var msg = "Invalid LliaBus rate.";
						msg = msg + "Expected either 'audio' or 'control',";
						msg = msg + "encountered:" + srate.asString;
						Error(msg).throw;
					})
			});
		if (srate == \audio,
			{
				var nOut = sopts.numOutputBusChannels;
				var nIn = sopts.numInputBusChannels;
				var fpb = sopts.firstPrivateBus;
				buses = Dictionary.new(fpb+8);
				nOut.do({|n|
					var name = "out_" ++ n.asString;
					buses.add(name -> Bus.new(\audio, n, 1))});
				nIn.do({|n|
					var index = n+nOut;
					var name = "in_" ++ n.asString;
					buses.add(name -> Bus.new(\audio, index, 1))});
			},{
                /*
                **  Defines set of "protected" control buses.
                **  These buses either provide default control input/output
                **  or they provide a constant value.
                **
                **  null_source -> A default control input bus, 
                **                 values on this bus should be ignored.
                **  null_zero   -> A bus with constant value 0, 
                **                 values should never be placed on this bus.
                **  null_one    -> A bus with constant value 1, 
                **                 values should never be placed on this bus.
                **  null_sink   -> A default control output bus.
                **                 values may freely be placed on this bus
                **                 but it should never be used for control input.
                */
                var zeroBus, oneBus;
                zeroBus = Bus.control(); 
                zeroBus.value = 0;
                oneBus = Bus.control();
                oneBus.value = 1;
                buses = Dictionary.new(8);
                buses.add("null_source" -> Bus.control());
                buses.add("null_sink" -> Bus.control());
                buses.add("null_source_zero" -> zeroBus);
                buses.add("null_source_one" -> oneBus);
            });
    } // end init

	size {
		^buses.size;
	}
	
	/*
    ** Returns: 
    **    Set - an unsorted list of all assigned bus names.
    */         
	busList {
		^buses.keys;
	}

	/*
    ** Predicate, test existence of bus.
    ** ARGS:
    **   id - String
    ** RETURNS:
    **   bool
    */
	busExists {|id|
		var flag = true;
		buses.atFail(id, {flag=false});
		^flag;
	}

	/*
	** Adds a new bus assignment.
    ** ARGS:
    **   id       - String, the bus name.  If a bus with the same name 
    **              already exists, a warning message is displayed and
    **              the existing bus is left in place.
    **   numChans - optional int, The number of channels, default 1.
    **
	** RETURNS:
    **   bool - true  -> if a new assignment was made.
    **          false -> bus already exists.
	*/
	
	addBus {|id, numChans=1|
		var b;
		id = id.asString;
		numChans = numChans.asInt;
		if (this.busExists(id),
			{
				var msg = "WARNING: Attempt to replace existing";
				msg = msg + rate.asString + "bus '" + id.asString + "'";
				postln(msg);
				^false;
			},{
				var b, msg;
				if (rate == \audio,
					{
						b = Bus.audio(nil, numChans);
					},{
						b = Bus.control(nil, numChans);
					});
				buses.add(id -> b);
				postf("Added % bus: '%' with % channels.\n", rate, id, numChans);
				^true;
			});
	}


	
	/*
    ** Retrieve the Bus object associated with id.
    ** ARGS:
    **   id - String.
    ** RETURNS:
    **   Bus
    ** Throws exception if bus does not exists. 
    */
	getBus {|id|
		if (this.busExists(id),
			{
				^buses.at(id);
			},{
				LliaBuses.busDoesNotExistsException(rate, id);
			});
	}

	/*
    ** Retrieve bus index associated with id.
    ** ARGS:
    **   id     - String
    **   offset - optional int, an offset added to bus index.
    ** RETURNS:
    **   int 
    ** Throws exception if bus does not exists.
	*/
	getBusIndex {|id, offset=0|
		var b = this.getBus(id);
		var i = b.index;
		^(i+offset);
	}

	/*
    ** Free indicated bus.  
    ** The first n public audio input and outbus buses
    ** can not be freed.  Attempts to do so are ignored.
    ** ARGS:
    **   id - String
    ** 
	*/	
	free {|id, verbose=1|
		if (this.busExists(id),
			{
				var b = this.getBus(id);
				var index = b.index;
				if (rate == \audio,
					{
						var fpb = sopts.firstPrivateBus;
						if (index >= fpb,
							{
								b.free;
								buses.removeAt(id);
							});
					},{
						if (index >= protectedControlBuses,{
							b.free;
							buses.removeAt(id);
						});
					});
				if (verbose==1, {
					postf("% bus '%' freed\n", rate, id);
				});
			});
	}

	restart {
		buses.keys.do({|b|
			this.free(b, 0);
		});
	}

	
	
	/*
    ** Free all buses manged by this.
    ** The first n public audio input and output buses are not molested.
	*/
	freeAll {
		this.busList.do({|id|
			var b = buses.at(id);
			b.free;
		});
	}
	
	lliaDump {|pad=""|
		var pad2 = pad ++"    ";
		var blist = this.busList.asList;
		postf("%% buses:\n", pad, rate);
		blist.sort.do({|id|
			var b = this.getBus(id);
			var i = b.index;
			var n = b.numChannels;
			while({id.size < 12},
				{
					id = id ++ " ";
				});
			postf("%% -> index %  channels %\n", pad2, id, i, n);});
	}
	
} // end class
	
		