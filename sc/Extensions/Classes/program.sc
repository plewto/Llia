/*
** program.sc 2015.12.04
*/

Program : Object {

	var pformat;
	var pname;
	var pdata;

	*new {|name="Init", format=\Generic|
		^super.new.init(name, format);
	}

	init {|name="Init", format=\Generic|
		this.name = name;
		pformat = format;
		pdata = IdentityDictionary.new;
	}

	name {
		^pname;
	}

	name_ {|str|
		pname = str;
		^str;
	}

	format {
		^pformat;
	}

	clear {
		pdata = IdentityDictionary.new;
	}

	synthParams {
		^pdata.getPairs;
	}

	getPairs {  // alias for synthParams
		^pdata.getPairs;
	}
	
	synthParams_ {|plist, clearFirst=true|
		if (clearFirst, {this.clear});
		pdata.putPairs(plist);
		^plist;
	}

	set_ {|param, value|
		pdata.put(param, value);
	}
	
	clone {
		var p = Program.new(this.name, this.format);
		p.synthParams_(this.synthParams);
		^p;
	}

			
}