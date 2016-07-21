### lliascript history command

history()

Display the lliascript history.

As lliascript commands are executed they are appended to the end of the
history log.  lliascript may also add remarks to the history, particularly
in the case of an error.


The history log is executable Python and may be saved and reloaded to
recreate a Llia state.


If A GUI is enabled a basic text editor is available under the
File/lliascript menu.


The editor tools include:

-   Open - Read a python file into the editor
-   Save - Save the current editor contents to a file
-   Exec - Execute the current editor contents as a lliascript batch file.
-   Compose - Creates a python script which may be used to recreate the
              current state of Llia.  