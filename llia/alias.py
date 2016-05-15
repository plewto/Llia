# llia.alias.py
# 2016.02.20
# Assigns local MIDI controller and channel names.
#

from __future__ import print_function
import json
from ConfigParser import NoOptionError, NoSectionError

from llia.generic import dump



class CCAssignments(object):

    """CCAssignments associates name with MIDI controller number."""
    
    MAX_NAME_LENGTH = 12
    
    def __init__(self, config_parser=None):
        """
        Construct new CCAssignments object.

        ARGS:
          config_parser - Optional configuration parser.
                          If supplied controller name assignments are read 
                          from configuration file section [MIDI-CONTROLLERS].
        """
        self._names = None
        self.reset()
        if config_parser:
            for cc in range(128):
                try:
                    key = "CTRL%03d" % cc
                    name = config_parser.get("MIDI-CONTROLLERS", key)
                    if name:
                        self[cc] = name
                except (NoOptionError, NoSectionError):
                    pass

    def __len__(self):
        return 128
    
    def reset(self):
        """Restore default assignments"""
        self._names = []
        for ctrl in range(len(self)):
            name = "%s" % ctrl
            self._names.append(name)

    def __setitem__(self, ctrl, name):
        """
        Assign name to MIDI controller.
        ARGS:
          ctrl - int, MIDI controller number
          name - String, the assigned name.  The name length is truncated 
                 to 12 characters.
        """
        self._names[ctrl] = str(name)[:CCAssignments.MAX_NAME_LENGTH]

    def __getitem__(self, ctrl):
        """
        Returns assigned name.
        ARGS:
          ctrl - int MIDI controller number
        RETURNS:
          String, if no name has been assigned to ctrl the result is the
          string version of ctrl.
        """
        return self._names[ctrl]

    def formatted_list(self):
        """
        RETURNS:
          A formated list of assignments.  Each element of the list is a 
          String with the controller number and the assigned name.
        """
        acc = []
        frmt = "[%03d] %s"
        for ctrl in range(len(self)):
            name = self[ctrl][:12]
            if name == str(ctrl): name = ""
            s = frmt % (ctrl, name)
            acc.append(s)
        return acc

    def serialize(self):
        acc = ["llia.CCAssignments"]+self._names
        return acc

    @staticmethod
    def deserialize(obj):
        id = obj[0]
        if id == "llia.CCAssignments":
            cca = CCAssignments()
            for i in range(len(cca)):
                cca[i] = obj[i+1]
            return cca
        else:
            msg = "Can not convert %s to CCAssignments" % obj
            raise TyoeError(msg)
    
    def __str__(self):
        acc = ""
        frmt = "[%03d] %s\n"
        for ctrl in range(len(self)):
            name = self[ctrl][:12]
            if name == str(ctrl): name = ""
            s = frmt % (ctrl, name)
            acc = acc + s
        return acc
    
    def dump(self, tab=0):
        pad = ' '*4*tab
        pad2 = pad+' '*4
        rows, columns = 32, 4
        acc = "%sCCNameMap:\n" % pad
        for r in range(rows):
            row = "%s" % pad2
            for c in range(columns):
                ctrl = r + c*rows
                name = self._names[ctrl]
                if name == str(ctrl):
                    name = ""
                row += "[%3d] %-12s " % (ctrl, name)
            acc += row + "\n"
        return acc
            


