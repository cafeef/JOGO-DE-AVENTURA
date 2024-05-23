from random import randint
from random import choice
from colorama import Fore
from colorama import Style
from time import sleep


'''
Legenda Numeros (pode ser trocada):
0- Espaço vazio
1- Floresta densa (não pode ser destruido, obstáculo)
2- Obstaculo do ambiente (arvore)
3- Água (existe a chance dele levar dano (afogamento) ou enfrentar um monstro aquatico)(Posso colocar chance de ter tesouros)
4- Obstaculo do ambiente (pedra)
5- Parede de madeira (pode ser destruida com explosivos ou outros items)(guardam items em estruturas)
6- Item (quando o jogador passa por 6 um item é adicionado ao seu inventário e o local é substituido por 0)
7- Baú (pode ser destruído)(contém um item)(pode ser aberto usando uma chave)
8- Armadilha (não definido)
'''
#Inicializando matriz vazia quadrada de tamanho escolhido
def inicializa(tamanho):
    mapa_ = []
    for i in range(0, tamanho):
        line = []

        for j in range(0, tamanho):
            line.append([0, False])
        mapa_.append(line)
    return mapa_
#Gera um inimigo baseado em dificuldade(quanto maior o número mais forte é o inimigo) em qualquer região do mapa
def geradorInimigo(spawn_zone, dificuldade= 1):
    randomy= randint(0, len(spawn_zone)-1)
    randomx= randint(0, len(spawn_zone)-1)
    if spawn_zone[randomy][randomx][0] != 0:
        geradorInimigo(spawn_zone, dificuldade)
    else:
        try:
            spawn_zone[randomy][randomx][0]= randint(9, 12)+ dificuldade
        except IndexError:
            geradorInimigo(spawn_zone, dificuldade)
#Gera uma armadilha no mapa
def geradorArmadilha(spawn_zone):
    randomy= randint(0, len(spawn_zone)-1)
    randomx= randint(0, len(spawn_zone)-1)
    if spawn_zone[randomy][randomx][0] != 0:
        geradorInimigo(spawn_zone)
    else:
        try:
            spawn_zone[randomy][randomx][0]= 8
        except IndexError:
            geradorInimigo(spawn_zone)
#Gera obstaculos tipo 2 e 4 no mapa (baseado em probabilidade em uma area)
def geradorAmbiente(spawn_zone : list,treeProbability= 2, spread_amount= 2):
    i= 0
    tObstaculo= choice((2,4))
    randomY= randint(0, len(spawn_zone))
    randomX= randint(0, len(spawn_zone))
    try:
        if spawn_zone[randomY][randomY][0] == 0:
            spawn_zone[randomY][randomX][0]= tObstaculo

    except IndexError:
        geradorAmbiente(spawn_zone, treeProbability, spread_amount)
    
    while i < treeProbability:
        randomSpreadX= randint(1,spread_amount)
        randomSpreadY= randint(1,spread_amount)
        try:
            if spawn_zone[randomY+ randomSpreadY][randomX+ (randomSpreadX)][0] == 0:
                spawn_zone[randomY+ randomSpreadY][randomX+ (randomSpreadX)][0]= tObstaculo
        except IndexError:
            pass
        i+= 1
#Gera estruturas retangulares(com diferença de no maximo 1) ou quadradas de material tMaterial e preenchida com items tItems no mapa
#Para entrar nas estruturas é necessário destruir o material tMaterial
def geradorEstrutura(spawn_zone, sizeX, sizeY):
    tMaterial= 5
    tItem= 6
    i= 0
    randomY= randint(0, len(spawn_zone)-sizeY-1)
    randomX= randint(0, len(spawn_zone)-sizeX-1)
    while i < 30:
        fillX= randint(1,sizeX)
        fillY= randint(1, sizeY)
        try:
            maior= max(sizeY,sizeX)
            if spawn_zone[randomY+ fillY][randomX+ fillX][0] == 0 and maior== sizeY:
                spawn_zone[randomY+ fillY-1][randomX+ fillX][0]= tItem
            if spawn_zone[randomY+ fillY][randomX+ fillX][0] == 0 and maior== sizeX:
                spawn_zone[randomY+ fillY][randomX+ fillX-1][0]= tItem
        except IndexError:
            geradorEstrutura(spawn_zone, sizeX, sizeY)
        i+= 1
    
    try:
        i= 0    
        spawn_zone[randomY][randomX][0]= tMaterial
        while i < sizeX:
            spawn_zone[randomY+i][randomX][0]= tMaterial
            spawn_zone[randomY][randomX+i][0]= tMaterial
            spawn_zone[randomY+i][randomX+ sizeY][0]= tMaterial
            i+= 1
        i= 0
        while i < sizeY:
            spawn_zone[randomY+i][randomX][0]= tMaterial
            spawn_zone[randomY][randomX+i][0]= tMaterial
            spawn_zone[randomY+ sizeX][randomX+ i][0]= tMaterial
            i+= 1
    except IndexError:
        geradorEstrutura(spawn_zone, sizeX, sizeY)

        i+= 1
