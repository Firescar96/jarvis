import time
import asyncio
from pynput import keyboard
import traceback
import voice_interface
import chatgpt_interface

exit_handlers = []

key_released = None
def on_release(key):
    global key_released
    key_released = key

# Set up a listener for keyboard events
key_listener = keyboard.Listener(on_release=on_release)
key_listener.start()

async def main():
    jarvis_active = True
    global key_pressed
    global key_released

    print('Press F and wait for the terminal output to stop then start speaking')
    while jarvis_active:
        time.sleep(0.1)

        if not key_released or not hasattr(key_released, 'char') or key_released.char != 'f':
            continue

        try:
            voice_text = voice_interface.read_voice()
        except Exception as e:
            print('voice_interface.read_voice() failed')
            traceback.print_exc()
            continue
        print('This is what I heard:', voice_text)
        print('Press any key to submit or press F to record again')
        key_released = None
        while key_released is None:
            await asyncio.sleep(0.1)

        if key_released and hasattr(key_released, 'char') and key_released.char == 'f':
            key_released = None
            continue
        key_released = None
        await chatgpt_interface.default(voice_text)

asyncio.run(main())
