#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                   # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        imageW = "img/recebidaCopia.jpg"
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.

        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.05)
        print("enviando 1 byte de sacrifício")
        com1.sendData(np.asarray(b'x00'))    #enviar byte de lixo
        print('enviou bytte sacrificio')
        time.sleep(.05)
        print("*******Início handshake*******")
        rxBuffer, nRx = com1.getData(15)
        print(rxBuffer)
        time.sleep(.05)
        print('Comçando transmissão de dados:')
    
        com1.sendData(np.asarray(rxBuffer))    #enviar byte de lixo
        time.sleep(.05)
        print("*******Final handshake*******")
        indice=0
        payloads=b""
        while True:
            com1.rx.clearBuffer()
            int_list = [int(byte) for byte in rxBuffer]
            tamanho=int_list[2]
            print(tamanho, "____________________" ,int_list[1])
            print("indices", int_list[0], int_list[1])
            if int_list[0]==int_list[1]:
                print("=============TERMINOU=============")
                break


            print("esperando pacote")
            rxBuffer, nRx = com1.getData(tamanho)
            recebe_int = [int(byte) for byte in rxBuffer]
            payloads+=rxBuffer[12:-3]
            print("AAAAAAAAAAAAAAAA",payloads)

            
            if indice!=int_list[0]:
                print("PACOTE FORA DE ORDEM")
            if (int_list[-1]!=255) or (int_list[-2]!=255) or (int_list[-1]!=255):
                print("ERRO EOP")
            if len(recebe_int)!=int_list[2]:
                print("ERRO TAMANHO")



            time.sleep(0.05)
            print("#################")
            print(rxBuffer[0:12]+rxBuffer[-3:])
            print("#################")
            com1.sendData(rxBuffer[0:12]+rxBuffer[-3:])
            print("")
            print(rxBuffer)
            print("")
            indice+=1
        f = open(imageW,'wb')
        f.write(payloads)
        f.close
        


        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
