from pynput.keyboard import Key, Listener

key_pressed = False


def on_press(key):
    global key_pressed
    # print("key pressed: {}".format(key_pressed))
    if not key_pressed:
        key_pressed = True
        print('{0} pressed'.format(key))
        if hasattr(key, 'char'):
            if 'w' == key.char:
                print("w - forward")
            if 'a' == key.char:
                print("a - left")
            if 'd' == key.char:
                print("d - right")
            if 's' == key.char:
                print("s - backward")


def on_release(key):
    global key_pressed
    key_pressed = False
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False


# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
