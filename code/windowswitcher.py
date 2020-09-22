from talon import Context, Module, app, clip, cron, imgui, canvas, actions, ui
from talon.skia import Rect
from ...knausj_talon.code.keys import default_alphabet, letters_string

from subprocess import run
from math import log, ceil

ctx = Context()

mod = Module()
mod.list('window_selection_words', desc='list of words ')
mod.list('homophones_selections', desc='list of valid selection indexes')

@mod.capture
def window_selection_words(m) -> int:
    "Returns the index of the aplication selected via letter words"

shown_windows = []
# window_codes = []
window_spelling = []

window_to_words = {}

@imgui.open(y=0,software=True)
def gui(gui: imgui.GUI):
    global shown_windows
    global window_spelling
    global groups
    gui.text("Select a window")
    index = 0
    for g in groups:
        gui.line()
        gui.text("desktop {}".format(g))
        for win in groups[g]:
            if gui.button("switch {}: {} ({})".format(window_spelling[index],win.title, win.app.name)):
                win.focus()
                close_gui_and_drawing()
            index = index + 1

    gui.line()
    if gui.button("close"):
        close_gui_and_drawing()


def make_combinations(amount):
    base_pieces = len(default_alphabet)
    base_num = ceil(log(amount, base_pieces))

    pieces = [0] * base_num
    results = []
    while len(results) < amount:
        for pos in range(base_num - 1, -1, -1):
            pieces[pos] += 1
            if pieces[pos] == base_pieces:
                pieces[pos] = 0
            else:
                break
        want_skip = False
        for i in range(0, len(pieces) - 1):
            if pieces[i] == pieces[i + 1]:
                want_skip = True
        if not want_skip:
            results.append(list(pieces))

    return results

@mod.action_class
class Actions:
    def show_window_switcher():
        """Display a window switcher"""
        global shown_windows
        global window_spelling
        global groups
        global this_desktop_windows
        global window_to_words

        shown_windows = ui.windows()

        print("current desk is...")
        current_desk = list(filter(lambda l: l.split("  ")[1][0] == "*", run(["wmctrl", "-d"], capture_output=True, encoding="utf8").stdout.splitlines()))[0].split("  ")
        print("   ", current_desk)

        # wmctrl -l gives us window IDs (in hex) and desktop numbers (-1 is pinned)
        desk_map = run(["wmctrl", "-l"], capture_output=True, encoding="utf8").stdout.splitlines()
        # for every window, store its ID : its desk
        desk_map = { int(a[0][2:], 16): int(a[1]) for a in map(lambda l: l.split()[0:2], desk_map) }

        # build letter combos
        combs = make_combinations(len(shown_windows))

        # grab the desktops that have windows
        groups = sorted(set(desk_map.values()))

        print("desk map:")
        print("    ", desk_map)

        # put a list of all window objects that are on one desktop for each desk
        groups = { k: list(filter(lambda e: desk_map.get(e.id, None) == k, shown_windows)) for k in groups }

        shown_windows = []
        this_desktop_windows = []
        window_to_words = {}

        # make a flat list
        for k in groups:
            shown_windows.extend(groups[k])
            if k == -1 or k == int(current_desk[0]):
                this_desktop_windows.extend(groups[k])

        # turn letter combos into word combos (ab -> air bat)
        window_spelling = list(map(lambda entry: " ".join(map(lambda digit: default_alphabet[digit], entry)), combs))
        ctx.lists['self.window_selection_words'] = window_spelling

        i = 0
        for k in groups:
            print(repr(k), " ", repr(int(current_desk[0])))
            if k == -1 or k == int(current_desk[0]):
                print("  this is the one!")
                for w in groups[k]:
                    print("    saving spelling for ", w.id, " as ", window_spelling[i], " which is ", i)
                    window_to_words[w.id] = window_spelling[i]
                    i += 1
            else:
                i += len(groups[k])

        gui.show()

    def switch_to_window(window: ui.Window):
        """Switch to the window at the given index"""
        window.focus()
        close_gui_and_drawing()

@ctx.capture(rule='{self.window_selection_words}')
def window_selection_words(m):
    taken = window_spelling.index(m.window_selection_words)
    return shown_windows[taken]

ctx.lists['self.window_selection_words'] = []
