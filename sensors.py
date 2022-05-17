import time
import hue_interface
import asyncio
import json
from deepdiff import DeepDiff

async def main():
  sensor_history = []

  sensor_history.append({'c79ed689-ea87-42d2-ba86-19c12f7cd064': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': True, 'type': 'light'}, 'c81a46c6-e441-4d47-aa60-ac43ce22332e': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': True, 'type': 'light'}, 'd337481a-91ac-4c6d-967e-944d1e754d6a': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': True, 'type': 'light'}, 'f4193a7f-0a36-4286-b75a-b7ebcd2a6e22': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': True, 'type': 'light'}, 'e63a7c2c-225b-451e-99ba-cec0ddb4eaae': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': True, 'type': 'light'}, '500e0161-767b-430b-aceb-019b6aab840b': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': True, 'type': 'light'}, '0027e6b2-7acb-4984-a7a8-dc4e39dc48a5': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, '64a5b577-35c6-4c74-8633-8d48f6e222ef': {'r': 1.0, 'g': 0.38843762758036693, 'b': 0.5510747457133525, 'on': True, 'type': 'light'}, '9529043b-f152-47a2-bd39-eb049b1c1ead': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, '2f11655a-4305-4f5c-bb24-1e8db1bfe54e': {'r': 1.0, 'g': 0.7124766801931415, 'b': 0.0, 'on': True, 'type': 'light'}, '82530f59-8b1a-4211-863f-01dd1071b03d': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, '9e51f5de-79ea-42ab-bdb4-2ee734dd849c': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, '1515a193-631a-401a-892a-1593d215fe37': {'r': 1.0, 'g': 0.7124766801931415, 'b': 0.0, 'on': True, 'type': 'light'}, '382edc89-4120-47bf-a14b-f667fc49c9c7': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, 'cd8d688d-a4eb-4349-8cb6-e1f8a21a442e': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, '3afe8ac8-6d0a-4f2e-afb6-154248cce023': {'r': 1.0, 'g': 0.38843762758036693, 'b': 0.5510747457133525, 'on': True, 'type': 'light'}})
  sensor_history.append({'c79ed689-ea87-42d2-ba86-19c12f7cd064': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': True, 'type': 'light'}, 'c81a46c6-e441-4d47-aa60-ac43ce22332e': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': True, 'type': 'light'}, 'd337481a-91ac-4c6d-967e-944d1e754d6a': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': True, 'type': 'light'}, 'f4193a7f-0a36-4286-b75a-b7ebcd2a6e22': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': False, 'type': 'light'}, 'e63a7c2c-225b-451e-99ba-cec0ddb4eaae': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': True, 'type': 'light'}, '500e0161-767b-430b-aceb-019b6aab840b': {'r': 1.0, 'g': 0.9216161695618857, 'b': 0.5811534559285528, 'on': True, 'type': 'light'}, '0027e6b2-7acb-4984-a7a8-dc4e39dc48a5': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, '64a5b577-35c6-4c74-8633-8d48f6e222ef': {'r': 1.0, 'g': 0.38843762758036693, 'b': 0.5510747457133525, 'on': True, 'type': 'light'}, '9529043b-f152-47a2-bd39-eb049b1c1ead': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, '2f11655a-4305-4f5c-bb24-1e8db1bfe54e': {'r': 1.0, 'g': 0.7124766801931415, 'b': 0.0, 'on': True, 'type': 'light'}, '82530f59-8b1a-4211-863f-01dd1071b03d': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, '9e51f5de-79ea-42ab-bdb4-2ee734dd849c': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, '1515a193-631a-401a-892a-1593d215fe37': {'r': 1.0, 'g': 0.7124766801931415, 'b': 0.0, 'on': True, 'type': 'light'}, '382edc89-4120-47bf-a14b-f667fc49c9c7': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, 'cd8d688d-a4eb-4349-8cb6-e1f8a21a442e': {'r': 1.0, 'g': 0.0, 'b': 0.0, 'on': True, 'type': 'light'}, '3afe8ac8-6d0a-4f2e-afb6-154248cce023': {'r': 1.0, 'g': 0.38843762758036693, 'b': 0.5510747457133525, 'on': True, 'type': 'light'}})

  await hue_interface.setup()

  while True:
    sensor_history.append(await hue_interface.input_lights())
    # print('sensors', sensors)
    sensor_diff = DeepDiff(sensor_history[-2], sensor_history[-1], view='tree')
    if not sensor_diff:
      continue
    
    minimized_dict = {}
    agenda = [(minimized_dict, x.all_up) for x in sensor_diff['values_changed']]
    while agenda:
      current_dict, current_diff = agenda.pop()
      field_param = current_diff.t2_child_rel.param
      current_dict[field_param] = {}
      if current_diff.down.t2_child_rel:
        agenda.append((current_dict[field_param], current_diff.down))
      else:
        current_dict[field_param] = current_diff.t2[field_param]
    print('minimized_dict', minimized_dict)

    sensor_history = sensor_history[-100:]
    time.sleep(2)


asyncio.get_event_loop().run_until_complete(main())


'''
try to do an exact match on state, and fallback to a gpt processor
'''