from talon import Module, Context, app, canvas, ui, ctrl
from talon.skia import Shader, Color
from talon_plugins import eye_mouse, eye_zoom_mouse

import math, time

import typing

mod = Module()

ctx = Context()

class MouseSnapNine:
    def __init__(self):
        self.states = []
        # self.screen_index = 0
        self.screen = ui.screens()[0]
        self.offset_x = self.screen.x
        self.offset_y = self.screen.y
        self.width = self.screen.width
        self.height = self.screen.height
        self.states.append((self.offset_x, self.offset_y, self.width, self.height))
        self.mcanvas = canvas.Canvas.from_screen(self.screen)
        self.active = False
        self.moving = False
        self.count = 0
        self.was_eye_tracking = False

    #     tap.register(tap.MMOVE, self.on_move)
    #
    # def on_move(self, typ, e):
    #     if typ != tap.MMOVE or not self.active:
    #         return
    #     x, y = self.pos()
    #     last_pos = self.states[-1]
    #     x2, y2 = last_pos[0] + last_pos[2]//2, last_pos[1] + last_pos[3]//2
    #     # print("moved ", e, x, y)
    #     if (e.x, e.y) != (x, y) and (e.x, e.y) != (x2, y2):
    #         self.stop(None)

    def start(self, *_):
        if self.active:
            return
        # noinspection PyUnresolvedReferences
        if eye_zoom_mouse.zoom_mouse.enabled:
            return
        if eye_mouse.control_mouse.enabled:
            self.was_eye_tracking = True
            eye_mouse.control_mouse.toggle()
        if self.mcanvas is not None:
            self.mcanvas.unregister("draw", self.draw)
        self.mcanvas.register("draw", self.draw)
        self.active = True

    def stop(self, *_):
        # self.mcanvas.unregister("draw", self.draw)
        self.active = False
        if self.was_eye_tracking and not eye_mouse.control_mouse.enabled:
            eye_mouse.control_mouse.toggle()
        self.was_eye_tracking = False

    def draw(self, canvas):
        paint = canvas.paint
        def draw_grid(offset_x, offset_y, width, height):
            canvas.draw_line(
                offset_x + width // 3,
                offset_y,
                offset_x + width // 3,
                offset_y + height,
            )
            canvas.draw_line(
                offset_x + 2 * width // 3,
                offset_y,
                offset_x + 2 * width // 3,
                offset_y + height,
            )

            canvas.draw_line(
                offset_x,
                offset_y + height // 3,
                offset_x + width,
                offset_y + height // 3,
            )
            canvas.draw_line(
                offset_x,
                offset_y + 2 * height // 3,
                offset_x + width,
                offset_y + 2 * height // 3,
            )

        def draw_crosses(offset_x, offset_y, width, height):
            for row in range(0, 2):
                for col in range(0, 2):
                    cx = offset_x + width / 6 + (col + 0.5) * width / 3
                    cy = offset_y + height / 6 + (row + 0.5) * height / 3

                    canvas.draw_line(
                        cx - 10, cy,
                        cx + 10, cy
                        )
                    canvas.draw_line(
                        cx, cy - 10,
                        cx, cy + 10
                        )

        # def draw_grid(offset_x, offset_y, width, height, dxp = 0, dyp = 0):
            # dx = (dxp / 100) * width
            # dy = (dyp / 100) * height
            # canvas.draw_line(
                # offset_x + width // 3,
                # offset_y + dy,
                # offset_x + width // 3,
                # offset_y + height - dy,
            # )
            # canvas.draw_line(
                # offset_x + 2 * width // 3,
                # offset_y + dy,
                # offset_x + 2 * width // 3,
                # offset_y + height - dy,
            # )

            # canvas.draw_line(
                # offset_x + dx,
                # offset_y + height // 3,
                # offset_x + width - dx,
                # offset_y + height // 3,
            # )
            # canvas.draw_line(
                # offset_x + dx,
                # offset_y + 2 * height // 3,
                # offset_x + width - dx,
                # offset_y + 2 * height // 3,
            # )

        if not self.active:
            if time.time() % 240 < 10:
                alpha = "60"
                animpos = (time.time() % 240) / 10
                fromcnt = (animpos - 0.5) * 2
                stops = [animpos - 0.1, animpos - 0.05, animpos, animpos + 0.05, animpos + 0.1]
                stops = list(map(lambda c: min(max(c, 0), 1), stops))
                paint.shader = Shader.linear_gradient(
                        0, self.height / 9,
                        self.width, 8 * self.height / 9,
                        ["00000000", "ff0000" + alpha, "0000ff" + alpha, "00ff00" + alpha, "00000000"],
                        stops,
                        Shader.TileMode.CLAMP)
            else:
                return


        def draw_text(offset_x, offset_y, width, height):
            for row in range(3):
                for col in range(3):
                    canvas.draw_text(
                        f"{row*3+col+1}",
                        offset_x + width / 6 + col * width / 3,
                        offset_y + height / 6 + row * height / 3,
                    )

        if self.count < 2:
            paint.color = "00ff007f"
            for which in range(1, 10):
                gap = 35 - self.count * 10
                if not self.active:
                    gap = 45
                draw_crosses(*self.calc_narrow(which, self.offset_x, self.offset_y, self.width, self.height))

        if self.active:
            paint.color = "ff0000ff"
        else:
            paint.color = "000000ff"
        draw_grid(self.offset_x, self.offset_y, self.width, self.height)

        if self.active and self.count < 3:
            paint.textsize += 6 - self.count * 3
            draw_text(self.offset_x, self.offset_y, self.width, self.height)

    def calc_narrow(self, which, offset_x, offset_y, width, height):
        row = int(which - 1) // 3
        col = int(which - 1) % 3
        offset_x += int(col * width // 3) - 5
        offset_y += int(row * height // 3) - 5
        width //= 3
        height //= 3
        width += 10
        height += 10
        return [offset_x, offset_y, width, height]


    def narrow(self, which, move=True):
        if which < 1 or which > 9:
            return
        self.save_state()
        self.offset_x, self.offset_y, self.width, self.height = self.calc_narrow(which, self.offset_x, self.offset_y, self.width, self.height)
        if move:
            ctrl.mouse_move(*self.pos())
        self.count += 1
        if self.count >= 4:
            self.reset(None)

    def pos(self):
        return self.offset_x + self.width // 2, self.offset_y + self.height // 2

    def reset(self, pos=-1):
        def _reset(m):
            self.save_state()
            self.count = 0
            x, y = ctrl.mouse_pos()

            if pos >= 0:
                self.screen = ui.screens()[pos]
            else:
                self.screen = ui.screen_containing(x, y)

            # print(screens)
            # self.screen = screens[self.screen_index]
            self.offset_x = self.screen.x
            self.offset_y = self.screen.y
            self.width = self.screen.width
            self.height = self.screen.height
            if self.mcanvas is not None:
                self.mcanvas.unregister("draw", self.draw)
            self.mcanvas = canvas.Canvas.from_screen(self.screen)
            self.mcanvas.register("draw", self.draw)
            if eye_mouse.control_mouse.enabled:
                self.was_eye_tracking = True
                eye_mouse.control_mouse.toggle()
            if self.was_eye_tracking and self.screen == ui.screens()[0]:
                # if self.screen == ui.screens()[0]:
                self.narrow_to_pos(x, y)
                self.narrow_to_pos(x, y)
                # self.narrow_to_pos(x, y)
            # print(self.offset_x, self.offset_y, self.width, self.height)
            # print(*self.pos())

        return _reset

    def narrow_to_pos(self, x, y):
        col_size = int(self.width // 3)
        row_size = int(self.height // 3)
        col = math.floor((x - self.offset_x) / col_size)
        row = math.floor((y - self.offset_y) / row_size)
        # print(f"Narrow to {row} {col} {1 + col + 3 * row}")
        self.narrow(1 + col + 3 * row, move=False)

    def save_state(self):
        self.states.append((self.offset_x, self.offset_y, self.width, self.height))

    def go_back(self):
        last_state = self.states.pop()
        self.offset_x, self.offset_y, self.width, self.height = last_state
        self.count -= 1

mg = MouseSnapNine()

@mod.action_class
class GridActions:
    def grid_activate():
        """Brings up a/the grid (mouse grid or otherwise)"""
        ctx.tags = ["user.grid"]
        mg.start()

    def grid_reset():
        """Resets the grid to fill the whole screen again"""
        mg.reset()(None)

    def grid_select_screen(screen: int):
        """Brings up a/the grid (mouse grid or otherwise)"""
        mg.reset(screen)(None)
        mg.start()

    def grid_narrow_list(digit: typing.List[int]):
        """Choose fields multiple times in a row"""
        print("narrow many", repr(digit))
        for d in digit:
            GridActions.grid_narrow(d)

    def grid_narrow(digit: int):
        """Choose a field of the grid and narrow the selection down"""
        print("narrow one", repr(digit))
        mg.narrow(digit)

    def grid_go_back():
        """Sets the grid state back to what it was before the last command"""
        mg.go_back()

    def grid_close():
        """Close the active grid"""
        ctx.tags = []
        mg.reset()(None)
        mg.stop()


mg.start()
mg.stop()