#Gera um rio que percorre horizontalmente todo o mapa em uma faixa escolhida
def geradorRio(spawn_zone):
    i= 0
    while i < len(spawn_zone[0]): 
        spawn_zone[randint(0,len(spawn_zone)-1)][i][0]= 3
        spawn_zone[randint(0,len(spawn_zone)-1)][i][0]= 3
        i+=1
#Gera um lago quadrado no mapa
def geradorLago(spawn_zone, tamanho):
    i= 0
    randomY= randint(0, len(spawn_zone))
    randomX= randint(0, len(spawn_zone))
    try:
        if spawn_zone[randomY][randomY][0] == 0:
            spawn_zone[randomY][randomX][0]= 2

    except IndexError:
        geradorAmbiente(spawn_zone, tamanho)
    
    while i < 25:
        tamanho_lagoX= randint(1,tamanho)
        tamanho_lagoY= randint(1,tamanho)
        try:
            if spawn_zone[randomY+ tamanho_lagoY][randomX+ (tamanho_lagoX)][0] == 0:
                spawn_zone[randomY+ tamanho_lagoY][randomX+ (tamanho_lagoX)][0]= 3
        except IndexError:
            pass
        i+= 1
#Gera um baú com maior probabilidade de posicionamento nos cantos do mapa
def geradorBau(spawn_zone):
    size= len(spawn_zone)
    randomy= randint(0, size-1)
    n1= randint(0, size-int((size/1.5)))
    n2= randint(int((size/1.5)), size-1)
    randomx= choice((n1, n2))
    if spawn_zone[randomy][randomx][0] != 0:
        geradorBau(spawn_zone)
    else:
        try:
            spawn_zone[randomy][randomx][0]= 7
        except IndexError:
            geradorBau(spawn_zone)
#Verifica se o player está perto de água
def checkWater(xpos : int, ypos : int):
    for y, x in ((1,0),(-1,0),(0,1),(0,-1)):
        if mapa_gerado[ypos+y][xpos+x] == 3:
            mapa_gerado[ypos+y][xpos+x][1]= True
#Verifica se o jogador pode ir em uma direção
#Marca território percorrido
def verificandoEspaço(direction):
    global xPosition
    global yPosition
    if direction % 2==0:
        zone_move= mapa_gerado[yPosition+ int(direction/2)][xPosition][0]
        if (zone_move == 0) or (zone_move == 3):
            yPosition += int(direction/2)
            return 0
        else:
            mapa_gerado[yPosition+ int(direction/2)][xPosition][1]= True
            return zone_move
    else:
        zone_move= mapa_gerado[yPosition][xPosition+ direction][0]
        if (zone_move == 0) or (zone_move == 3):
            xPosition += direction
            return 0
        else:
            mapa_gerado[yPosition][xPosition+ direction][1]= True
            return zone_move
