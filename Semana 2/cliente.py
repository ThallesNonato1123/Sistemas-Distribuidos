import socket

#definindo host e porta
HOST = 'localhost'
PORTA = 5010

#criar o descritor do socket
sock = socket.socket();

#estabelecer conexao
sock.connect((HOST,PORTA))

#enviar msg de hello
texto = input();

#loop só acaba quando o usuário da enter
while texto:
    #envia o nome do arquivo.txt
    sock.send(bytes(texto,'utf-8'))
    #recebe a resposta do servidor
    msg = sock.recv(1024);
    print(str(msg,encoding='utf-8'))
    texto = input();

#encerrar a conexão
sock.close();