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
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.

        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.05)
        rxBuffer, nRx = com1.getData(1)
        time.sleep(.05)
        tamanho_esperado=int.from_bytes(rxBuffer)
        print(f"tamanho esperado: {tamanho_esperado}")
        rxBuffer, nRx = com1.getData(tamanho_esperado)
            
        for i in range(len(rxBuffer)):
            print("recebeu {}" .format(rxBuffer[i]))    
    
        
        print('\n')
        print(rxBuffer)      
        print('\n')
        comandos=str(rxBuffer)[2:].lower().split("xff")
        qnt_comandos=str(rxBuffer).lower().count("ff".lower())
        print()
        for i in comandos:
            print(i[:-1])
        print()
        time.sleep(.05)


        print('Comçando transmissão de dados:')
        com1.sendData(np.asarray(b'x00'))    #enviar byte de lixo
        time.sleep(.5)
        #com1.sendData(qnt_comandos.to_bytes(1)) 
        com1.sendData(b"\xBB")         
        txSize = com1.tx.getStatus()
        print('quantidade de comandos = {}' .format(qnt_comandos))


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
