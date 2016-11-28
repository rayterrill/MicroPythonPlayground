import machine, neopixel, time
import network, socket
import ure

#turn on wifi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('ENTER_YOUR_SSID','ENTER_YOUR_WIFI_PASSWORD')
time.sleep(3)

np = neopixel.NeoPixel(machine.Pin(14), 1)

def setNeoPixel(color):
   npColor = hex_to_rgb(color)
   #convert values to gamma values
   #more info here info here: https://learn.adafruit.com/led-tricks-gamma-correction/the-issue
   gammaValues = setGammaValues(npColor)
   
   np[0] = gammaValues
   np.write()

def setGammaValues(npColor):
   r, g, b = npColor

   r = gammaEncode(r)
   g = gammaEncode(g)
   b = gammaEncode(b)
   
   gammaValues = (r, g, b)
   return gammaValues

def gammaEncode(value):
   gamma = 2.8

   #http://stackoverflow.com/questions/16521003/gamma-correction-formula-gamma-or-1-gamma
   gammaVal = ((value / 255) ^ gamma) * 255
   return gammaVal

def resetNeoPixel():
   np[0] = (0, 0, 0)
   np.write()
   
def getCheerlightsValue():
   url = 'http://api.thingspeak.com/channels/1417/field/2/last.json'
   _, _, host, path = url.split('/', 3)
   addr = socket.getaddrinfo(host, 80)[0][-1]
   s = socket.socket()
   s.connect(addr)
   s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
   #this part is super crude - not sure why i have to sleep but it seems like the data isn't ready yet
   time.sleep(1)
   data = s.recv(800)
   time.sleep(5)
   data = s.recv(400)
   #regex the color from the json data
   m = ure.search('"field2":"(#.*)"',data)
   color = m.group(1)
   return color

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

if __name__ == "__main__":
   resetNeoPixel()
   while True:
      color = getCheerlightsValue()
      setNeoPixel(color)
      time.sleep(30)
