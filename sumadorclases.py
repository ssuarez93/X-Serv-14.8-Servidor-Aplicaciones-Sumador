#!/usr/bin/python
# -*- coding: utf-8 -*-
# Sistemas Teleco. Sara Suárez.

import socket
import random

class WebApp:
    def parse(self, request):
        numero = int(request.split()[1][1:])
        return numero
    def process(self, parsedRequest):
        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")
    def suma(self, arg1, arg2):
        return arg1 + arg2
    def __init__(self, hostname, port):
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind(('localhost', 1234))

        mySocket.listen(5)
        primer_num = None

        try:
            while True:
                print 'Waiting for connections'
                (recvSocket, address) = mySocket.accept()
                print 'HTTP request received:'
                peticion = recvSocket.recv(1024)
                print peticion
                try:
                    numero = self.parse(peticion)
                except ValueError:
                    recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
                                    "<html><body><font size=6><font face=Comic Sans MS>Debes introducir un numero despues de 'http://localhost:1234/'")
                    continue

                if primer_num==None:
                    primer_num = numero
                    recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
                                    "<html><body><font size=6><font face=Comic Sans MS>Mandame el segundo numero para hacer la suma")
                else:
                    resultado = self.suma(primer_num, numero)
                    recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
                                    "<html><body><font size=6><font face=Comic Sans MS>" + str(primer_num) +
                                    " + " + str(numero) + " = " + str(resultado))
                    primer_num = None

            recvSocket.close()
        except KeyboardInterrupt:
	        print "Closing binded socket"
	        mySocket.close()

if __name__ == "__main__":
    testWebApp=WebApp("localhost", 1234)