#Oferecendo uma versão legível do mapa
def transformadorUI(mapa : list, ypos: int, xpos: int):
    count1=0
    count2=0
    for lines in mapa:
        visualizacaoS= ''
        visualizacaoI= ''
        count2= 0
        for colunas in lines:
            if True:
                #Verificando posição do jogador e colocando P de jogador na visualização
                if (count1== ypos) and (count2== xpos):
                    count2+=1
                    visualizacaoS+= '   '
                    visualizacaoI+= 'P  '
                    continue
                #Comparando colunas[0] com cada case e adicionando na linha de visualização o símbolo correspondente
                #Biblioteca colorama permite adicionar cor ao texto
                match colunas[0]:
                    case 0:
                        visualizacaoS+= '   '
                        visualizacaoI+= '   '
                    case 1:
                        visualizacaoS+= f'{Fore.GREEN}_  {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.GREEN}T  {Style.RESET_ALL}'
                    case 2:
                        visualizacaoS+= f'{Fore.GREEN}_  {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.GREEN}T  {Style.RESET_ALL}'
                    case 3:
                        visualizacaoS+= f'{Fore.BLUE}~  {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.BLUE}~  {Style.RESET_ALL}'
                    case 4:
                        visualizacaoS+= f'{Fore.LIGHTBLACK_EX}_  {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.LIGHTBLACK_EX}o  {Style.RESET_ALL}'
                    case 5:
                        visualizacaoS+= f'{Fore.YELLOW}{Style.DIM}#  {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.YELLOW}{Style.DIM}#  {Style.RESET_ALL}'
                    case 6:
                        visualizacaoS+= '   '
                        visualizacaoI+= f'{Fore.LIGHTYELLOW_EX}§  {Style.RESET_ALL}'
                    case 7:
                        visualizacaoS+= f'{Fore.YELLOW}$  {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.YELLOW}B  {Style.RESET_ALL}'
                    case 8:
                        visualizacaoS+= f'{Fore.LIGHTRED_EX}_  {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.LIGHTRED_EX}X  {Style.RESET_ALL}'
                    case 10:
                        visualizacaoS+= f' {Fore.RED}O {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.RED}| |{Style.RESET_ALL}'
                    case 11:
                        visualizacaoS+= f'{Fore.RED}## {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.RED}|| {Style.RESET_ALL}'
                    case 12:
                        visualizacaoS+= f' {Fore.RED}@ {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.RED}| |{Style.RESET_ALL}'
                    case 13:
                        visualizacaoS+= f'{Fore.RED}XX {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.RED}|| {Style.RESET_ALL}'
                    case 19:
                        visualizacaoS+= f'{Fore.WHITE}^  {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.WHITE}|  {Style.RESET_ALL}'
                    case 20:
                        visualizacaoS+= '   '
                        visualizacaoI+= '   '
            else:
                visualizacaoS+= '   '
                visualizacaoI+= '   '
            count2+=1
        count1+=1
        print(visualizacaoS)
        print(visualizacaoI)

def movimento():
    while True:
        mapa_gerado[yPosition][xPosition][1]= True
        checkWater(xPosition, yPosition)
        comando= str(input('Escolha uma direção para ir: '))
        comando= comando.lower()
        if comando == 'n':
            evento= verificandoEspaço(-2)
        elif comando == 's':
            evento= verificandoEspaço(2)
        elif comando == 'l':
            evento= verificandoEspaço(1)
        elif comando == 'o':
            evento= verificandoEspaço(-1)
        else:
            print('Direção inválida')
            continue
        transformadorUI(mapa_gerado, yPosition, xPosition)
        mapa_gerado[yPosition][xPosition][1]= True
        print(xPosition)
        print(yPosition)
        print(evento)

def iniciandoMapa(n):
    tamanho= n
    global mapa_gerado
    mapa_gerado= inicializa(tamanho)
    wall= []

    #Gerando o mapa
    geradorInimigo(mapa_gerado)
    i=0
    while i <8:
        geradorAmbiente(mapa_gerado, 4, 3)
        i+=1
    geradorEstrutura(mapa_gerado, 3, 4)
    geradorEstrutura(mapa_gerado, 3, 3)
    geradorRio(mapa_gerado[3:5])
    geradorLago(mapa_gerado, 3)
    geradorBau(mapa_gerado)
    geradorArmadilha(mapa_gerado)



    #Adicionando bordas
    for linha in mapa_gerado:
        linha.insert(0, [1, False])
        linha.append([1, False])

    for i in range(0, tamanho+2):
        wall.append([1, False])
    mapa_gerado.insert(0, wall)
    #Reset para evitar criar 2 vetores com mesmo endereço de memória e acidentalmente criar 2 saidas
    wall= []
    for i in range(0, tamanho+2):
        wall.append([1, False])
    mapa_gerado.append(wall)
    saida= randint(1,tamanho)
    mapa_gerado[0][saida][0]= 20
    mapa_gerado[1][saida][0]= 19
    #Colocando jogador no inicio do mapa
    yPosition= len(mapa_gerado)- 2
    starting_spawn= randint(1,tamanho-1)
    i= 0
    while mapa_gerado[-2][starting_spawn][0] != 0:
        starting_spawn= randint(1, tamanho-1)
        i+= 1
        if i >1000:
            i= 0
            break
    xPosition= starting_spawn
    #Verificando se o jogador não está preso
    if mapa_gerado[yPosition][xPosition][0] != 0:
        mapa_gerado[yPosition][xPosition][0]= 0
    if mapa_gerado[yPosition-1][xPosition][0] != 0:
        if mapa_gerado[yPosition][xPosition-1][0]!= 0:
            if (mapa_gerado[yPosition][xPosition+1][0] != 0) and (mapa_gerado[yPosition][xPosition+1][0] != 1):
                mapa_gerado[yPosition][xPosition+1][0]= 0
            elif mapa_gerado[yPosition][xPosition+1][0] == 1:
                mapa_gerado[yPosition][xPosition-1][0]= 0

