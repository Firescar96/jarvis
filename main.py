import time
import asyncio
import multiprocessing
import traceback
import hue_interface
import voice_interface
import chatgpt_interface
#### inputs


### outputs

def output_console(input_signal:str):
  print('log:', input_signal)



### main process
main_event_queue = multiprocessing.Queue()

event_listeners = {
  'hue_interface.output_lights': hue_interface.output_lights,
  'chatgpt_interface.default': chatgpt_interface.default  
}

exit_handlers = []
async def main():
  await hue_interface.setup()
  voice_interface.input_voice(main_event_queue, exit_handlers)

  jarvis_active = True
  while jarvis_active:
    time.sleep(.5)

    next_event = main_event_queue.get(block=True)
    # catch and skip cases when processing failed and this is an empty dict
    if not next_event:
      continue

    try:
      await event_listeners[next_event['name']](*next_event['args'])
    except Exception as e:
      print(e)
      traceback.print_exc()
      continue


try:
    asyncio.run(main()) 
except (KeyboardInterrupt, SystemExit):
    for handler in exit_handlers:
      handler()