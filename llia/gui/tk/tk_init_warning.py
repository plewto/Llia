# llia.gui.tk.tk_init_warning
# 2016.06.18

import tkMessageBox

# Ask for user consent before initializing an object.
# Returns True if use gives consent, False otherwise.
#
# If config.warn_on_initialize() returns True,
#    a confirmation dialog is presented for user's 
#    explicit consent.
#
# If config.warn_on_initialize() returns False,
#    Act as if user has given consent by returning True
#    without asking. 

def init_warning(msg, app):
    if app.config().warn_on_initialize():
        user = tkMessageBox.askokcancel("Initialize Warning", msg)
        return user
    else:
        return True
