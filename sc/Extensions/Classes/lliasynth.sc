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
    ** Construct instance of LliaSynthInfo.
    ** ARGS:
    **   lliaApp - instance of LliaHandler
    **   stype   - String, synth type.
    **             See Llia.llia.constants.py
    **   id      - int, unique synth serial number.
    **   km      - String, key mode.
    **             See Llia/llia/constants.py
    **   voiceCount - int, number of voices to allocate. voiceCount 
    **                is ignored by some key modes.
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
			