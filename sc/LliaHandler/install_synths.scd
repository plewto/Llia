/*
** Install SuperCollider Synths
*/

(
~manifest=["algo.scd",
    "asplit.scd",
    "bandpass.scd",
    "carnal.scd",
    "cascade.scd",
    "chronos.scd",
    "corvus.scd",
    "crusher.scd",
    "ctrlmixer.scd",
    "cutil.scd",
    "envgen.scd",
    "flngr.scd",
    "fm2.scd",
    "formant.scd",
    "ghostbus.scd",
    "hund.scd",
    "io.scd",
    "klstr.scd",
    "lfo1.scd",
    "lfo2.scd",
    "lfo3.scd",
    "m.scd",
    "masa.scd",
    "mixer.scd",
    "notch.scd",
    "orgn.scd",
    "panner.scd",
    "pitchshifter.scd",
    "prism.scd",
    "qmod.scd",
    "rdrum.scd",
    "ringmodulator.scd",
    "rumklang.scd",
    "saw3.scd",
    "snh.scd",
    "ss1.scd",
    "tremolo.scd",
    "xover.scd"];

    ~manifest.do({|fname|
        postf("Installing '%'\n", fname);
        fname.load;
    });
    )
    