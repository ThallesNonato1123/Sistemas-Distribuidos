import socket
HOST = '' #ip do host (vazio = default)
PORT = 5000 #porta( porta > 1024)
# par host e port = identificação do processo na máquina

#criar o descritor socket
sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM); #Internet e TCP

#vincular o endereco e porta
sock.bind((HOST,PORT))
#colocar-se em modo de espera
sock.listen(1) #argumento indica qtde de conexões pendentes

#aceitar conexao / pode ser um nó bloqueante
novoSock , endereco = sock.accept();
print('Conectado com: ' + str(endereco));

#esperar por mensagem do lado ativo
while True:
    msg = novoSock.recv(1024) #argumento indica qtde maxima de bytes
    if not msg: break
    novoSock.send(bytes(msg))
#fechar o descritor de socket da conexao
novoSock.close();
#fechar o descritor da conexao
sock.close(); 