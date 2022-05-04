#bibliotecas 
import socket
import select
import sys
import threading
from collections import Counter


HOST = ''
PORT = 5013
#lista com stdin para ter controle do server manualmente (sem dar ctrl c ou ctrl z)
entradas = [sys.stdin]

#dicionario para listar as conexoes
conexoes = {}
#variavel de exclusão mutua 
lock = threading.Lock()

#algoritmo para contar palavras
def contadorPalavras(texto):
    count = Counter();
    palavras = texto.split()
    for palavra in palavras:
            count[palavra]+=1
    #retorna as 5 palavras mais comuns
    return count.most_common(5)
#Configurações do Serivodr

#iniciação do socket
def iniciaServidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST,PORT))
    sock.listen(5)
    sock.setblocking(False)
    return sock

#aceite da conexão
def aceitaConexao(sock):
    clientSock, endereco = sock.accept()
    return clientSock, endereco

#atendimento das requisições para ler o arquivo e executar o algoritmo
def atendeRequisicoes(clientSock):
    while True:    #recebe o arquivo que vai ser lido
        msg = clientSock.recv(1024) #arquivo reebido
        if not msg:
            #lock para acesso unico a conexões (é acessada abaixo)
            lock.acquire()
            del conexoes[clientSock]
            lock.release()
            clientSock.close()
            return
        try:
            with open(str(msg,encoding='utf-8')) as file:
                texto = file.read().lower()
            #envia as strings em ordem (.send da biblioteca socket não aceita tuple,list e etc.. aparentemente só string)
            clientSock.send(bytes(str(contadorPalavras(texto)),'utf-8'))
        except:
                clientSock.send(bytes("Erro: o arquivo nao foi encontrado",'utf-8'))

def main():
    sock = iniciaServidor()
    entradas.append(sock);
    while True:
        r,w,e = select.select(entradas,[],[]) #receber entradas do S.O ou usuario
        for pronto in r:
                if pronto == sock: # se for um sock, tratar a chamada
                    clientsock, endereco = aceitaConexao(sock)
                    print('Conectado com: ',endereco)
                    lock.acquire()
                    conexoes[clientsock] = endereco #dicionario para pegar os endereços
                    lock.release()
                    cliente = threading.Thread(target=atendeRequisicoes,args = (clientsock,)) #cade thread cuida de uma requisição do cliente
                    cliente.start()
                elif pronto == sys.stdin: #se for um stdin, tratar o caso 
                    cmd = input()
                    if cmd == "fim":
                        if not conexoes:
                            sock.close(); #encerrar o socket
                            sys.exit(); #encerrar o programa em caso de "fim"
                        else:
                            print('Há conexões ativas')     
main()