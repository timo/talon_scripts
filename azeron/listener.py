import subprocess
import threading
from glob import glob
from talon import actions, ctrl

from talon.scripting.talon_script import TalonScriptError

filename = glob("/dev/input/by-id/usb*Azeron*event-joystick")[0]

code_action_map = {
    709: "az_thumb",
    291: "az_index_pull",
    296: "az_index_push",
    300: "az_index_low_flick",
    704: "az_index_middle_flick",
    706: "az_index_high_flick",
    292: "az_index_side",
    290: "az_middle_pull",
    295: "az_middle_push",
    299: "az_middle_low_flick",
    303: "az_middle_middle_flick",
    705: "az_middle_high_flick",
    289: "az_ring_pull",
    294: "az_ring_push",
    298: "az_ring_low_flick",
    302: "az_ring_middle_flick",
    288: "az_pinkie_pull",
    293: "az_pinkie_push",
    297: "az_pinkie_low_flick",
    301: "az_pinkie_pinkie_flick",
}

def runner():
    print("opening azeron file: " + filename)
    process = subprocess.Popen(["evtest", "--grab", filename], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, encoding="latin1")
    
    axis_val_x = 0
    axis_val_y = 0
    
    stick_val_x = 512
    stick_val_y = 512
    
    stick_changed = False
    stick_live_state = False

    for l in process.stdout:
        if l.startswith("Event"):
            lp = l.split(", ")
            if lp[1] == "type 1 (EV_KEY)":
                is_press = lp[-1] == "value 1\n"
                keycode = int(lp[2].split(" ")[1])
                if is_press:
                    suf = ""
                else:
                    suf = "_release"
                if keycode in code_action_map:
                    print("will act " + code_action_map[keycode] + suf)
                    try:
                        getattr(actions.user, code_action_map[keycode] + suf)()
                    except NotImplementedError:
                        print("no action implementation i guess")
                    except KeyError:
                        print("couldn't get the azeron key action")
                    except TalonScriptError as e:
                        print("error in talonscript execution :(")
                        print(e)
                else:
                    print("key ev: code %d, press %s action %s" % (keycode, is_press, code_action_map.get(keycode, "-")))
            elif lp[1] == "type 3 (EV_ABS)":
                axiscode = int(lp[2].split(" ")[1])
                if axiscode != 16 and axiscode != 17 and axiscode != 0 and axiscode != 1:
                    continue

                if axiscode == 16 or axiscode == 17:
                    last   = [axis_val_x, axis_val_y][axiscode == 17]
                    newval = int(lp[-1].split(" ")[1])

                    name = ""

                    if axiscode == 16:
                        if (last or newval) == -1:
                            name = "left"
                        elif (last or newval) == 1:
                            name = "right"
                    elif axiscode == 17:
                        if (last or newval) == -1:
                            name = "up"
                        elif (last or newval) == 1:
                            name = "down"

                    if axiscode == 17:
                        axis_val_y = newval
                    else:
                        axis_val_x = newval

                    evname = "az_hat_" + name + "_" + (newval == 0 and "release" or "press")
                    print("hat will act: " + evname)
                    try:
                        getattr(actions.user, evname)()
                    except NotImplementedError:
                        print("no action implementation i guess")
                    except KeyError:
                        print("couldn't get the azeron key action")

                elif axiscode == 0 or axiscode == 1:
                    newval = int(lp[-1].split(" ")[1])
                    if axiscode == 0:
                        stick_val_x = newval
                    elif axiscode == 1:
                        stick_val_y = newval
                    stick_changed = True

            elif lp[1].startswith("----------"): # SYN_REPORT
                if not stick_changed:
                    continue

                stick_changed = False

                stick_dx = stick_val_x - 512
                stick_dy = stick_val_y - 512

                x_stick_live = abs(stick_dx) < 200
                y_stick_live = abs(stick_dy) < 200

                if stick_live_state and not x_stick_live and not y_stick_live:
                    stick_live_state = False
                    # actions.user.az_stick_returned()
                    print("stick returned to neutral")
                elif x_stick_live and not y_stick_live:
                    print("x stick is live; " + str(stick_dx) + " / " + str(stick_dy))
                    # azeron stick is sideways, so this uses y
                    ctrl.mouse_scroll(y = int(stick_dx / 100))
                    stick_live_state = True
                elif y_stick_live and not x_stick_live:
                    print("y stick is live; " + str(stick_dx) + " / " + str(stick_dy))
                    # azeron stick is sideways, so this uses x
                    ctrl.mouse_scroll(x = int(stick_dy / 100))
                    stick_live_state = True
                elif x_stick_live and y_stick_live:
                    print("too far away from x or y axis: " + str(stick_dx) + " / " + str(stick_dy))
                else:
                    print("no input? " + str(stick_dx) + " / " + str(stick_dy))

                # try:
                    # actions.user.az_stick_movement()
                # except NotImplementedError:
                    # print("no action implementation i guess")
                # except KeyError:
                    # print("couldn't get the azeron key action")
                # except TalonScriptError as e:
                    # print("error in talonscript execution :(")
                    # print(e)

threading.Thread(target=runner).start()
