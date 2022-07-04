import rpyc
from rpyc import ThreadedServer
import os
import threading
from time import sleep, time


replicas = {
    1:{'host': 'localhost', 'port':10000},
    2:{'host': 'localhost', 'port':10001},
    3:{'host': 'localhost', 'port':10002},
    4:{'host': 'localhost', 'port':10003}
    }# configuração das replicas



ID = 0 #identificador global
X = 0  #variavel x
historico_global = [] #historico das alterações globais
historico_local = [] #historico das alterações locais
bastao = 1 # cópia primaira

def menu():
    print("Escolha uma das opções:\n1- Ler o valor atual de X na réplica\n2-Ler o histórico de alterações do valor de X\n3-Alterar o valor de X")
    print("4-Finalizar o programa")

def cria_servidor(id): 
    global ID
    ID = id
    
    class Replica(rpyc.Service):
        print("Replica " + str(id))
        
        def exposed_adicionaHistoria(self,valor): #função que adiciona a historia
            global historico_global
            historico_global.append(valor)

        def exposed_alterarX(self, novoValor): #função que altera o valor de x
            global X 
            X = novoValor
        
        def exposed_passoBastao(self, valor): #função para alterar o valor da copia primaria
            global bastao 
            bastao = valor
    
    srv = ThreadedServer(Replica,hostname=replicas[id]["host"] ,  port = replicas[id]["port"],protocol_config={
    'allow_public_attrs': True,}) #servidor
    srv.start()


def identifica_replica(): #identificar a replica que o usuario quer começar
    id = int(input("Escolha sua replica: "))
    carrega_replicas(id)


def carrega_replicas(id): #carrega as replicas
        global ID
        ID = id
        replica = threading.Thread(target=cria_servidor, args=(id,))
        replica.start()


def pegarX(): # pega o valor de x
    global X
    print(f"A variável X vale: {X}")

def temPermissao(ID,bastao): #verifica se a replica tem permissão para alterar a variavel x
    if(ID == bastao):
        return True
    return False

def passoBastao(ID): #função para definir a nova copia primaria
    global bastao
    print(f"Sou o id numero {ID} e quero ter a cópia primaria que pertence a {bastao}")
    for key in replicas.keys():
        if ID != bastao:
            conn = rpyc.connect(replicas[key]["host"],replicas[key]["port"])
            conn.root.passoBastao(ID)
            conn.close()


def retornar_historico(): #retorna o historico das alterações
    global historico_global,historico_local
    print(f"Alterações Globais:{historico_global}\nAlterações Locais:{historico_local}")


def alterar_x(): #função para alterar o valor de x nas replicas
    valor = int(input('Digite o valor para a variável X: '))
    global ID,bastao,historico_local
    historico_local.append((ID,valor))
    if(temPermissao(ID,bastao)):
        for key in replicas.keys():
            conn = rpyc.connect(replicas[key]["host"],replicas[key]["port"])
            conn.root.alterarX(valor)
            conn.root.adicionaHistoria((ID,valor))
            conn.close()
    else:
        passoBastao(ID)
        print(f"Agora a Copia Primária vale {bastao}")
        for key in replicas.keys():
            conn = rpyc.connect(replicas[key]["host"],replicas[key]["port"])
            conn.root.alterarX(valor)
            conn.root.adicionaHistoria((ID,valor))
            conn.close()

def interface(): #interface
    menu()
    while(True):
        op = int(input("Selcione sua escolha:"))
        print("\n")
        
        if op == 1:
            pegarX()
        elif op == 2:
            retornar_historico()
        elif op == 3:
            alterar_x()
        elif op == 4:
            os._exit(0)
        else:
            print("Opção Inválida")
        print("\n")
        menu()

def main():
    identifica_replica()
    interface()
main()