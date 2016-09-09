/*
** lliabuffers.sc 2016.05.01
** LliaBuffer, a helper class to manage buffers.
** 
*/

LliaBuffers : Object {

	var sopts;							// ServerOptions
	var buffers;						// Dictionary
	var protectedBuffers;               // static arracy of protectede buffers 
		

	*bufferDoesNotExistsException {|name|
		var msg = "Buffer '" ++ name.asString ++ "' does not exists.";
		Error(msg).throw;
	}


	
	*new {
		
		^super.new.init();
	}

	init {|app|
		var buf;
		protectedBuffers = ["SINE1", "TRIANGLE", "SAW128", "PULSE20"];
		sopts = ServerOptions.new;
		buffers = Dictionary.new(8);
		// this.sine1("SINE1", [1.0]);
		// this.wave("TRIANGLE", 128, 2.0, 2);
		// this.wave("SAW128");
		// this.wave("PULSE20", 128, 1.0, 5);
	}

	size {
		^buffers.size;
	}

	isProtectedBuffer {|name|
		protectedBuffers.do({|pname|
			if( pname == name,
				{
					^true;
				})})
		^false;
	}

	bufferCount {
		^sopts.numBuffers;
	}

	bufferList {
		^buffers.keys;
	}

	bufferExists {|name|
		var flag = true;
		name = name.asString;
		buffers.atFail(name, {flag=false});
		^flag;
	}

	plot {|name|
		name = name.asString;
		if (this.bufferExists(name),
			{
				var b;
				b = buffers.at(name);
				b.plot(name);
				^true;
			},{
				^false;
			})}
			
	
	addBuffer {|name, frames=1024, numChans=1|
		if (this.bufferExists(name),
			{
				var msg = "WARNING: Buffer '" ++ name.asString ++ "' already exists";
				postln(msg);
				^false;
			},{
				var b = Buffer.alloc(nil, frames, numChans);
				var frmt = "Added buffer '%'  frames: %   channels: %\n";
				buffers.add(name -> b);
				postf(frmt, name, frames, numChans);
				^true;
			})
	}

	getBuffer {|name|
		name = name.asString;
		if (this.bufferExists(name),
			{
				^buffers.at(name);
			},{
				LliaBuffers.bufferDoesNotExistsException(name);
			})
	}

	free {|name|
		if(this.bufferExists(name),
			{
				var b = buffers.at(name);
				b.free;
				buffers.removeAt(name);
			});
	}

	freeAll {
		this.bufferList.do({|name|
			this.free(name)});
	}

	restart {
		this.bufferList.do({|name|
			if( not(this.isProtectedBuffer(name)),
				{
					this.free(name);
				});
		});
	}

	
	*lowpass {|ary, cutoff, depth|
		var acc;
		acc = Array.new;
		ary.do ({|amp, i|
			if (i > cutoff,
				{
					amp = amp * depth;
					depth = depth * depth;
				});
			acc = acc.add(amp)});
		^acc;
	}

	*highpass {|ary, cutoff, depth|
		var acc;
		acc = Array.new;
		cutoff = ary.size-cutoff;
		acc = LliaBuffers.lowpass(ary.reverse, cutoff, depth);
		acc = acc.reverse;
		^acc;
	}

	*bandpass {|ary, center, depth|
		var acc;
		acc = Array.new;
		ary.do ({|amp, i|
			var diff = (center-i).abs;
			var scale = depth**diff;
			acc = acc.add(amp*scale);
		});
		^acc;
	}

	*bandreject {|ary, center, depth|
		var acc, bcc;
		acc = LliaBuffers.lowpass(ary, center, depth);
		acc = LliaBuffers.highpass(acc, center, depth);
		acc = acc.normalize(0.0, 1.0);
		bcc = [];
		acc.do ({|amp|
			bcc = bcc.add(1-amp);
		});
		^bcc;
	}
	
	*filter {|ary, mode, cutoff, depth|
		var acc = [];
		case
			{mode == "lowpass"}
			{acc = LliaBuffers.lowpass(ary, cutoff, depth)}
			
			{mode == "highpass"}
			{acc = LliaBuffers.highpass(ary, cutoff, depth)}
			
			{mode == "bandpass"}
			{acc = LliaBuffers.bandpass(ary, cutoff, depth)}

		    {mode == "bandreject"}
		    {acc = LliaBuffers.bandreject(ary, cutoff, depth)}
		
			{true} 
			{acc = ary};
		^acc;
	}


	/*
    ** harmgen1 generates an array of harmonic amplitudes suitable for use
    ** with sine1.
    ** 
    ** maxHarmonic - int, the maximum harmonic number
    ** decay - int, sets the decay rate for higher harmonics.
    **         for decay = 0 all amplitudes are 1.0
    **         for decay = 1 amplitudes are reciprocal of frequency
    **         for decay = 2 amplitudes are reciprocal of frequency squared.
    ** skip - int, set every nth harmonic to 0, to disable set skip to a value
    **        greater then maxHarmonic.
    ** mode - String, filter,  mode one of: "lowpass", "highpass", "bandpass"
    **        or "bandreject".  Any other value disables the filter.
    ** cutoff - filter cutoff/center in terms of harmonic number.
    ** depth  - float, filter scale factor. 0 < scale <= 1
	*/

	*harmgen1 {|maxHarmonic, decay=1, skip=nil, mode="", cutoff=nil, depth=0.5|
		var acc;
		if (skip == nil, {skip = maxHarmonic+1});
		if (cutoff == nil, {cutoff = maxHarmonic/2});
		acc = [];
		maxHarmonic.do ({|i|
			var freq, skipFlag, amp;
			freq = i+1;
			amp = 1.0/(freq**decay);
			skipFlag = (freq % skip) == 0;
			if (skipFlag, {amp = 0});
			acc = acc.add(amp);
		});
		acc = LliaBuffers.filter(acc, mode, cutoff, depth);
		^acc;
	}

	sine1 {|name, amps, frames=1024|
		if (this.addBuffer(name, frames),
			{
				var b = this.getBuffer(name);
				b.sine1(amps, true, true, true);
				^true;
			},{
				^false;
			})
	}

	/*
    ** Recipes:
    ** sawtooth - use defaut values
    ** sqaure   - skip = 2
    ** triangle - decay = 2, skip = 2
    ** narrow pulse (all amps = 1) - decay = 0
    ** 33% pulse - skip = 3
    ** 25% pulse - skip = 4
    ** 20% pulse - skip = 5
	*/
	wave {|name, maxHarmonic=128, decay=1, skip=nil, mode="", cutoff=nil, depth=0.5, frames=1024|
		if (this.addBuffer(name, frames),
			{
				var b = this.getBuffer(name);
				var amps = LliaBuffers.harmgen1(maxHarmonic, decay, skip, mode, cutoff, depth);
				b = b.sine1(amps, true, true, true);
				^true;
			},{
				^false;
			})
	}
	
	lliaDump {|pad=""|
		var pad2 = pad ++ "    ";
		var blist = this.bufferList.asList;
		postf("%Buffers:\n", pad);
		blist.sort.do({|id|
			var b = this.getBuffer(id);
			var bufnum = b.bufnum;
			var frames = b.numFrames;
			var chans = b.numChannels;
			var sr = b.sampleRate;
			var path = b.path;
			while({id.size < 12},
				{
					id = id ++ " ";
				});
			postf("%% number: %  frames: %  channels: %   sr: %   path: '%'\n",
				pad2, id, bufnum, frames, chans, sr, path);
		});
	}


	
} // end class

	