# llia.lliascript.compose
# 2016.05.19

from __future__ import print_function

import llia.constants as con
from llia.lliascript.synthhelper import SynthHelper

class Composer(object):

    """
    Composer constructs a Python script which may be used to reconstruct
    the current state of Llia.
    """

    def __init__(self, parser):
        self.parser = parser

    def get_synth(self, sid):
        return self.parser.app.proxy.get_synth(sid)
        
    def build(self):
        code = "# Llia Compose script\n"
        code += "# Version %s\n\n" % str(con.VERSION)
        code = "from __future__ import print_function\n\n"
        code += self.build_channel_assignments()
        code += self.build_controller_assignments()
        code += self.build_audio_buses()
        code += self.build_control_buses()
        code += self.build_buffers()
        code += self.build_synths()
        code += self.build_bus_assignments()
        code += self.build_buffer_assignments()
        code += self.build_graph()
        code += 'show_group("ALL")\n'
        return code

    @staticmethod
    def is_protected_audio_bus(name):
        return name[:4] == "out_" or name[:3] == "in_"
    
    def build_audio_buses(self):
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
    
    def build_control_buses(self):
        code = "# Control buses\n"
        for e in self.parser.entities.values():
            if e.lstype == "cbus":
                name = e.lsid
                if not self.is_protected_control_bus(name):
                    code += 'cbus("%s")\n' % name
        code += "\n"
        return code

    def build_buffers(self):
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

    def _load_bank(self,e):
        sid = e.lsid
        bank = self.get_synth(sid).bank()
        fn = bank.filename
        bcc = ""
        if fn:
            bcc += 'load_bank("%s",sid="%s")\n' % (fn,sid)
        cp = bank.current_slot
        bcc += 'program(%d)\n' % cp
        return bcc
    
    def build_synths(self, load_banks=True):
        def predicate(obj):
            return obj.lstype == 'synth' or obj.lstype == 'group'
        acc = filter(predicate, self.parser.entities.values())
        acc.sort(key=lambda x: x.data["serial-number"])
        code = "# Synths\n"
        for e in acc:
            if e.data['is-group']:
                code += 'group("%s")\n' % e.data['name']
            else:
                sid = e.lsid
                sy = self.get_synth(sid)
                code += '# -------------------- Synth: %s\n' % sid
                if e.data['is-control-synth']:
                    code += 'control_synth("%s")\n' % e.data['stype']
                elif e.data['is-efx']:
                    code += 'efx("%s")\n' % e.data["stype"]
                else:
                    stype = e.data['stype']
                    kmode = e.data['keymode']
                    vcount = e.data['voice-count']
                    code += 'synth("%s","%s",%s)\n' % (stype,kmode,vcount)
                code += 'keytable("%s",silent=True)\n' % sy.keytable()
                code += 'extended_mode(%s,%d,nosync=True)\n' % (sy.extended_mode, sy.extended_count)
                code += 'midi_input_channel(%d,silent=True)\n' % sy.midi_input_channel()
                code += 'create_editor()\n'
                if load_banks:
                    code += self._load_bank(e)
                ed = sy.synth_editor
                for akey in ed.annotation_keys():
                    txt = ed.get_annotation(akey)
                    code += 'set_annotation("%s","%s")\n' % (akey,txt)
        return code
    
    def build_buffer_assignments(self):
        code = "# Buffer Assignments\n"
        for e in self.parser.entities.values():
            if e.lstype == "buffer-assignment":
                param = e.data["param"]
                bname = e.data["buffer-name"]
                sid = e.data["sid"]
                code += 'assign("%s", "%s", sid="%s")\n' % (param,bname,sid)
        code += "\n"
        return code
  
    def build_bus_assignments(self):
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
    
    def build_channel_assignments(self):
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
                
    def build_controller_assignments(self):
        code = "# MIDI Controller Assignments\n"
        config = self.parser.config
        for ctrl in range(128):
            name = config.controller_name(ctrl)
            try:
                int(name)
            except ValueError:
                code += 'controller_name(%d, "%s", silent=True)\n' % (ctrl, name)
        code += "\n"
        return code

    def build_graph(self):
        gh = self.parser.graphhelper
        code = "# Create graph\n"
        code += "graph_sync()\n"   # Force graph creation 
        for tid,t in gh.synth_tokens():
            pos = t.position()
            code += 'graph_move_token("%s",%d,%d,sync=False)\n' % (tid,pos[0],pos[1])
        for tid,t in gh.audio_bus_tokens():
            pos = t.position()
            code += 'graph_move_token("%s",%d,%d,sync=False)\n' % (tid,pos[0],pos[1])
        for tid,t in gh.control_bus_tokens():
            pos = t.position()
            code += 'graph_move_token("%s",%d,%d,sync=False)\n' % (tid,pos[0],pos[1])
        code += 'graph_sync()\n'
        return code
        
