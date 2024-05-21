from random import randint
from time import sleep

#TURNOS
def combate(config, inimigo, turno):
    #O JOGADOR ESTÁ VIVO?
    if config[0][2] > 0:
        #O INIMIGO MORREU ?
        if inimigo[1] <= 0:
            print(f" O {inimigo[0]} foi derrotado. Parabens !")
            print(f" Você receber {inimigo[7]} de xp, e agora seu xp é {config[3][5]}")
            config[3][5] += inimigo[7]

            #EXISTE ALGUM ITEM A SER PEGO?
            #print("Vasculhando em busca de itens...")
            #sleep(2.3)
            #vasculharRestos(config, inimigo)         

        #SE NÃO, ROLE O TURNO
        else:
            if turno == "j":
                print(f"Um {inimigo[0]} está a sua frente!")
                menuDeAcoes(config,inimigo)

            elif turno == 'i':
                if inimigo[1] >= 0:
                    print(f"O turno é do {inimigo[0]}")
                    ataqueInimigo(inimigo,config)

                #SE O JOGADOR TIVER VIDA, PASSE O COMBATE DE VOLTA PARA ELE
                else: 
                    return config
                
    #SE NÃO, ENCERRE O COMBATE
    else:
        print("VOCÊ MORREU (╥﹏╥) ")
        return False

#MENU JOGADOR
def menuDeAcoes(config,inimigo):
    print("------------------------É seu turno! O que deseja fazer ?------------------------")
    print("| :ATACAR     |\n| :INVENTARIO |\n| :FUGIR      |")
    n = ''
    while n != "ATACAR" and n != "INVENTARIO" and n != "FUGIR":
        n = input("| Digite sua escolha:  ")

    #ATACANDO
    if n == "ATACAR":
        i = 0
        while i < 5:
            if config[1][i] != None:
                print(f"{i} -> {config[1][i]}")
                i+=1
            else:
                i+=1
        
        j = -1
        while not(0 <= j <= 5):
            j = int(input("Escolha um item a ser usado:  "))
            ataqueJogador(config, j , inimigo)

    elif n == "INVENTARIO":
        #MOSTRANDO O INVENTARIO
        verInventario(config)
        #CHAMANDO NOVAMENTE O MENU DE AÇÕES
        menuDeAcoes(config,inimigo)
    else:
        print("Tentando fugir...")
        sleep(0.7)
        chanceDeEscapar = config[0][5] + randint(1,20)
        if chanceDeEscapar < 10:
            print("Você correu!!")
            #ENCERRANDO O COMBATE
            return config
        else:
            print("O inimigo não te deixa partir, e agora é o turno dele!!")
            sleep(0.5)
            #PASSANDO O TURNO DE VOLTA PARA O INIMIGO
            combate(config,inimigo,"i")

#GERADORES
def gerarInimigo(inimigo):
    inimigoConfig = []
    if inimigo == 1:
        inimigoConfig.append("Javali")
        inimigoConfig.append(12)
        inimigoConfig.append(5)
        inimigoConfig.append(None)
        inimigoConfig.append("Presas de Javali")
        inimigoConfig.append(5)
        inimigoConfig.append(1)
        inimigoConfig.append(10)

    elif inimigo == 2:
        inimigoConfig.append("Esquilo Com AIDS")
        inimigoConfig.append(2)
        inimigoConfig.append(6)
        inimigoConfig.append(None)
        inimigoConfig.append("Adaga Homofobica")
        inimigoConfig.append(1)
        inimigoConfig.append(4)
        inimigoConfig.append(10)
    elif inimigo == 3:
        inimigoConfig.append("Guaxinim")
        inimigoConfig.append(12)
        inimigoConfig.append(10)
        inimigoConfig.append("Manto Do Bandido")
        inimigoConfig.append("3Oitao")
        inimigoConfig.append(6)
        inimigoConfig.append(2)
        inimigoConfig.append(10)
    elif inimigo == 4:
        inimigoConfig.append("Lobo Pidão")
        inimigoConfig.append(16)
        inimigoConfig.append(7)
        inimigoConfig.append(None)
        inimigoConfig.append("Me jogue aos lobos e eu voltarei, ai ai me morederam")
        inimigoConfig.append(6)
        inimigoConfig.append(3)
        inimigoConfig.append(12)
    elif inimigo == 5:
        inimigoConfig.append("Goblin")
        inimigoConfig.append(12)
        inimigoConfig.append(8)
        inimigoConfig.append("Roupas velhas (8)")
        inimigoConfig.append("Saraivada de Lanças")
        inimigoConfig.append(4)
        inimigoConfig.append(4)
        inimigoConfig.append(12)
    elif inimigo == 6:
        inimigoConfig.append("Tartaruga")
        inimigoConfig.append(1)
        inimigoConfig.append(19)
        inimigoConfig.append("Casco de Tartaruga")
        inimigoConfig.append("Bonk")
        inimigoConfig.append(1)
        inimigoConfig.append(1)
        inimigoConfig.append(20)
    return inimigoConfig

#ATAQUES
def ataqueJogador(config,escolha, receptor):
    acerto = (randint(1,20))
    sleep(1.2)
    print(f"Você rolou um {acerto}")
    sleep(0.5)
