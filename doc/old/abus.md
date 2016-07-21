### lliascript abus command

abus(name, channels=1)

Creates an audio bus on the server.  


**ARGS

-    name - String, the audio bus name.  If an audio bus with the same name
     already exist abus does nothing.  All buses, buffers and synths must
     have unique names and an attempt to create an audio bus with a name
     used for some other non audio bus object will provoke a warning.

     Llia automatically creates names for the first several "public" audio
     buses.  The exact number of automatic buses is determined by how
     SuperCollider is configured.  The output buses have enumerated names
     of the form "out_0", "out_1", ..., "out_n".   These correspond to the
     first n sound card outputs.  A typical value for n is 8.  Like wise
     the  first n input buses have names "in_0", "in_1", ..., "in_n".

-    channels - int, number of bus channel, default 1.