#MAPA : (LEANDO)
#MENU INICIAL : (FERNANDA)
def inicio():
    r = 0
    print('------------------\n SEJA BEM VINDO!  \nESCOLHA UMA OPÇÃO:\n------------------ ')
    print('[1] INICIAR O JOGO \n[2] SAIR')
    r = int(input(''))
    while r != 1 and r != 2: 
        print('ESCOLHA UMA OPÇÃO VÁLIDA: ')
        r = int(input(''))
    if r == 1:
        return 1
    if r == 2: 
        return 2

def ApresentacaoPersonagem():
    c = 0
    while c == 0:
        print('Escolha a classe que deseja saber mais: \n')
        print('[1] BÁRBARO \n[2] GUERREIRO \n[3] MAGO')
        r = int(input(''))
        if r == 1: 
            print('BÁRBARO: São guerreiros de origem selvagem.\nEles não tem refinamento algum em seu jeito de lutar, dando espaço ao uso de força bruta.\nPresumivelmente, também não são muito inteligentes.')
            print('Deseja confirmar BÁRBARO como sua escolha? ')
            print('[1] SIM [0] NÃO')
            c = int(input(''))
            if c == 1:
                return 1
        if r == 2:
            print('GUERREIRO: Guerreiros são exímios lutadores marciais, sempre prontos para o combate. Possuem extremas habilidades de combate.')
            print('Deseja confirmar GUERREIRO como sua escolha? ')
            print('[2] SIM [0] NÃO')
            c = int(input(''))
            if c == 2:
                return 2
        if r == 3:
            print('MAGO: Se distingue pela capacidade de lançar certos tipos de magia, possuindo alta inteligência mas sendo fraco em combate.')
            print('Deseja confirmar MAGO como sua escolha? ')
            print('[3] SIM [0] NÃO')
            c = int(input(''))
            if c == 3:
                return 3
            
