### lliascript controller_name command

controller_name(ctrl, name=None)

Print or change MIDI controller name.

**ARGS

-    ctrl - int MIDI controller number, 0 <= ctrl <= 127.
-    name - optional String, the controller's new name.

**RETURNS

-    String, the controller's name.


Controller names may also be set by the startup configuration file.


If a GUI is enabled controller names may be set via an editor window.  The
editor consists of a large list of controller names above a text entry
widget.  The entry widget is used to alter the name of the currently
selected controller.  Pressing the Enter key while the text widget has
focus causes the selected controller name to be updated and for the
selected controller number to be incremented.  The up and down arrow keys
may be used in either the list or the text widget to increment/decrement
the selected controller.   

Any space character in a controller name is automatically replaced by an
underscore '_'.

If two or more controllers have identical names a warning message is
displayed. 