/*
** Install SuperCollider Synths
*/

(
~manifest=["asplit.scd",
    "carnal.scd",
    "cascade.scd",
    "chronos.scd",
    "crusher.scd",
    "ctrlmixer.scd",
    "flngr.scd",
    "fm2.scd",
    "ghostbus.scd",
    "grayhound.scd",
    "klstr.scd",
    "lfo1.scd",
    "lfo2.scd",
    "lfo3.scd",
    "masa.scd",
    "mixer.scd",
    "orgn.scd",
    "panner.scd",
    "pitchshifter.scd",
    "qmod.scd",
    "rdrum.scd",
    "ringmodulator.scd",
    "rumklang.scd",
    "saw3.scd",
    "snh.scd",
    "tremolo.scd",
    "xover.scd"];

    ~manifest.do({|fname|
        postf("Installing '%'\n", fname);
        fname.load;
    });
    )
    