import socket

HOST='localhost'
PORT= 5000

#criar o descritor de socket
sock = socket.socket()

#estabelecer conexao
sock.connect((HOST,PORT))

#enviar msg de hello
texto = input();

while texto:
    sock.send(bytes(texto,'utf-8'))
    msg = sock.recv(1024);
    print(str(msg,encoding='utf-8'))
    texto = input();

#encerrar a conexao
sock.close();