class ChannelAssignments(object):

    """ChannelAssignments associates names with MIDI channels."""
    
    def __init__(self, config_parser=None):
        """
        Construct new ChannelAssignments object

        ARGS:
          config_parser - optional configuration parser.
                          If supplied channel name assignments are read
                          form configuratio file section [MIDI-CHANNELS].

        """
        self._channel_names = None
        self._rvs_map = None
        self.reset()
        if config_parser:
            for chan in range(1, 17):
                try:
                    key = "C%02d" % chan
                    name = config_parser.get("MIDI-CHANNELS", key)
                    if name:
                        self[chan] = name
                except (NoOptionError, NoSectionError):
                    pass
                
    def __len__(self):
        return 16

    def reset(self):
        """
        Restore default assignments.
        The default names are the string version of the channel 
        number.
        """
        self._channel_names = map(str, range(1, 17))
        self._rvs_map = {}
        for i in range(1, 17):
            self._rvs_map[str(i)] = i
        

    def __setitem__(self, channel, name):
        """
        Assign name to MIDI channel.
        ARGS:
          channel - int MIDI channel 1 through 16.
          name    - String.
        RETURNS: 
           int MIDI channel 
        """
        try:
            chan0 = channel-1
            self._channel_names[chan0] = str(name)
            self._rvs_map[name] = channel
        except (TypeError, IndexError):
            msg = "Invalid MIDI channel number, expected int [1..16] "
            msg += "encountered %s" % channel
            raise IndexError(msg)

    def channel_defined(self, name):
        return self._rvs_map.has_key(name)
        
    def get_channel(self, channel_name, default=1):
        """
        Returns channel associated with name.
        ARGS:
          channel_name - String 
          default      - optional default channel if name not defined.
                         defaults to 1.
        RETURNS:
          int MIDI channel 1 through 16.
        """
        if type(channel_name) == type(0) and 1 <= channel_name <= 16:
            return channel_name
        else:
            return self._rvs_map.get(channel_name, default)
            
    def __getitem__(self, channel):
        """
        Returns name associated with MIDI channel.
        ARGS:
          channel - int channel number 1 through 16
        RETURNS:
          int MIDI channel
        RAISES
          IndexError if channel < 0 or channel > 16.
        """
        try:
            chan0 = int(channel)-1
            if chan0 < 0:
                raise IndexError()
            return self._channel_names[chan0]
        except (TypeError, IndexError):
            msg = "Invalid MIDI channel number, expected int [1..16] "
            msg += "encountered %s %s" % (type(channel), channel)
            raise IndexError(msg)

    def formatted_list(self):
        acc = []
        frmt = "[%02d] %s"
        for i in range(len(self)):
            chan = i+1
            name = self[chan]
            if name == str(chan):
                name = " "
            txt = frmt % (chan, name)
            txt = "%-24s" % txt
            acc.append(txt)
        return acc

    def serialize(self):
        acc = ["llia.ChannelAssignments"] + self._channel_names
        return acc

    @staticmethod
    def deserialize(obj):
        id = obj[0]
        if id == "llia.ChannelAssignments":
            cca = ChannelAssignments()
            for i in range(len(cca)):
                chan = i+1
                cca[chan] = obj[chan]
            return cca
        else:
            msg = "Can not convert %s to ChannelAssignments" % obj
            raise TypeError(msg)
    
    def __str__(self):
        acc = ""
        for i in range(len(self)):
            chan = i+1
            name = self[chan]
            if name == str(chan):
                name = " "
            acc += "[%02d] %-20s\n" % (chan, name)
        return acc

    def dump(self, tab=0):
        pad = ' '*4*tab
        pad2 = pad+' '*4
        acc = "%sChannelAssignments:\n" % pad
        for c in self.formatted_list():
            acc += "%s%s\n" % (pad2, c)
        return acc
    

# GLOBAL_MIDI_CC_ASSIGNMENTS = CCAssignments()
# GLOBAL_MIDI_CHANNEL_ASSIGNMENTS = ChannelAssignments()


@dump.when_type(CCAssignments)
def _dump_cc(obj):
    print(obj.dump())
            
@dump.when_type(ChannelAssignments)
def _dump_chan(obj):
    print(obj.dump())



def test():    
    cca = CCAssignments()
    cca[16] = "Joystick x"
    cca[17] = "Joystick y"
    s1 = cca.serialize()
    ccb = CCAssignments.deserialize(s1)
    dump(cca)
    dump(ccb)
    
    cha = ChannelAssignments()
    cha[1] = "TX1"
    cha[2] = "TX2"
    s2 = cha.serialize()
    chb = ChannelAssignments.deserialize(s2)
    dump(cha)
    dump(chb)
