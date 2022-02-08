# jarvis

# Status
This project is pretty early. For something a little further along I would have a task list like [Cenza's Kanban](https://www.notion.so/e86d7ef66aaf4a3eb8e86f0952e6534e?v=b95e04d101f64770863f77232765fe05) but right now it's too experimental. I just have my [notes in Notion](https://www.notion.so/Jarvis-49354603b625456ca3342a32487a5a2c).



# Overview
This project is an exploration into making neural nets with very 'clean signals'. Clean meaning not noisy and 100% accurate. For example, the apis for smart home lights, locks, and temperature sensors have highly accurate outputs (e.g. the lights never report they are a different color than they are) and accurate inputs (e.g. setting the lights to red will never make them turn blue).

Theoretically the bot should be able to train itself with one iteration, compared to the millions of iterations it takes for a bot to play Go or Starcraft. Adding a new light should be as easy as plugging it in and asking the bot to recognize a new device. That part is key, It should be able to play with the device and figure out what it can do similar to a human would with a prosthetic limb.

Future work also includes incorporating [Nubia](https://github.com/wl-research/nubia) to determine logical sentence aggrement. This will be useful to do something Google Assistant can't and parse all of 'turn on the lights', 'lights please', 'can i get some light in here', and potentially 'i need light' all as commands to turn on the lights, without having to explicitly code all of those cases.

# Development

Barrier to entry to running this is pretty high, you need at least one [Phillips Hue](https://www.philips-hue.com/en-us) light and access to [OpenAI's GPT3](https://www.theguardian.com/commentisfree/2020/sep/08/robot-wrote-this-article-gpt-3). I personally don't possess beta access to GPT3, I've been sharing a friend's account for months.

Also I put all my secrets in one file and you can't have it.

# Demo
[![Jarvis Demo](http://img.youtube.com/vi/i4Jjgc48KeY/0.jpg)](http://www.youtube.com/watch?v=i4Jjgc48KeY "Jarvis 2022-01-31")