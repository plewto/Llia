/*
** lliabuffers.sc 2016.05.01
** LliaBuffer, a helper class to manage buffers.
** 
*/

LliaBuffers : Object {

	var sopts;							// ServerOptions
	var buffers;						// Dictionary

	*bufferDoesNotExistsException {|id|
		var msg = "Buffer '" ++ id.asString ++ "' does not exists.";
		Error(msg).throw;
	}

	*new {
		^super.new.init();
	}

	init {
		sopts = ServerOptions.new;
		buffers = Dictionary.new(8);
	}

	size {
		^buffers.size;
	}
	
	bufferCount {
		^sopts.numBuffers;
	}

	bufferList {
		^buffers.keys;
	}

	bufferExists {|id|
		var flag = true;
		buffers.atFail(id, {flag=false});
		^flag;
	}

	addBuffer {|id, frames=1024, numChans=1|
		if (this.bufferExists(id),
			{
				var msg = "WARNING: Buffer '" ++ id.asString ++ "' already exists";
				postln(msg);
				^false;
			},{
				var b = Buffer.new(nil, frames, numChans);
				buffers.add(id -> b);
				^true;
			})
	}

	getBuffer {|id|
		if (this.bufferExists(id),
			{
				^buffers.at(id);
			},{
				LliaBuffers.bufferDoesNotExistsException(id);
			})
	}

	free {|id|
		if(this.bufferExists(id),
			{
				var b = buffers.at(id);
				b.free;
				buffers.removeAt(id);
			});
	}

	freeAll {
		this.bufferList.do({|id|
			this.free(id)});
	}
	
	sine1 {|id, amps, frames=1024|
		if (this.addBuffer(id, frames),
			{
				var b = this.getBuffer(id);
				b.sine1(amps, true, true, true);
				^true;
			},{
				^false;
			})
	}

	sine {|id="sine", frames=1024|
		^this.sine1(id, [1.0], frames);
	}
			
	sawtooth {|id="sawtooth", harmonics=16, frames=1024|
		var acc = List.new;
		harmonics.do({|n|
			var freq = n+1;
			var amp = 1.0/freq;
			acc.add(amp)});
		^this.sine1(id, acc, frames);
	}

	square {|id="square", harmonics=16, frames=1024|
		var acc = List.new;
		harmonics.do({|n|
			var freq = (n+1)*2-1;
			var amp = 1.0/freq;
			acc.add(amp)});
		^this.sine1(id, acc, frames);
	}

	triangle {|id="triangle", harmonics=16, frames=1024|
		var acc = List.new;
		harmonics.do({|n|
			var freq = (n+1)*2-1;
			var amp = 1.0/(freq*freq);
			acc.add(amp)});
		^this.sine1(id, acc, frames);
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

	