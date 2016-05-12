# llia.llscript.lsutil
# 2016.05.09

from __future__ import print_function

from llia.llerrors import LliascriptParseError

def expect(ttype, token):
    if ttype == "str":
        return token
    elif ttype == "strint":
        try:
            value = int(token)
        except ValueError:
            value= token
            return value
    elif ttype == "int":
        try:
            value = int(token)
            return value
        except ValueError:
            msg = "Expected int, encountered %s" % token
            raise LliascriptParseError(msg)
    elif ttype == "float":
        try:
            value = float(token)
            return value
        except ValueError:
            msg = "Expected float, encounterd %s" % token
            raise LliascriptParseError(msg)
    else:
        return token


def parse_required_args(tokens, required_args):
    acc = []
    min_count = len(required_args)
    if len(tokens) < min_count:
        msg = "Expected at least %d tokens, found %d"
        msg = msg % (min_count, len(tokens))
        raise LliascriptParseError(msg)
    # Required args
    for i,exptype in enumerate(required_args):
        token = tokens[i]
        value = expect(exptype, token)
        acc.append(value)
    return acc

def parse_positional_args(tokens, required_args, opt_args=[]):
    acc = parse_required_args(tokens, required_args)
    index = len(required_args)
    for j,arg in enumerate(opt_args):
        try:
            token = tokens[index]
        except IndexError:
            token = arg[1]
        exptype = arg[0]
        value = expect(exptype, token)
        acc.append(value)
        index += 1
    return acc

def parse_keyword_args(tokens, required_args, order=[], keyword_args={}):
    acc = parse_required_args(tokens, required_args)
    bcc = {}
    index = len(required_args)
    while index < len(tokens):
        try:
            kw = tokens[index].lower()
            token = tokens[index+1]
            try:
                spec = keyword_args[kw]
            except KeyError:
                msg = "Unexpected keyword %s" % kw
                raise LliascriptParseError(msg)
            value = expect(spec[0], token)
            bcc[kw] = value
        except IndexError:
            msg = "Expected matching keyword/value pairs"
            raise LliascriptParseError(msg)
        index += 2
    for kw in order:
        kw = kw.lower()
        dflt = keyword_args[kw][1]
        value = bcc.get(kw, dflt)
        acc.append(value)
    return acc
            
