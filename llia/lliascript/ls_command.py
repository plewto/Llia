# llia.lliascript.ls_command
# 2016.05.15

from __future__ import print_function
from llia.lliascript.ls_constants import *

class LsCommand(object):

    def __init__(self, parser):
        self.parser = parser
        self.proxy = parser.proxy
        self.config = parser.config

    @staticmethod
    def list_targets():
        msg  = """
        The ls command is used to list various types of information.
        Use help for more general help.

        ls(target)  

        Where target is one of:

        ABUS     - list audio buses
        CBUS     - list control busses
        BUFFER   - list buffers
        SYNTH    - list all active synths
        EFX      - list all active effects synths
        CHAN     - list MIDI channel names
        CTRL     - list MIDI controller names
        STYPE    - list recognized synth, efx types
        KEYMODE  - list recognized keymodes
        """
        print(msg)
        return [ABUS, CBUS, BUFFER, SYNTH, EFX, CHAN, CTRL, STYPE, KEYMODE]

    def ls(self, target=None):
        if not target:
            return self.list_targets()
        elif target == ABUS:
            return self.proxy.list_audio_buses()
        elif target == CBUS:
            return self.proxy.list_control_buses()
        elif target == BUFFER:
            return self.proxy.list_buffers()
        elif target == SYNTH:
            return self.proxy.list_synths()
        elif target == EFX:
            return self.proxy.lsit_efx()
        elif target == CHAN:
            print("MIDI Channels:")
            acc = []
            for i in range(16):
                name = self.config.channel_assignments[i+1]
                acc.append(name)
            print(self.config.channel_assignments)
            return acc
        elif target == CTRL:
            acc = []
            print("MIDI Controllers:")
            for i in range(128):
                name = self.config.controller_assignments[i]
                acc.append(name)
            print(self.config.controller_assignments)
            return acc
        elif target == STYPE:
            acc = [SYNTH_TYPES, EFFECT_TYPES]
            print("Synth Types:")
            for q in sorted(SYNTH_TYPES):
                print("    %s" % q)
            print("EFX Types:")
            for q in sorted(EFFECT_TYPES):
                print("   %s" % q)
            return acc
        elif target == KEYMODE:
            acc = sorted(KEY_MODES)
            print("Key modes:")
            for a in acc:
                print("   %s" % a)
            return acc
        else:
            msg = "Invalid ls target: %s" % target
            self.parser.warning(msg)
            return []
