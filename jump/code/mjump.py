from talon import Module, ctrl, ui

mod = Module()

@mod.action_class
class jump:
    def jump_window_center():
        'jump mouse cur to middle of window'
        w = ui.active_window()
        r=w.rect
        x=r.x+(r.width//2)
        y=r.y+(r.height//2)
        ctrl.mouse_move(x,y)
