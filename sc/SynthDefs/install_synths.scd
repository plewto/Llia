/*
** Installs Llia SyntDefs.
*/

(
~manifesat = [ "asplit.scd",
	"carnal.scd",
	"flngr.scd",
	"fm2.scd",
	"ghostbus.scd",
	"klstr.scd",
	"lfo1.scd",
	"lfo2.scd",
	"lfo3.scd",
	"masa.scd",
	"mixer.scd",
	"orgn.scd",
	"panner.scd",
	"pulsegen.scd",
	"rdrum.scd",
	"saw3.scd",
	"snh.scd",
	"testtones.scd",
	"tremolo.scd",
	"xover.scd"];


~manifest.do({|fname|
	postf("Installing '%'\n", fname);
	fname.load;
});
)