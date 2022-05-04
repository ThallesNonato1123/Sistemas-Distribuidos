import socket
#biblioteca para pegar um contador
from collections import Counter

#algoritmo para contar palavras
def contadorPalavras(texto):
    count = Counter();
    palavras = texto.split()
    for palavra in palavras:
            count[palavra]+=1
    #retorna as 5 palavras mais comuns
    return count.most_common(5)

def main():
    #definindo host, porta e socket
    HOST = ''
    PORTA = 5010
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock.bind((HOST,PORTA))
    sock.listen(1)
    novoSock , endereco = sock.accept()
    print('Conectado com: ' + str(endereco))
    while True:
        #recebe o arquivo que vai ser lido
        msg = novoSock.recv(1024) 
        if not msg: break
        try:
            with open(str(msg,encoding='utf-8')) as file:
                texto = file.read().lower()
            #envia as strings em ordem (.send da biblioteca socket não aceita tuple,list e etc.. aparentemente só string)
            novoSock.send(bytes(str(contadorPalavras(texto)),'utf-8'))
        except FileNotFoundError:
            novoSock.send(bytes("Erro: o arquivo nao foi encontrado",'utf-8'))
    novoSock.close();
    sock.close(); 
main()
