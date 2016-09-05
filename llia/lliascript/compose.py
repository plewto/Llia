# llia.lliascript.compose
# 2016.05.19

from llia.lliascript.synthhelper import SynthHelper


fill_outbus_args = SynthHelper.fill_outbus_args

class Composer(object):

    def __init__(self, parser):
        self.parser = parser

    def build(self):
        code = "from __future__ import print_function\n\n"
        code += self._build_channel_assignments()
        code += self._build_controller_assignments()
        code += self._build_audio_buses()
        code += self._build_control_buses()
        code += self._build_buffers()
        code += self._build_synths()
        code += self._build_audio_bus_assignments()
        code += self._build_control_bus_assignments()
        code += self._build_buffer_assignments()
        code += 'show_group("ALL")\n'
        return code

    @staticmethod
    def is_protected_bus(name):
        return name[:4] == "out_" or name[:3] == "in_"
    
    def _build_audio_buses(self):
        code = "# Audio buses\n"
        for e in self.parser.entities.values():
            if e.lstype == "abus":
                name = e.lsid
                if not self.is_protected_bus(name):
                    try:
                        chan = int(e.data["channels"])
                    except KeyError:
                        chan = 1
                    code += 'abus("%s", %d)\n' % (name, chan)
        code += "\n"
        return code

    
    def _build_control_buses(self):
        code = "# Control buses\n"
        for e in self.parser.entities.values():
            if e.lstype == "cbus":
                name = e.lsid
                try:
                    chan = int(e.data["channels"])
                except KeyError:
                    chan = 1
                code += 'cbus("%s", %d)\n' % (name, chan)
        code += "\n"
        return code

    def _build_buffers(self):
        code = "# Buffers\n"
        for e in self.parser.entities.values():
            if e.lstype == "buffer":
                filename = e.data["filename"]
                if filename:    # ISSUE: FIX ME
                    msg = "Can not as yet rebuild buffer from filename. "
                    msg += " %s '%s'" % (e.name, filename)
                    self.warning(msg)
                else:
                    if e.data.has_key("is-wavetable"):
                        code += 'wavetab("%s", ' % e.lsid
                        code += '%d, ' % int(e.data["harmonics"])
                        code += '%f, ' % float(e.data["decay"])
                        code += '%d, ' % int(e.data["skip"])
                        code += '%d, ' % int(e.data["cutoff"])
                        code += '"%s", ' % e.data["mode"]
                        code += '%f, ' % float(e.data["depth"])
                        code += '%d)\n' % int(e.data["frames"])
                    else:
                        code += 'buffer("%s",' % e.lsid
                        code += '%d,' % int(e.data["frames"])
                        code += '%d)\n' % int(e.dta["channels"])
        code += "\n"
        return code

    def _build_synths(self):
        acc = []
        for e in self.parser.entities.values():
            print("DEBUG parse, e.lstype = ", e.lstype)
            if e.lstype == "synth" or e.lstype == "group":
                acc.append(e)
        acc.sort(key=lambda x: x.data["serial-number"])
        code = "# Synths\n"
        for e in acc:
            if e.data["is-efx"]:
                code += 'efx("%s", ' % e.data["stype"]
                code += '%d, ' % int(e.data["id"])
                outbus,param,offset = fill_outbus_args(e.data["outbus"])
                code += '["%s","%s",%d])\n' % (outbus,param,offset)
            elif e.data["is-group"]:
                name = e.data["name"]
                code += 'group("%s")\n' % name
            else:
                # Assume an instrumental synth
                code += 'synth("%s", ' % e.data["stype"]
                code += '%d, ' % int(e.data["id"])
                code += '"%s", ' % e.data["keymode"]
                code += '%d, ' % int(e.data["voice-count"])
                outbus,param,offset = fill_outbus_args(e.data["outbus"])
                code += '["%s", "%s", %d])\n' % (outbus,param,offset)
            code += "create_editor()\n"
            # Load bank
            sy = self.parser.synthhelper.get_synth()
            bnk = sy.bank()
            fname = bnk.filename
            if fname:
                code += 'try:\n'
                code += '    load_bank("%s")\n' % fname
                code += 'except Error as err:\n'
                code += '    print(\'ERROR: can not load bank file "%s"\' % fname)\n'
                code += '    print(type(err))\n'
                code += '    print(err.message)\n'
        code += "\n"
        return code
    
    def _build_buffer_assignments(self):
        code = "# Buffer Assignments\n"
        for e in self.parser.entities.values():
            if e.lstype == "buffer-assignment":
                param = e.data["param"]
                bname = e.data["buffer-name"]
                sid = e.data["sid"]
                code += 'assign("%s", "%s", sid="%s")\n' % (param,bname,sid)
        code += "\n"
        return code

    def _build_audio_bus_assignments(self):
        code = "# Audio bus assignments\n"
        for e in self.parser.entities.values():
            if e.lstype == "audio-bus-assignment":
                param = e.data["param"]
                bname = e.data["bus-name"]
                offset = int(e.data["offset"])
                sid = e.data["sid"]
                code += 'assign("%s", "%s", %d, "%s")\n' % (param,bname,offset,sid)
        code += "\n"
        return code

    def _build_control_bus_assignments(self):
        code = "# Control bus assignments\n"
        for e in self.parser.entities.values():
            if e.lstype == "control-bus-assignment":
                param = e.data["param"]
                bname = e.data["bus-name"]
                offset = int(e.data["offset"])
                sid = e.data["sid"]
                code += 'assign("%s", "%s", %d, "%s")\n' % (param,bname,offset,sid)
        code += "\n"
        return code

    def _build_channel_assignments(self):
        code = "# MIDI Channel Assignments\n"
        config = self.parser.config
        for i in range(16):
            c = i+1
            name = config.channel_name(c)
            try:
                int(name)
            except ValueError:
                code += 'channel_name(%d, "%s")\n' % (c, name)
        code += "\n"
        return code
                
    def _build_controller_assignments(self):
        code = "# MIDI Controller Assignments\n"
        config = self.parser.config
        for ctrl in range(128):
            name = config.controller_name(ctrl)
            try:
                int(name)
            except ValueError:
                code += 'controller_name(%d, "%s")\n' % (ctrl, name)
        code += "\n"
        return code
