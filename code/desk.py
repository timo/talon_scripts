from talon import ctrl, Module, Context
import os

ctx = Context()
mod = Module()

@mod.action_class
class Actions:
    def switch_desk(index: str):
        """Switch to a virtual desktop by index (starting at 1)"""
        os.system("wmctrl -s " + str(int(index) - 1))
