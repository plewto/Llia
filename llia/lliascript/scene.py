# llia.lliascript.scene
# 2017.04.09

from __future__ import print_function

import llia.constants as con
from llia.lliascript.compose import Composer


class Scene(Composer):

    def __init__(self, parser):
        super(Scene, self).__init__(parser)

    def create_script(self):
        code = "# LLia Scene\n"
        code += "# Version %s\n\n" % str(con.VERSION)
        code += "from __future__ import print_function\n\n"
        code += self.build_channel_assignments()
        code += self.build_controller_assignments()
        code += self.build_audio_buses()
        code += self.build_control_buses()
        code += self.build_buffers()
        code += self.build_synths(load_banks=False)
        code += self.build_bus_assignments()
        code += self.build_buffer_assignments()
        code += self.build_graph()
        code += 'show_group("ALL")\n'
        return code
    
    def serialize(self):
        script = self.create_script()
        synths = self.parser.proxy.get_all_synths()
        bank_data = {}
        current_slots = {}
        for sy in synths:
            sid = sy.sid
            bnk = sy.bank()
            bank_data[sid] = bnk.serialize()
            current_slots[sid] = bnk.current_slot
        data = {"script" : self.create_script(),
                "bank_data" : bank_data,
                "current_slots" : current_slots}
        return data

