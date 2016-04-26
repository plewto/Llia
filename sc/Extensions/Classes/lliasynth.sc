/*
** lliasynth.sc  2016.04.20
**
** Wrapper class for KeymodeObject.
*/

LliaSynthInfo : Object {

	var <oscID;
	var <globalAppID;
	var <synthType;
	var <keymodeName;
	var keymodeObject;
	var <buses;   // list (inbus, outbus)
	var vcount;  // voice count


	/*
	** Create new LliaSynthInfo instance.
    ** ARGS:
    **   stype - String, a Synth name, See Llia.docs.synthtypes
    **   id    - Int, numeric synth id, id = 1,2,3,...
    **           id used as part of the OSC path and must be unique
    **           for each synthtype.
    **           The final OSC path to this synth becomes:
	**           /llia/stype/id/
    **
    **   km    - String, the keymode. See Llia.docs.keymodes
    **   outbus - Audio outbut bus
    **   inbus  - Optional audio input bus
    **   voiceCount - Optional number of synths to allocate.
    **                Some keymodes will ignore this value.
    */    
	*new {|stype, id, globalID, km, outbus, inbus, voiceCount|
		^super.new.init(stype, id, globalID, km, outbus, inbus, voiceCount);
	}

	init {|stype, id, globalID, km, outbus, inbus, voiceCount|
		oscID = id.asString;
		globalAppID = globalID.asString;
		synthType = stype;
		keymodeName = km.asString;
		buses = [inbus, outbus];
		vcount = voiceCount;
		keymodeObject = case
		    {keymodeName == "Poly1"}
		    {Poly1.new(synthType, id, globalAppID)}

		    {keymodeName == "Mono1"}
		    {Mono1.new(synthType, id, globalAppID)}

		    {keymodeName == "EFX"}
		    {EfxKeymode.new(synthType, id, globalAppID)}

		    {True == True}
		    {error("Invalid Llia keymode '"++km.asString++"'")};

		keymodeObject.outbus_(outbus);
		keymodeObject.inbus_(inbus);
	}

	/*
    ** Free this instance and all resources under it.
	*/
	free {
		keymodeObject.free;
		synthType = "Freed " ++ synthType;
	}

	/*
    ** All notes off.
    */
	panic {
		keymodeObject.allNotesOff;
	}

	lliaDump {|pad=""|
		var pad2 = pad++"    ";
		var pad3 = pad2++"    ";
		postf("%LliaSynthInfo:\n", pad);
		postf("%synthType: '%',   oscID: '%'\n", pad2, synthType, oscID);
		postf("%keymode: %\n", pad2, keymodeName);
		postf("%inbus  : %\n", pad3, buses[0]);
		postf("%outbus : %\n", pad3, buses[1]);
		postf("%voice count : %\n", pad3, vcount);
		keymodeObject.lliaDump(pad2);
	}

}
			