def EscolhaPersonagem():
    Classe, Forc, Inte, Agl = None, None, None, None
    ataque1, ataque2, ataque3, ataque4, ataque5, armadura = None, None, None, None, None, None
    d_ataque1, d_ataque2, d_ataque3, d_ataque4, d_ataque5, Ca = None, None, None, None, None, None
    item1, item2, item3, item4, item5, xp = None, None, None, None, None, 20
    r = ApresentacaoPersonagem()
    if r == 1:
        Classe = 'Barbaro'
        print('Você escolheu bárbaro. Você possui: ')
        vidaMax, vidaAtual, Forc, Inte, Agl, d_ataque1, Ca = 18, 18, 5, 1, 4, 5, 9
        item1, armadura = 'Machado', 'Gibão de Pele'
        print(f'{Forc} DE FORÇA | {Inte} DE INTELIGÊNCIA | {Agl} DE AGILIDADE ')
        print('VOCÊ GANHOU SUA PRIMEIRA ARMA: MACHADO')
        atributos = [Classe, vidaMax, vidaAtual, Forc, Inte, Agl]
        ataques = [ataque1, ataque2, ataque3, ataque4, ataque5, armadura]
        dano_ataques = [d_ataque1, d_ataque2, d_ataque3, d_ataque4, d_ataque5, Ca]
        itens = [item1, item2, item3, item4, item5, xp]
        MaPerso = [atributos, ataques, dano_ataques, itens]
        return MaPerso
    
    if r == 2:
        Classe = 'Guerreiro'
        print('Você escolheu guerreiro. Você possui: ')
        vidaMax, vidaAtual, Forc, Inte, Agl, d_ataque1, Ca = 18, 18, 4, 3, 3, 4, 10
        item1, armadura = 'Espada', 'Cota de Malha'
        print(f'{Forc} DE FORÇA | {Inte} DE INTELIGÊNCIA | {Agl} DE AGILIDADE ')
        print('VOCÊ GANHOU SUA PRIMEIRA ARMA: ESPADA')
        atributos = [Classe, vidaMax, vidaAtual, Forc, Inte, Agl]
        ataques = [ataque1, ataque2, ataque3, ataque4, ataque5, armadura]
        dano_ataques = [d_ataque1, d_ataque2, d_ataque3, d_ataque4, d_ataque5, Ca]
        itens = [item1, item2, item3, item4, item5, xp]
        MaPerso = [atributos, ataques, dano_ataques, itens]
        return MaPerso

    if r == 3:
        Classe = 'Mago'
        print('Você escolheu mago. Você possui: ')
        vidaMax, vidaAtual, Forc, Inte, Agl, d_ataque1, Ca= 15, 15, 2, 4, 2, 2, 8
        item1, armadura = 'Cajado', 'Manto do Mago'
        print(f'{Forc} DE FORÇA | {Inte} DE INTELIGÊNCIA | {Agl} DE AGILIDADE ')
        print('VOCÊ GANHOU SUA PRIMEIRA ARMA: CAJADO')
        atributos = [Classe, vidaMax, vidaAtual, Forc, Inte, Agl]
        ataques = [ataque1, ataque2, ataque3, ataque4, ataque5, armadura]
        dano_ataques = [d_ataque1, d_ataque2, d_ataque3, d_ataque4, d_ataque5, Ca]
        itens = [item1, item2, item3, item4, item5, xp]
        MaPerso = [atributos, ataques, dano_ataques, itens]
        return MaPerso
    
def MenuDeAcoes(config,inimigo):
    #Montar o menu de ações (que vai ser exibido sempre)
    #mover, atacar, fugir, abrir, descansar e listar inventário.
    print('Escolha o que deseja fazer: [1] MOVER | [2] ATACAR | [3] ABRIR | [4] DESCANSAR | [5] INVENTÁRIO')
    r = int(input(' '))
    if r == 1:
        print('[1] ESQUERDA | [2] DIREITA | [3] FRENTE | [4] ATRÁS')
        m = int(input(' '))
        if m == 1: 
            print('Movendo-se para a esquerda...')
        if m == 2: 
            print('Movendo-se para a direita...')
        if m == 3: 
            print('Movendo-se para a frente...')
        if m == 4: 
            print('Movendo-se para atrás...')
    if r == 2:
        menuCombate(config,inimigo)
        #funcao do atos de atacar
    if r == 3: 
        if config[3][1] == 'chave baú':
            print('Vocë abriu o baú!')
        else: 
            print('Você não tem a chave para acessar o baú.')
    if r == 4:
        print('Você escolheu descansar.')
        dif = config[0][1] - config[0][2]
        config[0][2] = config[0][2] + dif
        print(f'Sua vida aumentou {dif} unidades, sua vida atual é de {config[0][1]}.')
    if r == 5: 
        print(f"|Vida : {config[0][1]}/{config[0][2]} |For: {config[0][3]} | Int: {config[0][4]} |Agl: {config[0][5]} | Xp: {config[3][5]} |")
        print("E olhando na mochila se percebe que... ")
        print("Você possui: ")
        i = 0
        while i < 5:
            if config[1][i] != 0:
                print(f"° um(a) {config[1][i]}. Dano - > {config[2][i]}")
                i+=1
            else:
                i+=1
        print(f"Verificando a armadura que carrega você vê um(a) {config[1][5]}, que te faz ter {config[2][5]} de CA")
#MENU INICIAL : (FERNANDA)
#COMBATE : (ATOS)
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
                menuCombate(config,inimigo)

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
def menuCombate(config,inimigo):
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
        menuCombate(config,inimigo)
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
#COMBATE : (ATOS)

##################
#Início do programa principal


r = inicio()
if r == 1:
    config = EscolhaPersonagem()   
    print(config[0])
    print(config[1])
    print(config[2])
    print(config[3])
    while True: 
        MenuDeAcoes(config,None)
if r == 2:
    print('Que pena! Espero que volte logo!')


'''
Movimentação é liberada
'''
iniciandoMapa(14)

movimento()
