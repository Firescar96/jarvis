import asyncio
import json
import aiohttp
from gpt_interface import process_color_hex
from colormath.color_objects import sRGBColor, xyYColor
from colormath.color_conversions import convert_color
import urllib3
from secrets import hue_username, hue_host, hue_rooms
urllib3.disable_warnings()


async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task
    return await asyncio.gather(*(sem_task(task) for task in tasks))

lights = []
async def setup():
    async with aiohttp.ClientSession() as session:
        device_rids = []
        for room in hue_rooms:
            url = f"https://{hue_host}/clip/v2/resource/room/{room}"
            response = await session.get(url, headers={'hue-application-key': hue_username}, ssl=False)
            children = (await response.json())['data'][0]['children']
            device_rids.extend([x['rid'] for x in children])

        for device in device_rids:
            url = f"https://{hue_host}/clip/v2/resource/device/{device}"
            response = await session.get(url, headers={'hue-application-key': hue_username}, ssl=False)
            services = (await response.json())['data'][0]['services']
            lights.extend([x for x in services if x['rtype'] == 'light'])
    

async def output_lights(color_text):
    color = process_color_hex(color_text)

    # color may be in two different formats, FFF and FFFFFF
    char_per_color = len(color)/3
    max_color = ((16**char_per_color)-1)
    red = int(color[0:int(char_per_color)], 16) / max_color
    green = int(color[int(char_per_color):int(2*char_per_color)], 16) / max_color
    blue = int(color[int(2*char_per_color):], 16) / max_color

    xyY = convert_color(sRGBColor(red, green, blue), xyYColor)
    # taking the max is more what I want, although xyY.xyy_Y is supposed to be brightness
    brightness = max(red, green, blue) * 100
    
    async with aiohttp.ClientSession() as session:

        tasks = []
        for light in lights:
            url = f"https://{hue_host}/clip/v2/resource/light/{light['rid']}"
            tasks.append(session.put(url, data=json.dumps({
                "dimming":{"brightness":brightness},
                "color":{"xy":{"x":xyY.xyy_x,"y":xyY.xyy_y}},
                "on": {"on": brightness != 0}
            }), headers={'hue-application-key': hue_username}, ssl=False))
        
        #hue bridge can only handle so many requests at once, empirically 3 works and is better than 1, but 15 is too many
        await gather_with_concurrency(1, *tasks)



async def input_lights():
    async with aiohttp.ClientSession() as session:

        tasks = []
        for light in lights:
            url = f"https://{hue_host}/clip/v2/resource/light/{light['rid']}"
            tasks.append(session.get(url, data=json.dumps({
                
            }), headers={'hue-application-key': hue_username}, ssl=False))
        
        #hue bridge can only handle so many requests at once, empirically 3 works and is better than 1, but 15 is too many
        results = await gather_with_concurrency(1, *tasks)
        results = await asyncio.gather(*[x.json() for x in results])
        light_colors = {}
        for index, res in enumerate(results):
            xyy_color = {**res['data'][0]['color']['xy'], 'brightness': res['data'][0]['dimming']['brightness']}
            rgb:sRGBColor = convert_color(xyYColor(xyy_color['x'], xyy_color['y'], xyy_color['brightness']/100), sRGBColor)
            light_data = {
                'r': rgb.clamped_rgb_r,
                'g': rgb.clamped_rgb_g,
                'b': rgb.clamped_rgb_b,
                'on': res['data'][0]['on']['on'],
                'type': 'light'
            }
            light_colors[lights[index]['rid']] = light_data
        return light_colors


# testing section
# async def main():
#     light_colors = await input_lights()
#     print(light_colors)

# if __name__ == "__main__":
#     asyncio.run(main())