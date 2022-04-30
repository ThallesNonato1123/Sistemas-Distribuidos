import socket

HOST = 'localhost'
PORTA = 5010

sock = socket.socket();
sock.connect((HOST,PORTA))

texto = input();

while texto:
    sock.send(bytes(texto,'utf-8'))
    msg = sock.recv(1024);
    print(str(msg,encoding='utf-8'))
    texto = input();
sock.close();