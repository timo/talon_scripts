action(user.az_index_push): key(shift:down)
action(user.az_index_push_release): key(shift:up)
action(user.az_index_pull): core.repeat_command(1)

action(user.az_index_high_flick): key(backspace)
action(user.az_middle_high_flick): key(delete)

action(user.az_thumb): user.delayed_speech_on()

action(user.az_thumb_release): user.delayed_speech_off()

action(user.az_pinkie_pull):
    speech.enable()
    app.notify("speech on")
action(user.az_pinkie_push):
    speech.disable()
    app.notify("speech off")


action(user.az_hat_left_press): edit.word_left()
action(user.az_hat_right_press): edit.word_right()
action(user.az_hat_up_press): edit.right()
action(user.az_hat_down_press): edit.left()

click a whole lot:
    mouse_click(0)
    sleep(100ms)
    mouse_click(0)
    sleep(100ms)
    mouse_click(0)
    sleep(100ms)
    mouse_click(0)
    sleep(100ms)
    mouse_click(0)
    sleep(100ms)
    mouse_click(0)
    sleep(100ms)
    mouse_click(0)
    sleep(100ms)
    mouse_click(0)
    sleep(100ms)
    mouse_click(0)
    sleep(100ms)
    mouse_click(0)
    sleep(100ms)
    mouse_click(0)
    sleep(100ms)
    mouse_click(0)
    sleep(100ms)

many times: core.repeat_command(100)
