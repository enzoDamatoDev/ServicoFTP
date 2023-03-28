'''
Enrique Granado - 32107803
Enzo Damato - 32125992
'''
import socket #importa modulo socket

TCP_IP = '192.168.0.33' # endereço IP do servidor 
TCP_PORTA = 32125      # porta disponibilizada pelo servidor
TAMANHO_BUFFER = 1024 #tamanho do buffer

#lista dos metodos implementados
LISTA_COMANDOS = ['QUIT','GET','PUT','DELETE','DIR']

# Criação de socket TCP do cliente
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor em IP e porta especifica 
socket.connect((TCP_IP, TCP_PORTA))
print ('Conectado')

#recebe arquivo do servidor COMANDO GET
def get(arquivo):
    try:
        comando = 'GET '+arquivo # linha de comando completa
        socket.send(comando.encode('utf-8')) #envia comando pro servidor
        data = socket.recv(1024).decode("utf-8") #começa a receber o arquivo
        if data.split(' ')[0].upper() == 'ERRO': #se houver qualquer erro, retorna
            print(data)
            return
        with open(arquivo, 'w') as novoArquivo:#salva o arquivo
            while(data): #recebe cada linha do arquivo e a salva
                novoArquivo.write(data)
                data = socket.recv(1024).decode("utf-8")

                if "EOF" in data: #recebe sinal de encerramento do arquivo
                    stop_point = data.find("EOF")
                    novoArquivo.write(data[:stop_point]) #encerra o arquivo
                    print("OK")
                    return

    except Exception as e:
        print("Erro ao baixar arquivo "+arquivo)
        print(e)


#envia arquivo ao servidor COMANDO PUT
def put(arquivo):
    try:
        comando = 'PUT '+arquivo # linha de comando completa
        socket.send(comando.encode('utf-8')) #envia comando pro servidor
        with open(arquivo,'r') as arq: #abre o arquivo com nome arq
            for linha in arq: #envia cada linha do arquivo ao servidor
                socket.send(linha.encode('utf-8'))

        socket.send(('EOF').encode('utf-8')) #envia um sinal de encerramento do arquivo

    except Exception as e:
        print("Erro ao enviar arquivo "+arquivo)
        print(e)

    status = socket.recv(1024).decode("utf-8") # imprime resposta do servidor
    print(status)

#apaga um arquivo do servidor COMANDO DELETE
def delete(arquivo):
    comando = 'DELETE '+arquivo # linha de comando completa
    socket.send(comando.encode('utf-8')) #envia comando pro servidor
    print(socket.recv(TAMANHO_BUFFER).decode('utf-8')) # imprime resposta do servidor

#lista o diretorio do servidor COMANDO DIR
def listDir():
    socket.send("DIR".encode('utf-8')) #envia comando ao servidor
    print(socket.recv(TAMANHO_BUFFER).decode('utf-8')) # lista os arquivos


def main():
    while 1:
    # envia mensagem para servidor 
        mensagem  = input("> ") #input do usuario
        comando = mensagem.split(' ')[0].upper() #separa o comando usado

        if comando not in LISTA_COMANDOS: #verifica comando valido
            print('Comando inválido!')

        if comando == 'QUIT': #desconectar do servidor
            print("Desconectando")
            socket.send(comando.encode('utf-8'))
            break

        if comando == 'GET': #recebe arquivo do servidor
            try:
                arquivo = mensagem.split(' ')[1] #identifica o arquivo
                get(arquivo)

            except Exception as e:
                if 'list index out of range' in str(e): #arquivo foi fornecido?
                    print("forneça o nome do arquivo")
                else:
                    print(e)

        if comando == 'PUT': #envia arquivo ao servidor
            try:
                arquivo = mensagem.split(' ')[1] #identifica o arquivo
                put(arquivo)
            except Exception as e:
                if 'list index out of range' in str(e): #arquivo foi fornecido?
                    print("forneça o nome do arquivo")
                else:
                    print(e)
        
        if comando == 'DELETE': #apaga um arquivo do servidor
            try:
                arquivo = mensagem.split(' ')[1] #identifica o arquivo
                delete(arquivo)
            except Exception as e:
                if 'list index out of range' in str(e): #arquivo foi fornecido?
                    print("forneça o nome do arquivo")
                else:
                    print(e)

        if comando == 'DIR': #lista o diretorio do servidor
            listDir()


    print("conexão encerrada")
    socket.close()

main()