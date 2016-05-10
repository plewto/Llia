# llia.lsl.lliscript
# 2016.05.09

from llia.lsl.bufferhelper import BufferHelper
from llia.lsl.parser import LSLParser



def get_lliascript_parser(app):
    parser =  LSLParser(app)
    bufhelper = BufferHelper(parser)
    parser.buffer_helper = bufhelper

    return parser



