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
	var <keymodeObject;
	var vcount;   // voice count
	var <>isEfx;


	/*
	** Create new LliaSynthInfo instance.
    ** ARGS:
	** lliaApp - Instance of LliaHandler	
    **   stype - String, a Synth name, See Llia.docs.synthtypes
    **   id    - Int, numeric synth id, id = 1,2,3,...
    **           id used as part of the OSC path and must be unique
    **           for each synthtype.
    **           The final OSC path to this synth becomes:
	**           /llia/stype/id/
    **   km       - String, the keymode. See Llia.docs.keymodes
    **   voiceCount - Optional number of synths to allocate.
    **                Some keymodes will ignore this value.
    */    
	*new {|lliaApp, stype, id, globalID, km, voiceCount|
		^super.new.init(lliaApp, stype, id, globalID, km, voiceCount);
	}

	init {|lliaApp, stype, id, globalID, km, voiceCount|
		oscID = id.asString;
		globalAppID = globalID.asString;
		synthType = stype;
		keymodeName = km.asString;
		vcount = voiceCount;
		isEfx = false;
		keymodeObject = case
		    {keymodeName == "Poly1"}
		    {Poly1.new(lliaApp, synthType, oscID, globalAppID)}

		    {keymodeName == "PolyN"}
		    {PolyN.new(lliaApp, synthType, oscID, globalAppID, voiceCount)}
		
		    {keymodeName == "PolyRotate"}
		    {PolyRotate.new(lliaApp, synthType, oscID, globalAppID, voiceCount)}
		
		    {keymodeName == "Mono1"}
		    {Mono1.new(lliaApp, synthType, oscID, globalAppID)}

		    {keymodeName == "MonoExclusive"}
		    {MonoExclusive.new(lliaApp, synthType, oscID, globalAppID)}
		
		    {keymodeName == "EFX"}
		    {EfxKeymode.new(lliaApp, synthType, oscID, globalAppID)}

		    {True == True}
		    {error("Invalid Llia keymode '"++km.asString++"'")};
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
		postf("%keymode : %\n", pad2, keymodeName);
		postf("%voice count : %\n", pad3, vcount);
		keymodeObject.lliaDump(pad2);
	}

}
			