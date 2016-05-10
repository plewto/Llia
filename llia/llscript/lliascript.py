# llia.llscript.lliscript
# 2016.05.09

from llia.llscript.bufferhelper import BufferHelper
from llia.llscript.synthhelper import SynthHelper
from llia.llscript.parser import LSLParser



def get_lliascript_parser(app):
    parser =  LSLParser(app)
    bufhelper = BufferHelper(parser)
    parser.buffer_helper = bufhelper
    synthhelper = SynthHelper(parser)
    parser.synth_helper = synthhelper
    return parser



