## Scripts in this repository

### top level

* `pop_debug.py` - a simple script that just outputs "pop!" to the log whenever
    the pop noise is recognized.
* `eye_plugin_conf.py` - settings to make eye mouse controls a little more sensitive

### Desk Switcher

The files `code/desk.py` and `misc/deskswitch.talon` together offer switching
virtual desktops on linux using the tool `wmctrl`.

It offers a single spoken command: *switch desk <number>*, where number starts
at one.

### Window Switcher

`code/windowswitcher.py` and `misc/windowswitcher.talon` implement a window
switcher with a GUI popup.

Speaking *switch window* opens the switch GUI where open windows are grouped
by virtual desktop (requires `wmctrl`) and every window gets a letter or
combination of letters from your spelling alphabet (the script assumes
*~/.talon/user/knausj_talon/* to be a clone of the knausj85/knausj_talon git
repo so that it can get the alphabet from its *code/keys.py* file).

When the GUI is open, *switch air bat* switches to the window in question and
closes the GUI.

### Jetbrains additions

My `jetbrains.talon` file adds a mapping to the `EditorMatchBrace` action,
which jumps to whatever kind of brace corresponds to the one the cursor is on.

It also adds a command to invoke `JumpToChar` from the `jump` plugin by lae.

### Additions to *standard*

I found the words *standard in*, *standard out*, and *standard error* missing
from knausj's standard.talon, so I added them here.

### Debug helper to print window titles

Whenever something funky happens with app switching, this might be able to help
debugging (you can't switch to the repl when you need info about the "current"
window; for obvious reasons)

### Additions to Generic Editor

The file `text/generic_editor.talon` only adds one command, which is
*new line above*. It goes up one line, goes to the end of the line, and presses
enter to add a new line.
