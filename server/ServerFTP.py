'''
Enrique Granado - 32107803
Enzo Damato - 32125992
'''



import socket, os #importa modulo socket

command_list = ["QUIT","GET","PUT","DELETE","DIR"] #lista de comandos implementados

HOST = '192.168.0.33' # ip do host
PORTA = 32125 # porta do processo
TAMANHO_BUFFER = 1024 # tamanho do buffer

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# iniciar socket

print (f"agardando conexão IP {HOST} porta {PORTA}")

servidor.bind((HOST, PORTA)) #conectar ao cliente
servidor.listen()
conn, addr = servidor.accept()

print ('Conectado')

'''
As funções implementadas aqui são a partir da visão do cliente
''' 

#envia arquivo ao cliente COMANDO GET
def get(arquivo):
    try:
        with open(arquivo,'r') as arq: #abre o arquivo com nome arq
            for linha in arq: #envia cada linha do arquivo ao cliente
                conn.send(linha.encode('utf-8'))

        conn.send(('EOF').encode('utf-8')) #envia um sinal de encerramento do arquivo
        print("OK")
    except Exception as e:
        print("Erro ao enviar arquivo "+arquivo)
        print(e)
        conn.send(('ERRO '+str(e)).encode('utf-8')) #retorna o erro ao cliente

#recebe arquivo do cliente COMANDO PUT
def put(arquivo):
    try:
        print("baixando arquivo "+arquivo)
        data = conn.recv(1024).decode("utf-8") #começa a receber o arquivo
        with open(arquivo, 'w') as novoArquivo: #salva o arquivo
            while(data): #recebe cada linha do arquivo e a salva
                novoArquivo.write(data)
                data = conn.recv(1024).decode("utf-8")

                if "EOF" in data: #recebe sinal de encerramento do arquivo
                    stop_point = data.find("EOF")
                    novoArquivo.write(data[:stop_point]) #encerra o arquivo
                    conn.send(('OK').encode('utf-8')) #retorna OK ao cliente
                    return

    except Exception as e:
        print("Erro ao baixar arquivo "+arquivo)
        print(e)
        conn.send(('ERRO '+str(e)).encode('utf-8'))

#apaga um arquivo local COMANDO DELETE
def delete(arquivo):
    if os.path.exists(arquivo): #verifica a existencia do arquivo
        os.remove(arquivo) #remove o arquivo
        print("Arquivo removido "+arquivo)
        conn.send("OK".encode('utf-8')) #retorna ok ao cliente
    else:
        print(arquivo)
        conn.send("Inexistente".encode('utf-8')) #retorna erro ao cliente

#lista o diretorio local COMANDO DIR
def listDir():
    arquivos = os.listdir("./") #lista os arquivos da paasta atual
    conn.send(str(arquivos).encode('utf-8'))
    print(str(arquivos))

def main():
    while 1: #escuta continuamente a conexão

        data = conn.recv(TAMANHO_BUFFER).decode('UTF-8') #recebe a linha de comando
        comando = data.split(' ')[0].upper() #identifica o comando especifico
        if data: 
            print ("Cliente:", data)

        if(comando == 'QUIT'): #encerra a aplicação
            break

        if comando == "GET": #envia arquivo ao cliente
            arquivo = data.split(' ')[1] #identifica o arquivo
            get(arquivo)

        if comando == "PUT": #recebe arquivo do cliente
            arquivo = data.split(' ')[1] #identifica o arquivo
            put(arquivo)

        if comando == "DELETE": #apaga um arquivo local
            arquivo = data.split(' ')[1] #identifica o arquivo
            delete(arquivo)

        if comando == "DIR": #lista o diretorio local
            listDir()
        
        
    print("conexão encerrada")
    servidor.close()

main()