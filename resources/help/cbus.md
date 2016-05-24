### lliascript cbus command

cbus(name, channel=1)

Create server side control bus.

**ARGS

-    name - String, the control bus name.  If a control bus with the same
     name already exists cbus does nothing.  All buses, buffers and synths
     must have unique names and an attempt to create a control bus with a
     name in use for an existing non-control bus object results in a
     reprimand.

-    channels - int, number of bus channels, default 1.