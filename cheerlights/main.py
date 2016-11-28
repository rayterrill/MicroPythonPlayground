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
   #hardcoding values for now because of LED trickery/Gamma Correction. More info here: https://learn.adafruit.com/led-tricks-gamma-correction/the-issue
   #need to add gamma correction support
   if color == '#FFC0CB': #pink
      npColor = (255, 48, 48)
   elif color == '#FFA500': #orange
      npColor = (255, 36, 0)
   else :
      npColor = hex_to_rgb(color)
   
   np[0] = npColor
   np.write()

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
