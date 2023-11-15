# vfd-night-clock

![image](https://github.com/shufps/vfd-night-projector-clock/assets/3079832/26defe71-99af-4adf-99c5-2ff88ad4d1ce)

## Description

The VFD Night Projector Clock is the first and only (at the moment and to my knowledge 😁) night projecting clock that uses a VFD display.

When receiving one of the NOS IVL2-7/5 displays, I noticed that the illuminated area could fit in about full-format (24x36mm) what was standard in analogue photography.

For this reason there are plenty of old lenses (e.g. with M42 threading) out there that almost cost nothing anymore although they have impressive technical properties like 1:2.8 with f=135.

Moreover, they have a flange focal distance of 45.46mm which allows to build a relatively compact casing.

![image](https://github.com/shufps/vfd-night-projector-clock/assets/3079832/6077442a-a951-40c0-a322-d42cf13f020e)

So here it is ... 🥳




This image shows a comparison between my old radio clock with projector and the VFD night clock projector:

![image](https://github.com/shufps/vfd-night-projector-clock/assets/3079832/448887c9-fb1b-4cfb-b31c-fcd3ef0189bd)

The brighness is perfect in the night 👌 (but ofc barely visible at day)

If everything is adjusted properly, you even can see the grid on the digits:

![image](https://github.com/shufps/vfd-night-projector-clock/assets/3079832/fac6c88d-ac99-44ef-92ff-6fea36e940d9)


## Properties

There are some methods how a VFD can be operated. After some prior experience with VFDs this is one of the easiest methods:

- isolated 24 DCDC converter for anode voltage. The V+ is connected to GND, so you have -24V on the board
- the positive gate/segment voltage is +3.3V. You easily can switch the positive gate/segment voltage with BSS84s from a STM32 with no additional parts what is the easiest solution. This gives a total gate / segment voltage of 27.3V
- AC Filament drive is done with a full-bridge made of a two channel MOSFET driver. The output is AC coupled and pulled to about -22V. Bias is adjustable (even could be used to change the brightness)

![image](https://github.com/shufps/vfd-night-projector-clock/assets/3079832/3ee4af2f-46fb-4d40-b717-108762b51c3f)



## STM32 Software

The STM32 software currently only supports a json-rpc via USB virtual COM port (CDC). Buttons are currently unused 🙈

There is python code that can 

- measure the clock accuracy
- set the time
- set the display state and auto-switch on/off

This are small examples that nicely demonstrate how to use the json-rpc.

## 3D case

![image](https://github.com/shufps/vfd-night-projector-clock/assets/3079832/7ccb60f4-8a49-468e-9ba0-ce93a029dc57)

The case was designed in a way that no supports are needed. The upper part is simply clipped on the lower part.

<!--
Ode to VFD Displays (Chatti4 2023)

Oh, relics of an era long past,<br>
Vacuum Fluorescent Displays, you hold fast.<br>
Born in Soviet realms, a technological feast,<br>
Your glasspunk aesthetics have never ceased.<br>

In your cylindrical tubes, a dance of light,<br>
A greenish-blue hue, softly bright.<br>
Your glow, a whisper from history's tide,<br>
In old devices, you reside with pride.<br>

You are the silent storytellers, bold,<br>
Of times when technology wasn't so cold.<br>
Your luminescent charm, a visual delight,<br>
In the stillness of rooms, you're the night's light.<br>

Through you, numbers and words gracefully flow,<br>
A retro display, a nostalgic glow.<br>
Your enduring spirit, a testament to time,<br>
In the world of screens, you're a verse, a rhyme.<br>

VFD, in your glass cocoon you lay,<br>
A visual symphony in green and gray.<br>
A bridge from the past, to the present you lead,<br>
A piece of history, in every glowing bead.<br>

In the march of progress, you're a quiet ode,<br>
A reminder of a less digital road.<br>
VFD displays, in you, the past does reside,<br>
A beautiful, forgotten technological stride.<br>
-->
