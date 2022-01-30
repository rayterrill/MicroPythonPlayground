import machine, neopixel, time
import network, socket
import ure
import urequests
import json
import os
import sys

COLORS = {
   'red': (0, 255, 0),
   'green': (255, 0, 0),
   'blue': (0, 0, 255),
   'cyan': (255, 0, 255),
   'white': (255, 255, 255),
   'oldlace': (145, 153, 130),
   'purple': (0, 128, 128),
   'magenta': (0, 255, 51),
   'yellow': (170, 255, 0),
   'orange': (34, 255, 0),
   'pink': (51, 255, 119)
}

SLEEP = .1

def setNeoPixel(color):
   val = COLORS[color]
   
   np[0] = val
   np.write()

def resetNeoPixel():
   np[0] = (0, 0, 0)
   np.write()

def circleColors():
   for key in COLORS:
      np[0] = COLORS[key]
      np.write()
      time.sleep(SLEEP)

def getCheerlightsValue():
   url = 'http://api.thingspeak.com/channels/1417/field/1/last.json'
   r = urequests.get(url)
   json = r.json()
   
   return json['field1']

if __name__ == "__main__":
   np = neopixel.NeoPixel(machine.Pin(14), 1)
   resetNeoPixel()

   from captive_portal import CaptivePortal

   portal = CaptivePortal()

   portal.start()

   #loop 3 times to indicate we're connected
   for i in range(3):
      circleColors()

   while True:
      while True:
         try:
            color = getCheerlightsValue()
            setNeoPixel(color)
         except:
            print('Looks like we had an error on getting our color.')
         time.sleep(30)
