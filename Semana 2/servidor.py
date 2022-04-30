import socket
from collections import Counter

def contadorPalavras(texto):
    count = Counter();
    palavras = texto.split()
    frequencia_palavras = {}
    for palavra in palavras:
        if palavra not in frequencia_palavras:
            count[palavra]+=1
    return count.most_common(5)

def main():
    HOST = ''
    PORTA = 5010
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock.bind((HOST,PORTA))
    sock.listen(1)
    novoSock , endereco = sock.accept()
    print('Conectado com: ' + str(endereco))
    while True:
        msg = novoSock.recv(1024) 
        if not msg: break
        with open(str(msg,encoding='utf-8')) as file:
            texto = file.read().lower()
            novoSock.send(bytes(str(contadorPalavras(texto)),'utf-8'))
    print('a')
    novoSock.close();
    sock.close(); 
main()