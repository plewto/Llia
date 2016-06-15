(
s = Server.local.boot;
)

(
a.free;
a = LliaHandler.new();
~buffers = a.buffers;
// ~buffers.wave("saw");
~buffers.lliaDump;

)


q = Synth(\ORGN);
q.free;


r = Stethoscope(s);
