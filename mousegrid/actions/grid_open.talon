tag: user.grid
-
<number>:
    user.grid_narrow(number)

grid off:
    user.grid_close()

grid:
    user.grid_reset()

back:
    user.grid_go_back()
    
click:
    mouse_click(0)
    user.grid_close()
