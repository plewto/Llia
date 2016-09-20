# llia.lliascript.compose
# 2016.05.19

from llia.lliascript.synthhelper import SynthHelper


#fill_outbus_args = SynthHelper.fill_outbus_args

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
        code += self._build_bus_assignments()
        code += self._build_buffer_assignments()
        code += 'show_group("ALL")\n'
        return code

    @staticmethod
    def is_protected_audio_bus(name):
        return name[:4] == "out_" or name[:3] == "in_"
    
    def _build_audio_buses(self):
        code = "# Audio buses\n"
        for e in self.parser.entities.values():
            if e.lstype == "abus":
                name = e.lsid
                if not self.is_protected_audio_bus(name):
                    code += 'abus("%s")\n' % name
        code += "\n"
        return code


    @staticmethod
    def is_protected_control_bus(name):
        return name.startswith("null_")
    
    def _build_control_buses(self):
        code = "# Control buses\n"
        for e in self.parser.entities.values():
            if e.lstype == "cbus":
                name = e.lsid
                if not self.is_protected_control_bus(name):
                    code += 'cbus("%s")\n' % name
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
        def predicate(obj):
            return obj.lstype == 'synth' or obj.lstype == 'group'
        acc = filter(predicate, self.parser.entities.values())
        acc.sort(key=lambda x: x.data["serial-number"])
        code = "# Synths\n"
        for e in acc:
            if e.data['is-group']:
                code += 'group("%s")\n' % e.data['name']
            elif e.data['is-control-synth']:
                code += 'control_synth("%s")\n' % e.data['stype']
            elif e.data['is-efx']:
                code += 'efx("%s")\n' % e.data["stype"]
            else:
                stype = e.data['stype']
                kmode = e.data['keymode']
                vcount = e.data['voice-count']
                code += 'synth("%s","%s",%s)\n' % (stype,kmode,vcount)
            code += 'create_editor()\n'
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
  
    def _build_bus_assignments(self):
        proxy = self.parser.app.proxy
        aob = aib = cob = cib = ""
        for sy in proxy.get_all_synths():
            specs = sy.specs
            sid = sy.sid
            
            for param,junk in specs["audio-output-buses"]:
                bn = sy.get_audio_output_bus(param)
                aob+='assign_audio_output("%s","%s","%s")\n'%(param,bn,sid)

            for param,junk in specs["audio-input-buses"]:
                bn = sy.get_audio_input_bus(param)
                aib+='assign_audio_input("%s","%s","%s")\n'%(param,bn,sid)

            for param,junk in specs["control-output-buses"]:
                bn = sy.get_control_output_bus(param)
                cob+='assign_control_output("%s","%s","%s")\n'%(param,bn,sid)

            for param,junk in specs["control-input-buses"]:
                bn = sy.get_control_input_bus(param)
                cib+='assign_control_input("%s","%s","%s")\n'%(param,bn,sid)
        code = "\n# Audio bus assignments\n"
        code += aob
        code += aib
        code += "\n# Control bus assignments\n"
        code += cob
        code += cib
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