#         AGILIDADE     CHANCE     CA-INIMIGO
    if (config[0][4] + acerto) >= receptor[2]:
        #ACERTOU
        if config[2][escolha] == None:
            print("Não há itens nesse slot, ataque perdido")
        else:
            #   NÃO É MAGO ?         '''DANO DA ARMA'''  '''FORÇA''' 
            if config[0][0] != 3:
                dano = randint(1, config[2][escolha]) + config[0][2]
                receptor[1] -= (dano)
                print(f"Você deu {dano} de dano no {receptor[0]}, e a vida dele agora é {receptor[1]}")
            #É MAGO, ENTÃO USE INTELIGENCIA NO DANO 
            else:
                dano = randint(1, config[2][escolha]) + config[0][3]
                receptor[1] -= (dano)
                print(f"Você deu {dano} de dano no {receptor[0]}, e a vida dele agora é {receptor[1]}")
        sleep(0.5)
        combate(config,receptor, "i")

    else:
        print("O inimigo desviou")
        sleep(0.5)
        combate(config,receptor, "i")

def ataqueInimigo(inimigo,config):
    sleep(0.5)
    acerto = randint(1,20) + inimigo[6]
    if acerto >= config[2][5]:
        print(f"O {inimigo[0]} acertou, e utilizando um {inimigo[4]} ele te deu {inimigo[5]} de dano!")
        config[0][2] -= inimigo[5]
        sleep(0.5)
        combate(config, inimigo, "j")
    else:
        print(f"o {inimigo[0]} tentou usar {inimigo[4]}, porém errou!!!")
        sleep(0.5)
        combate(config, inimigo, "j")
        
#INVENTARIO
def vasculharRestos(config, inimigo):
    if inimigo[4] != (None):
        print("\n------------------------ item descoberto ------------------------ ")
        print(f"O inimigo deixou cair sua arma, você verifica e encontra uma {inimigo[4]} que dá até {inimigo[5]} de dano")
        print("Deseja pegar e adicionar ao inventario?")
        e = ""
        while e != "SIM" and e != "NAO":
            e = input("SIM ou NAO:  ")
        if e == "SIM":
            i = 0
            invfull = 0
            while i < 5:
                if config[1][i] != (None):
                    invfull +=1
                    i+=1
                else: 
                    config[1][i] = inimigo[4]
                    config[2][i] = inimigo[5]
                    i = 6
                if invfull == 5:
                    print("O seu inventario está cheio, deseja trocar o item encontrado por algum que você possua?")
                    e = ""
                    while e != "SIM" and e != "NAO":
                        e = input("SIM ou NAO:  ")
                    if e == "SIM":
                        print("Por qual ?")
                        print(f"0 - {config[1][0]} \n 1 - {config[1][1]} \n 2 - {config[1][2]} \n 3 - {config[1][3]} \n 4 - {config[1][4]}")
                        e = -1
                        while not(0 <= e <= 4):
                            e = int(input(":  "))
                        config[1][e] = inimigo[4]
                        config[2][e] = inimigo[5]
                #A ALGUMA ARMADURA A SER PEGA ?
    else:
        print("Não há armas a serem pegas!")
    if inimigo[3] != (None):
        print("\n------------------------ item descoberto ------------------------")
        print(f"O inimigo também deixou cair um {inimigo[3]}, que te dá {inimigo[2]} de CA, deseja vestir ao invés de {config[1][5]} que te dá {config[2][5]}")
        e = ""
        while e != "SIM" and e != "NAO":
            e = input("SIM ou NAO:  ")
        if e == "SIM":
            config[1][5] = inimigo[3]
            config[2][5] = inimigo[2]
        else:
            return config
    else:
        print("Não há armaduras a serem pegas!")
        return config

def verInventario(config):
    i = 0
    print(f"|Vida : {config[0][1]}/{config[0][2]} |For: {config[0][3]} | Int: {config[0][4]} |Agl: {config[0][5]} | Xp: {config[3][5]} |")
    print("E olhando na mochila se percebe que... ")
    print("Você possui: ")
    while i < 5:
        if config[1][i] != None:
            print(f"° um(a) {config[1][i]}. Dano - > {config[2][i]}")
            i+=1
        else:
            i+=1
    print(f"Verificando a armadura que carrega você vê um(a) {config[1][5]}, que te faz ter {config[2][5]} de CA")




jogador = [[3, 18 , 18, 1, 5, 2],["Flaminha", "Chamas tracejantes", None, None, None, "Manto do Mago"], [1, 8, None, None , None, 8],[None, None, None, None, None, 0]]

combate(jogador,gerarInimigo(3),"j")


'''
README
PARA INICIAR UM COMBATE DEVESE USAR A FUNÇÃO:
combate([jogador],[gerarInimigo(3)],["j"])
Exemplo:
combate(jogador,gerarInimigo(3),"j")


Nessa função, o primeiro parametro é as configurações do jogador(inventario, vida, CA, etc...)
O segundo paramentro é o inimigo as configurações do inimigo, tendo como parametro o inimigo especifico.
O terceiro paramentro sempre deve ser iniciado com ["j"], pois declara de quem é o turno, o valor (j) é de jogador e o valor (i) é de inimigo.


'''



