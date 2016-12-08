import machine, network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('SSID','PASSWORD')

html = "HTTP/1.0 200 OK\r\n" + "Server: Micropython for ESP8266\r\n" + "Content-Type: text/plain\r\n" + "Connection: close\r\n" + "\r\n" + "Hello World!"

import socket
addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    response = html
    cl.send(response)
    cl.close()
