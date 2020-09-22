M grid:
    user.grid_activate()

grid win:
    user.grid_place_window()
    user.grid_activate()

grid <number>+ click:
    user.grid_activate()
    user.grid_narrow_list(number_list)
    mouse_click(0)
    user.grid_close()

grid <number>+:
    user.grid_activate()
    user.grid_narrow_list(number_list)

grid screen <number>:
    user.grid_select_screen(number)
    user.grid_activate()
