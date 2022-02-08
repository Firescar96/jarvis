import asyncio
import json
import aiohttp
from colormath.color_objects import AdobeRGBColor, xyYColor
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

async def output_lights(color):
    # color may be in two different formats, FFF and FFFFFF
    char_per_color = len(color)/3
    max_color = ((16**char_per_color)-1)
    red = int(color[0:int(char_per_color)], 16) / max_color
    green = int(color[int(char_per_color):int(2*char_per_color)], 16) / max_color
    blue = int(color[int(2*char_per_color):], 16) / max_color

    xyY = convert_color(AdobeRGBColor(red, green, blue), xyYColor)
    # taking the max is more what I want, although xyY.xyy_Y is supposed to be brightness
    brightness = max(red, green, blue) * 100
    
    async with aiohttp.ClientSession() as session:
        lights = []
        for room in hue_rooms:
            url = f"https://{hue_host}/clip/v2/resource/room/{room}"
            response = await session.get(url, headers={'hue-application-key': hue_username}, ssl=False)
            services = (await response.json())['data'][0]['services']
            lights.extend([x for x in services if x['rtype'] == 'light'])

        tasks = []
        for light in lights:
            url = f"https://{hue_host}/clip/v2/resource/light/{light['rid']}"
            tasks.append(session.put(url, data=json.dumps({
                "dimming":{"brightness":brightness},
                "color":{"xy":{"x":xyY.xyy_x,"y":xyY.xyy_y}},
                "on": {"on": brightness != 0}
            }), headers={'hue-application-key': hue_username}, ssl=False))
        
        #hue bridge can only handle so many requests at once, empirically 3 works and is better than 1, but 15 is too many
        await gather_with_concurrency(3, *tasks)












# This works, but I have no use for the entertainment api right now

# from contextlib import suppress
# from mbedtls import tls
    # num_lights = {
    #     'e2f27d28-5f55-471d-b9c9-0b7270d6f4f4': 6,
    #     'bc41b027-5fc7-4be1-9a0a-52246090323f': 10,
    # }
    # for entertainment_id in num_lights:
    #     url = f"https://{host}/clip/v2/resource/entertainment_configuration/{entertainment_id}"

    #     response = requests.put(url, data=json.dumps({'action': 'start'}), headers={'hue-application-key': username}, verify=False)

    #     print('entertainment_id', entertainment_id)
    #     dtls_cli_ctx = tls.ClientContext(tls.DTLSConfiguration(
    #         pre_shared_key=(username, client_key),
    #         validate_certificates=False,
    #     ))
    #     dtls_cli = dtls_cli_ctx.wrap_socket(
    #         socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
    #         server_hostname=None,
    #     )
    #     dtls_cli.connect((host, 2100))
    #     def block(callback, *args, **kwargs):
    #         while True:
    #             with suppress(tls.WantReadError, tls.WantWriteError):
    #                 return callback(*args, **kwargs)


    #     block(dtls_cli.do_handshake)


    #     header = [
    #         b'HueStream', #protocol
    #         b'\x02', b'\x00', #version 2.0
    #         b'\x01', #sequence number 1
    #         b'\x00', b'\x00', #reserved
    #         b'\x00', #color mode RGB
    #         b'\x00', #reserved
    #         entertainment_id.encode() #entertainment configuration
    #     ]
    #     header = b''.join(header)

    #     data = header
    #     red = int(color[0:2], 16)<<8
    #     green = int(color[2:4], 16)<<8
    #     blue = int(color[4:6], 16)<<8
    #     for i in range(num_lights[entertainment_id]):
    #         data += i.to_bytes(1, 'big')
    #         data += red.to_bytes(2, 'big')
    #         data += green.to_bytes(2, 'big')
    #         data += blue.to_bytes(2, 'big')

    #     dtls_cli.send(data)

        # requests.put(url, data=json.dumps({'action': 'stop'}), headers={'hue-application-key': username}, verify=False)
