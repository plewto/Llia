### lliascript buffer command

buffer(name, frames=1024, channels=1)


Creates new buffer.

**ARGS**

-    name - String,  The buffers name.
            If a buffer with the same name already exists, do not replace
            it, instead simply  make it the 'current' buffer.
	    If some non buffer object is already named name, print warning
            message.

-    frames - Optional int, number of buffer frames.  If the buffer is to
     be used as a wave table this value must be a power of 2.

-    channels - Optional int, number of buffer channels.
