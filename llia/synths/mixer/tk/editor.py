# llia.synths.mixer.tk.editor


from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

def create_editor(parent):
    TkMixerPanel(parent)


class TkMixerPanel(TkSubEditor):

    NAME = "Mixer"
    IMAGE_FILE = "resources/Mixer/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)

        y0 = 60
        ypan = y0 + 260
        yrev = ypan + 120
        x0 = 120

        def fader(chan, x):
            param = "gain%s" % chan
            s = cf.volume_slider(frame, param, editor)
            self.add_control(param,s)
            s.widget().place(x=x, y=y0, height=200)

        def panner(chan, x):
            param = "pan%s" % chan
            s = cf.bipolar_slider(frame,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x, y=ypan, height=75)

        def reverb_send(chan, x):
            param = "reverb%s" % chan
            s = cf.normalized_slider(frame, param, editor)
            self.add_control(param, s)
            s.widget().place(x=x, y=yrev-19, height=75)

        for i in range(4):
            chan = "%s" % (i+1,)
            x = x0 + i * 60
            fader(chan, x)
            panner(chan, x)
            reverb_send(chan, x)

        x_reverb = x0 + 300

        s_reverb_size = cf.normalized_slider(frame, "reverbRoomSize", editor)
        s_reverb_damp = cf.normalized_slider(frame, "reverbDamp", editor)
        s_reverb_lowpass = cf.third_octave_slider(frame, "reverbLowpass", editor)
        s_reverb_highpass = cf.third_octave_slider(frame, "reverbHighpass", editor)
        s_reverb_balance = cf.bipolar_slider(frame, "reverbBalance", editor)
        s_reverb_return = cf.volume_slider(frame, "reverbReturn", editor)

        self.add_control("reverbRoomSize", s_reverb_size)
        self.add_control("reverbDamp", s_reverb_damp)
        self.add_control("reverbLowpass", s_reverb_lowpass)
        self.add_control("reverbHighpass", s_reverb_highpass)
        self.add_control("reverbReturn", s_reverb_return)
        self.add_control("reverbBalance", s_reverb_balance)

        s_reverb_size.widget().place(x=x_reverb, y=ypan, height=175)
        s_reverb_damp.widget().place(x=x_reverb+60, y=ypan, height=175)
        s_reverb_lowpass.widget().place(x=x_reverb+120, y=ypan, height=175)
        s_reverb_highpass.widget().place(x=x_reverb+180, y=ypan, height=175)
        s_reverb_balance.widget().place(x=x_reverb+240, y=ypan, height=175)
        s_reverb_return.widget().place(x=x_reverb+300, y=ypan, height=175)

        x_main = x_reverb
        s_main1 = cf.volume_slider(frame,"mainAmpA", editor)
        s_main2 = cf.volume_slider(frame,"mainAmpB", editor)
        self.add_control("mainAmpA", s_main1)
        self.add_control("mainAmpB", s_main2)
        s_main1.widget().place(x=x_main, y=y0, height=200)
        s_main2.widget().place(x=x_main+60, y=y0, height=200)
