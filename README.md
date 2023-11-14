# vfd-night-clock

![image](https://github.com/shufps/vfd-night-projector-clock/assets/3079832/26defe71-99af-4adf-99c5-2ff88ad4d1ce)

## Description

The VFD Night Projector Clock is the first and only (at the moment and to my knowledge 😁) night projecting clock that uses a VFD display.

When receiving one of the NOS IVL2-7/5 displays, I noticed that it could have about full-format (24x36mm) what was standard in analogue photography.

For this reason there are plenty of old lenses (e.g. with M42 threading) out there that almost cost nothing anymore although they have impressive technical properties like 1:2.8 with f=135.

Moreover, they have a flange focal distance of 45.46mm which allows to build a relatively compact casing.

![image](https://github.com/shufps/vfd-night-projector-clock/assets/3079832/57ff3927-153c-475b-b000-4556b7a6dd36)

So here it is ... 🥳

This image shows a comparison between my old radio clock with projecting clock and the VFD projector:

![image](https://github.com/shufps/vfd-night-projector-clock/assets/3079832/d19576c7-4cfa-4a5a-8980-7dacecd6e32d)

The brighness is perfect in the night 👌

## Properties

There are some methods how a VFD can be operated. After some prior experience with VFDs this is one of the easiest method:

- isolated 24 DCDC converter for anode voltage. The V+ is connected to GND, so you have -24V on the board
- the positive gate/segment voltage is +3.3. You easily can switch BSS84 with a STM32 what is the easiest solution. This gives a total gate / segment voltage of 27.3V
- AC Filament drive is done with a full-bridge made or a two channel MOSFET driver. The output is AC coupled and pulled to about -22V. Bias is adjustable (even could be used to change the brightness)

![image](https://github.com/shufps/vfd-night-projector-clock/assets/3079832/3951aacf-8164-4a93-aad1-ff78df7fda37)

## STM32 Software

The STM32 software currently only supports a json-rpc via USB CDC. Buttons are currently unused 🙈

There is python code that can 

- measure the clock accuracy
- set the time
- set the display state and auto-switch on/off

This are small examples that nicely demonstrate how to use the json-rpc.

## 3D case

![image](https://github.com/shufps/vfd-night-projector-clock/assets/3079832/7ccb60f4-8a49-468e-9ba0-ce93a029dc57)

The case was designed in a way that no supports are needed. The upper part is simply clipped on the lower part.
