from random import randint
from random import choice
from colorama import Fore
from colorama import Style
from time import sleep
import sys
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
9- Chave
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
def geradorInimigo(spawn_zone, dificuldade= 10):
    randomy= randint(0, len(spawn_zone)-1)
    randomx= randint(0, len(spawn_zone)-1)
    if spawn_zone[randomy][randomx][0] != 0:
        geradorInimigo(spawn_zone, dificuldade)
    else:
        try:
            spawn_zone[randomy][randomx][0]= dificuldade
        except IndexError:
            geradorInimigo(spawn_zone, dificuldade)
def geradorChave(spawn_zone):
    randomy= randint(0, len(spawn_zone)-1)
    randomx= randint(0, len(spawn_zone)-1)
    if spawn_zone[randomy][randomx][0] != 0:
        geradorChave(spawn_zone)
    else:
        try:
            spawn_zone[randomy][randomx][0]= 9
        except IndexError:
            geradorChave(spawn_zone)
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
def checkNearVisible(xpos : int, ypos : int):
    for y, x in ((1,0),(-1,0),(0,1),(0,-1)):
        if mapa_gerado[ypos+y][xpos+x][0] != 10 and mapa_gerado[ypos+y][xpos+x][0] != 11 and mapa_gerado[ypos+y][xpos+x][0] != 12 and mapa_gerado[ypos+y][xpos+x][0] != 13 and mapa_gerado[ypos+y][xpos+x][0] != 8:
            mapa_gerado[ypos+y][xpos+x][1]= True
#Verifica se o jogador pode ir em uma direção
#Marca território percorrido
def verificandoEspaço(direction):
    global xPosition
    global yPosition
    if direction % 2==0:
        zone_move= mapa_gerado[yPosition+ int(direction/2)][xPosition][0]
        if (zone_move == 0) or (zone_move == 3) or (zone_move == 19):
            yPosition += int(direction/2)
            return [zone_move, yPosition, xPosition]
        else:
            mapa_gerado[yPosition+ int(direction/2)][xPosition][1]= True
            return [zone_move, yPosition+ int(direction/2), xPosition]
    else:
        zone_move= mapa_gerado[yPosition][xPosition+ direction][0]
        if (zone_move == 0) or (zone_move == 3) or (zone_move == 19):
            xPosition += direction
            return [zone_move, yPosition, xPosition]
        else:
            mapa_gerado[yPosition][xPosition+ direction][1]= True
            return [zone_move, yPosition, xPosition+direction]
#Oferecendo uma versão legível do mapa
def transformadorUI(mapa : list, ypos: int, xpos: int):
    count1=0
    count2=0
    for lines in mapa:
        visualizacaoS= ''
        visualizacaoI= ''
        count2= 0
        for colunas in lines:
                #Verificando posição do jogador e colocando P de jogador na visualização
            if (count1== ypos) and (count2== xpos):
                count2+=1
                visualizacaoS+= '   '
                visualizacaoI+= 'P  '
                continue
            if colunas[1] == True:
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
                        visualizacaoI+= f'{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}§  {Style.RESET_ALL}'
                    case 7:
                        visualizacaoS+= f'{Fore.YELLOW}$  {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.YELLOW}B  {Style.RESET_ALL}'
                    case 8:
                        visualizacaoS+= f'{Fore.LIGHTRED_EX}_  {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.LIGHTRED_EX}X  {Style.RESET_ALL}'
                    case 9:
                        visualizacaoS+= f'{Fore.LIGHTWHITE_EX}{Style.BRIGHT}   {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.LIGHTWHITE_EX}{Style.BRIGHT}f  {Style.RESET_ALL}'
                    case 19:
                        visualizacaoS+= f'{Fore.WHITE}^  {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.WHITE}|  {Style.RESET_ALL}'
                    case 20:
                        visualizacaoS+= '   '
                        visualizacaoI+= '   '
                    case 10 | 11 | 12 | 13:
                        visualizacaoS+= f' {Fore.RED}O {Style.RESET_ALL}'
                        visualizacaoI+= f'{Fore.RED}| |{Style.RESET_ALL}'

            else:
                visualizacaoS+= '   '
                visualizacaoI+= '   '
            count2+=1
        count1+=1
        print(visualizacaoS)
        print(visualizacaoI)
#Verifica se é possível completar o nível ou não
def checkFinal(initial_y: int, initial_x: int, orientacao: list):
    pawnY= initial_y
    pawnX= initial_x
    guia_orientacao= ((-1,0), (0,1), (1,0), (0,-1))
    fowardBlock= mapa_gerado[pawnY+ orientacao[0]][pawnX+ orientacao[1]][0]
    rightBlock= mapa_gerado[pawnY+ orientacao[1]][pawnX+ (orientacao[0]*-1)][0]
    if fowardBlock == 19:
        return True
    if rightBlock != 1 and rightBlock != 2 and rightBlock != 4 and rightBlock != 5 and rightBlock != 7:
        i= 0
        while i < 4:
            if orientacao == guia_orientacao[i]:
                if orientacao == guia_orientacao[-1]:
                    orientacao= guia_orientacao[0]
                else:
                    orientacao= guia_orientacao[i+1]
                break
            i+= 1
        pawnY+= orientacao[0]
        pawnX+= orientacao[1]

    else:
        i= 0
        while i < 4:
            if orientacao == guia_orientacao[i]:
                if orientacao == guia_orientacao[0]:
                    orientacao= guia_orientacao[-1]
                else:
                    orientacao= guia_orientacao[i-1]
                break
            i+= 1
    try:
        return checkFinal(pawnY, pawnX, orientacao)
    except RecursionError: #Quando o peão passa de 1000 movimentos o programa determina o mapa como impossível
        return False
    
def movimento(config):
        global sala
        while True:
            mapa_gerado[yPosition][xPosition][1]= True
            checkNearVisible(xPosition, yPosition)
            comando= str(input('Escolha uma direção para ir: '))
            comando= comando.lower()
            global evento
            if comando == 'w':
                evento= verificandoEspaço(-2)
                break
            elif comando == 's':
                evento= verificandoEspaço(2)
                break
            elif comando == 'd':
                evento= verificandoEspaço(1)
                break
            elif comando == 'a':
                evento= verificandoEspaço(-1)
                break
            else:
                print('Direção inválida')
        checkNearVisible(xPosition, yPosition)
        mapa_gerado[yPosition][xPosition][1]= True
        transformadorUI(mapa_gerado, yPosition, xPosition)
        if 10 <= evento[0] <= 13:
            monstro_atual= criarFichaMonstro(evento[0])
            combate(config, monstro_atual, "j")
            vasculharRestos(config, monstro_atual)
        elif evento[0] == 6:
            i= 0
            for item in config[3]:
                if item == None:
                    mapa_gerado[evento[1]][evento[2]][0]= 0
                    config[3][i]= vetor_items[randint(1,8)]
                    print(f'Você ganhou um(a) {config[3][i]}')
                    break
                i+= 1
        elif evento[0] == 9:
            i= 0
            for item in config[3]:
                if item == None:
                    mapa_gerado[evento[1]][evento[2]][0]= 0
                    config[3][i]= 'Chave'
                    print(f'Você ganhou uma Chave')
                    break
                i+= 1
        elif evento[0] == 20:
            print('\nVocê segue o mapa e de repente o caminho atrás de você se fecha.\nVocê se depara com mais território não explorado.')
            vetor_efeitos[6]= 0
            sala+= 1
            iniciandoMapa(tamanho_inicial_mapa)
        elif evento[0] == 19:
            print('Acima de você há uma passagem!')
        elif evento[0] == 8:
            print('Você é surpreendido por uma armadilha!')
            dano= randint(5, int(config[0][2]/2))
            config[0][2]-= dano
            print(f'A armadilha deu {dano} de dano em você')
            mapa_gerado[evento[1]][evento[2]][0]= 0
        elif evento[0] == 3:
            if vetor_efeitos[6] != 2:
                if randint(1,5) == 2:
                    vetor_efeitos[6]+= 1
                    monstro_atual= criarFichaMonstro(randint(12,13), True)
                    print('Algo surge das profundezas!')
                    sleep(0.5)
                    combate(config, monstro_atual, "j")
                    vasculharRestos(config, monstro_atual)
def iniciandoMapa(n):
    tamanho= n
    global mapa_gerado
    mapa_gerado= inicializa(tamanho)
    wall= []
    
    #Gerando o mapa
    i= 0
    escalar= 0
    if sala > 3:
        escalar+= sala
    while i < 6+escalar:
        geradorInimigo(mapa_gerado, 10+randint(0,sala))
        i+= 1
    i=0
    while i < randint(6,10):
        geradorAmbiente(mapa_gerado, 4, 3)
        i+=1
    i= 0
    while i < randint(1,2):
        geradorEstrutura(mapa_gerado, randint(3,4), randint(3,4))
        i+= 1
    terAgua= choice((1,2,3,4,5))
    aguaRand= randint(2, tamanho-3)
    if (terAgua == 1) or (terAgua == 2):
        geradorLago(mapa_gerado, randint(3,4))
    elif terAgua == 3:
        geradorRio(mapa_gerado[aguaRand: aguaRand+2])
    elif terAgua == 4:
        geradorRio(mapa_gerado[aguaRand: aguaRand+2])
        geradorLago(mapa_gerado, 3)
    else:
        geradorRio(mapa_gerado[aguaRand: aguaRand+2])
        geradorRio(mapa_gerado[aguaRand: aguaRand+2])
    i= 0
    while i < randint(3, 6):
        geradorBau(mapa_gerado)
        i+= 1
    i= 0
    while i < randint(3, 5):
        geradorChave(mapa_gerado)
        i+= 1
    i= 0 
    while i < randint(1,3):
        geradorArmadilha(mapa_gerado)
        i+= 1
    #Adicionando bordas
    for linha in mapa_gerado:
        linha.insert(0, [1, True])
        linha.append([1, True])

    for i in range(0, tamanho+2):
        wall.append([1, False])
    mapa_gerado.insert(0, wall)
    #Reset para evitar criar 2 vetores com mesmo endereço de memória e acidentalmente criar 2 saidas
    wall= []
    for i in range(0, tamanho+2):
        wall.append([1, True])
    mapa_gerado.append(wall)
    saida= randint(1,tamanho)
    mapa_gerado[0][saida][0]= 20
    mapa_gerado[1][saida][0]= 19
    #Colocando jogador no inicio do mapa
    global yPosition
    yPosition= len(mapa_gerado)- 2
    starting_spawn= randint(1,tamanho-1)
    i= 0
    while mapa_gerado[-2][starting_spawn][0] != 0:
        starting_spawn= randint(1, tamanho-1)
        i+= 1
        if i >1000:
            i= 0
            break
    global xPosition
    xPosition= starting_spawn
    if checkFinal(len(mapa_gerado)-2, starting_spawn, (-1, 0)) == False:
        iniciandoMapa(n)
#MAPA : (LEANDRO)
#MENU INICIAL : (FERNANDA)
def inicio():
    r = 0
    print('------------------\n SEJA BEM VINDO!  \nESCOLHA UMA OPÇÃO:\n------------------ ')
    print('[1] INICIAR O JOGO \n[2] SAIR')
    try:
        r = int(input(''))
        while r != 1 and r != 2: 
            print('ESCOLHA UMA OPÇÃO VÁLIDA: ')
            r = int(input(''))
    except ValueError:
        inicio()
    if r == 1:
        return 1
    if r == 2: 
        return 2

def ApresentacaoPersonagem():
    c = 0
    while c == 0:
        print('Escolha a classe que deseja saber mais: \n')
        print('[1] BÁRBARO \n[2] GUERREIRO \n[3] MAGO')
        try:
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
        except ValueError:
            ApresentacaoPersonagem()    
def EscolhaPersonagem():
    Classe, Forc, Inte, Agl = None, None, None, None
    ataque1, ataque2, ataque3, ataque4, ataque5, armadura = None, None, None, None, None, None
    d_ataque1, d_ataque2, d_ataque3, d_ataque4, d_ataque5, Ca = None, None, None, None, None, None
    item1, item2, item3, item4, item5, xp = 'Chave', None, None, None, None, 20
    r = ApresentacaoPersonagem()
    global level
    level = 0
    if r == 1:
        Classe = 'Barbaro'
        print('Você escolheu bárbaro. Você possui: ')
        vidaMax, vidaAtual, Forc, Inte, Agl, d_ataque1, Ca = 18, 18, 5, 1, 4, 5, 9
        ataque1, armadura  = 'Machado', 'Gibão de Pele' 
        print(f'{Forc} DE FORÇA | {Inte} DE INTELIGÊNCIA | {Agl} DE AGILIDADE ')
        print('VOCÊ GANHOU SUA PRIMEIRA ARMA: MACHADO')
        print('VOCÊ COMEÇA COM UMA CHAVE')
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
        ataque1, armadura = 'Espada', 'Cota de Malha'
        print(f'{Forc} DE FORÇA | {Inte} DE INTELIGÊNCIA | {Agl} DE AGILIDADE ')
        print('VOCÊ GANHOU SUA PRIMEIRA ARMA: ESPADA')
        print('VOCÊ COMEÇA COM UMA CHAVE')
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
        ataque1, armadura = 'Cajado', 'Manto do Mago'
        print(f'{Forc} DE FORÇA | {Inte} DE INTELIGÊNCIA | {Agl} DE AGILIDADE ')
        print('VOCÊ GANHOU SUA PRIMEIRA ARMA: CAJADO')
        print('VOCÊ COMEÇA COM UMA CHAVE')
        atributos = [Classe, vidaMax, vidaAtual, Forc, Inte, Agl]
        ataques = [ataque1, ataque2, ataque3, ataque4, ataque5, armadura]
        dano_ataques = [d_ataque1, d_ataque2, d_ataque3, d_ataque4, d_ataque5, Ca]
        itens = [item1, item2, item3, item4, item5, xp]
        MaPerso = [atributos, ataques, dano_ataques, itens]
        return MaPerso
    
def MenuDeAcoes(config):
    #Montar o menu de ações (que vai ser exibido sempre)
    #mover, atacar, fugir, abrir, descansar e listar inventário. #
    print('Escolha o que deseja fazer: [1] MOVER | [2] USAR ITEM | [3] DESCANSAR | [4] INVENTÁRIO')
    #Permite que o jogador continue a jogar caso ele digite uma letra e ocorra ValueError
    while True:
        try:
            r = int(input(' '))
            break
        except ValueError:
            pass
    if r == 1:
        if movimento(config) == False:
            return False
    if r == 2:
        tem_item= False
        conta= 0
        for item in config[3][:5]:
            if item != None:
                print(f'{conta} -> {config[3][conta]}')
                conta+= 1
                tem_item= True 
            else:
                conta+=1
        if tem_item == False:
            print('Você não tem nenhum item na mochila!')
        #Player usará item em uma posição do mapa
        while tem_item == True:
            try:
                comando= int(input('Escolha um item para usar: '))
                item_usar= config[3][comando]
                guard= comando
                if (item_usar == None) or (comando == 5):
                    continue
            except ValueError or IndexError:
                continue
            comando= str(input('Escolha uma direção para usar o item: '))
            comando= comando.lower()
            if comando == 'w':
                evento= verificandoEspaço(-2)
            elif comando == 's':
                evento= verificandoEspaço(2)
            elif comando == 'd':
                evento= verificandoEspaço(1)
            elif comando == 'a':
                evento= verificandoEspaço(-1)
            else:
                print('Direção inválida')
                continue
            itemsMapa(item_usar, evento[1:], comando)
            if evento[0] == 8:
                print('Uma armadilha foi ativada com o seu item')
                mapa_gerado[evento[1]][evento[2]][0]= 0
            sleep(2)
            transformadorUI(mapa_gerado, yPosition, xPosition)
            print(f'Você usou {item_usar}')
            config[3][guard]= None
            break
         

    if r == 3:
        i = 0
        fim = len(config[3])
        p = ''
        while fim >= 0:
            while i <= (fim - 1):
                p = config[3][i]
                if p == 'Poção':
                    print('Você escolheu descansar.')
                    dif = config[0][1] - config[0][2]
                    config[0][2] = config[0][2] + dif
                    print(f'Sua vida aumentou {dif} unidades, sua vida atual é de {config[0][1]}.')
                    config[3][i]= None
                    break
                elif i == (fim -1):
                    print('Você não tem a poção necessária para descansar.')
                i += 1
            if p == 'Poção':
                break
            fim -= 1
        
    if r == 4: 
        verInventario(config)
#MENU INICIAL : (FERNANDA)
#COMBATE : (ATOS)
#TURNOS
def combate(config, inimigo, turno):
    #O JOGADOR ESTÁ VIVO?
    if config[0][2] > 0:
        #O INIMIGO MORREU ?
        if inimigo[1] <= 0:
            print(f" O {inimigo[0]} foi derrotado. Parabéns !")
            print(f" Você receber {inimigo[7]} de xp, e agora seu xp é {config[3][5]}")
            config[3][5] += inimigo[7]  
            uparDeLevel(config)
            mapa_gerado[evento[1]][evento[2]][0]= 0
            vetor_efeitos[0]= 0
            vetor_efeitos[1]= 0
            vetor_efeitos[2]= 0 
            vetor_efeitos[3]= 0
            vetor_efeitos[4]= 0
            vetor_efeitos[5]= 0

        #SE NÃO, ROLE O TURNO
        else:
            if turno == "j":
                print(f"Um {inimigo[0]} está a sua frente!")
                menuCombate(config,inimigo)

            elif turno == 'i':
                if (inimigo[1] >= 0) and (vetor_efeitos[2] == 0):
                    print(f"O turno é do {inimigo[0]}")
                    ataqueInimigo(inimigo,config)

                elif vetor_efeitos[2] == 1:
                    print(f'O inimigo {inimigo[0]} está paralizado nesse turno')
                    vetor_efeitos[2]= 0
                    combate(config, inimigo, "j")
                #SE O JOGADOR TIVER VIDA, PASSE O COMBATE DE VOLTA PARA ELE
                else: 
                    return config
                
    #SE NÃO, ENCERRE O COMBATE
    else:
        print("VOCÊ MORREU (╥﹏╥) ")
        print(f'Florestas percorridas: {sala}')
        print(f'Pontuação total: {config[3][5]}')
        sys.exit()
def uparDeLevel(config):
    global level
    if config[0][0] == 'Barbaro' and level == 1:
        if config[3][5] >= 100:
            config[0][1] += 15
            config[0][2] += 15
            config[0][3] += 2
            config[0][5] += 1
            print(f"Você upou de level!, agora seu level é {level}")
            level +=1
        
    elif config[0][0] == 'Barbaro' and level == 2:
        if config[3][5] >= 400:
            config[0][1] += 30
            config[0][2] += 30
            config[0][3] += 2
            print(f"Você upou de level!, agora seu level é {level}")
            level +=1
    elif config[0][0] == 'Barbaro' and level == 3:
        if config[3][5] >= 900:
            config[0][1] += 60
            config[0][2] += 60
            config[0][3] += 3
            config[0][5] += 1
            print(f"Você upou de level!, agora seu level é {level}")
            level +=1

    if config[0][0] == 'Mago' and level == 1:
        if config[3][5] >= 100:
            config[0][1] += 8
            config[0][2] += 8
            config[0][4] += 3
            config[0][5] += 1
            print(f"Você upou de level!, agora seu level é {level}")
            level +=1
        
    elif config[0][0] == 'Mago' and level == 2:
        if config[3][5] >= 400:
            config[0][1] += 15
            config[0][2] += 15
            config[0][4] += 3
            print(f"Você upou de level!, agora seu level é {level}")
            level +=1
    elif config[0][0] == 'Mago' and level == 3:
        if config[3][5] >= 900:
            config[0][1] += 30
            config[0][2] += 30
            config[0][4] += 4
            config[0][5] += 1
            print(f"Você upou de level!, agora seu level é {level}")
            level +=1
    if config[0][0] == 'Guerreiro' and level == 1:
        if config[3][5] >= 100:
            config[0][1] += 15
            config[0][2] += 15
            config[0][3] += 2
            config[0][5] += 2
            print(f"Você upou de level!, agora seu level é {level}")
            level +=1
        
    elif config[0][0] == 'Guerreiro' and level == 2:
        if config[3][5] >= 400:
            config[0][1] += 30
            config[0][2] += 30
            config[0][3] += 1
            config[0][5] += 1
            print(f"Você upou de level!, agora seu level é {level}")
            level +=1
    elif config[0][0] == 'Guerreiro' and level == 3:
        if config[3][5] >= 900:
            config[0][1] += 60
            config[0][2] += 60
            config[0][3] += 2
            config[0][5] += 2
            print(f"Você upou de level!, agora seu level é {level}")
            level +=1

#MENU JOGADOR
def menuCombate(config,inimigo):
    print("------------------------É seu turno! O que deseja fazer ?------------------------")
    print("| :ATACAR     |\n| :INVENTARIO |\n| :ITEM       |\n| :FUGIR      |")
    n = ''
    while n != "ATACAR" and n != "INVENTARIO" and n != "FUGIR" and n != "ITEM":
        n = input("| Digite sua escolha:  ")
        n= n.upper()

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
        while (0 > j) or (j > 5):
            try:
                j = int(input("Escolha um item a ser usado:  "))
            except ValueError:
                pass
        return ataqueJogador(config, j , inimigo)

    elif n == "INVENTARIO":
        #MOSTRANDO O INVENTARIO
        verInventario(config)
        #CHAMANDO NOVAMENTE O MENU DE AÇÕES
        menuCombate(config,inimigo)
    elif n == "ITEM":
        conta= 0
        #Procurando por todos os items do jogador (tirando o xp q ta no final)
        tem_items= False
        for item in config[3][:5]:
            if item != None:
                print(f'{conta} -> {item}')
                conta+= 1
                tem_items= True
            else:
                conta+= 1
        if tem_items == False:
            print('Você não tem items para usar no momento!')
            menuCombate(config,inimigo)
            sleep(1)
        j= -1
        while (0 > j) or (j > 5):
            try:
                j= int(input('Digite um item para ser usado: '))
            except ValueError:
                pass
            if config[3][j] == None:
                continue
            break  
        itemsCombate(config[3][j])
        config[3][j]= None
        menuCombate(config, inimigo)
    else:
        print("Tentando fugir...")
        sleep(0.7)
        chanceDeEscapar = config[0][5] + randint(1,20) - vetor_efeitos[1]
        if chanceDeEscapar < 10:
            vetor_efeitos[1]= 0
            print("Você correu!!")
            #ENCERRANDO O COMBATE
            return config
        else:
            print("O inimigo não te deixa partir, e agora é o turno dele!!")
            sleep(0.5)
            #PASSANDO O TURNO DE VOLTA PARA O INIMIGO
            return combate(config,inimigo,"i")

#GERADORES
def criarFichaMonstro(dificuldade, aquatico= False):
    inimigoConfig = []
    if aquatico == False:
        inimigo = randint(1,10)
    elif dificuldade == 12:
        inimigo= 2
    else:
        inimigo= choice((1,2,9))
    #FACIL
    if dificuldade == 10 or dificuldade == 11:    
        if inimigo == 1:
            inimigoConfig.append("Javas")
            inimigoConfig.append(12)
            inimigoConfig.append(5)
            inimigoConfig.append(None)
            inimigoConfig.append("Presas de Encomenda")
            inimigoConfig.append(5)
            inimigoConfig.append(1)
            inimigoConfig.append(10)
        elif inimigo == 2:
            inimigoConfig.append("Esquilo Acafeinado")
            inimigoConfig.append(2)
            inimigoConfig.append(6)
            inimigoConfig.append(None)
            inimigoConfig.append("Enxurrada de Nozes")
            inimigoConfig.append(2)
            inimigoConfig.append(5)
            inimigoConfig.append(10)
        elif inimigo == 3:
            inimigoConfig.append("Guaxinim")
            inimigoConfig.append(10)
            inimigoConfig.append(10)
            inimigoConfig.append("Manto Do Bandido")
            inimigoConfig.append("3Oitao")
            inimigoConfig.append(6)
            inimigoConfig.append(1)
            inimigoConfig.append(10)
        elif inimigo == 4:
            inimigoConfig.append("Lobo Pedinte")
            inimigoConfig.append(14)
            inimigoConfig.append(8)
            inimigoConfig.append("Proteção Carente")
            inimigoConfig.append("Me jogue aos lobos e eu voltarei, ai ai me morederam")
            inimigoConfig.append(5)
            inimigoConfig.append(3)
            inimigoConfig.append(12)
        elif inimigo == 5:
            inimigoConfig.append("Algum Bando Goblin")
            inimigoConfig.append(12)
            inimigoConfig.append(8)
            inimigoConfig.append("Roupas velhas")
            inimigoConfig.append("Saraivada de Coisas Nojentas")
            inimigoConfig.append(4)
            inimigoConfig.append(4)
            inimigoConfig.append(12)
        elif inimigo == 6:
            inimigoConfig.append("Jabuti")
            inimigoConfig.append(1)
            inimigoConfig.append(19)
            inimigoConfig.append("Casco de Jabuti")
            inimigoConfig.append("Bonk")
            inimigoConfig.append(1)
            inimigoConfig.append(1)
            inimigoConfig.append(20)
        elif inimigo == 7:
            inimigoConfig.append("Preguiça")
            inimigoConfig.append(20)
            inimigoConfig.append(4)
            inimigoConfig.append("Roupas Estilosas")
            inimigoConfig.append("Agarrão")
            inimigoConfig.append(6)
            inimigoConfig.append(3)
            inimigoConfig.append(15)
        elif inimigo == 8:
            inimigoConfig.append("Velha")
            inimigoConfig.append(8)
            inimigoConfig.append(5)
            inimigoConfig.append("Pantufas quentinhas")
            inimigoConfig.append("Bola de fogo")
            inimigoConfig.append(8)
            inimigoConfig.append(1)
            inimigoConfig.append(20)
        elif inimigo == 9:
            inimigoConfig.append("Flavio")
            inimigoConfig.append(1)
            inimigoConfig.append(1)
            inimigoConfig.append(None)
            inimigoConfig.append("Aula Assincrona")
            inimigoConfig.append(1)
            inimigoConfig.append(1)
            inimigoConfig.append(1)
        elif inimigo == 10:
            inimigoConfig.append("Mosquito")
            inimigoConfig.append(1)
            inimigoConfig.append(20)
            inimigoConfig.append("zzzzzzzzzzzzzzz")
            inimigoConfig.append("Picada")
            inimigoConfig.append(1)
            inimigoConfig.append(-5)
            inimigoConfig.append(20)
    #MEDIO
    elif dificuldade == 12:
        if inimigo == 1:
            cobra = randint(1,10)
            if cobra == 1:
                inimigoConfig.append("Coral Verdadeira")
                inimigoConfig.append(2)
                inimigoConfig.append(16)
                inimigoConfig.append("Pele :Preto - Amarela - Preto - Amarelo - Laranja")
                inimigoConfig.append("Envenenar")
                inimigoConfig.append(8)
                inimigoConfig.append(4)
                inimigoConfig.append(40)
            elif cobra == 2:
                inimigoConfig.append("Jararaca")
                inimigoConfig.append(2)
                inimigoConfig.append(16)
                inimigoConfig.append("Pele :Marrom")
                inimigoConfig.append("Envenenar")
                inimigoConfig.append(8)
                inimigoConfig.append(4)
                inimigoConfig.append(40)
            elif cobra == 3:
                inimigoConfig.append("Jararacuçu")
                inimigoConfig.append(2)
                inimigoConfig.append(16)
                inimigoConfig.append("Pele :Preto - Amarelo")
                inimigoConfig.append("Envenenar")
                inimigoConfig.append(8)
                inimigoConfig.append(4)
                inimigoConfig.append(40)
            elif cobra == 4:
                inimigoConfig.append("Urutu")
                inimigoConfig.append(2)
                inimigoConfig.append(16)
                inimigoConfig.append("Pele :Marrom - Preto")
                inimigoConfig.append("Envenenar")
                inimigoConfig.append(8)
                inimigoConfig.append(4)
                inimigoConfig.append(40)
            elif cobra == 5:
                inimigoConfig.append("Cascavel")
                inimigoConfig.append(2)
                inimigoConfig.append(16)
                inimigoConfig.append("Pele :Marrom")
                inimigoConfig.append("Envenenar")
                inimigoConfig.append(8)
                inimigoConfig.append(4)
                inimigoConfig.append(40)
            elif cobra == 6:
                inimigoConfig.append("Surucucu")
                inimigoConfig.append(2)
                inimigoConfig.append(16)
                inimigoConfig.append("Pele :Dourada")
                inimigoConfig.append("Envenenar")
                inimigoConfig.append(8)
                inimigoConfig.append(4)
                inimigoConfig.append(40)
            elif cobra == 7:
                inimigoConfig.append("Cobra Papagaio")
                inimigoConfig.append(2)
                inimigoConfig.append(16)
                inimigoConfig.append("Pele :Verde")
                inimigoConfig.append("Mordida")
                inimigoConfig.append(8)
                inimigoConfig.append(4)
                inimigoConfig.append(40)
            elif cobra == 8:
                inimigoConfig.append("Falsa Coral")
                inimigoConfig.append(2)
                inimigoConfig.append(16)
                inimigoConfig.append("Pele :Cinza - Preto - Vermelho")
                inimigoConfig.append("Mordida")
                inimigoConfig.append(8)
                inimigoConfig.append(4)
                inimigoConfig.append(40)
            elif cobra == 9:
                inimigoConfig.append("Jiboia")
                inimigoConfig.append(2)
                inimigoConfig.append(16)
                inimigoConfig.append("Pele :Marrom")
                inimigoConfig.append("Mordida")
                inimigoConfig.append(8)
                inimigoConfig.append(4)
                inimigoConfig.append(40)
            elif cobra == 10:
                inimigoConfig.append("Muçurana")
                inimigoConfig.append(2)
                inimigoConfig.append(16)
                inimigoConfig.append("Pele :Preta")
                inimigoConfig.append("Mordida")
                inimigoConfig.append(8)
                inimigoConfig.append(4)
                inimigoConfig.append(40)
        elif inimigo == 2:
            inimigoConfig.append("Jacaré")
            inimigoConfig.append(20)
            inimigoConfig.append(14)
            inimigoConfig.append("Pele dura")
            inimigoConfig.append("Vacina")
            inimigoConfig.append(6)
            inimigoConfig.append(4)
            inimigoConfig.append(40)
        elif inimigo == 3:
            inimigoConfig.append("Gavião Real")
            inimigoConfig.append(3)
            inimigoConfig.append(15)
            inimigoConfig.append("Coroa de Penas")
            inimigoConfig.append("Arremessar filhos")
            inimigoConfig.append(8)
            inimigoConfig.append(10)
            inimigoConfig.append(40)
        elif inimigo == 4:
            inimigoConfig.append("Carteira de Trabalho")
            inimigoConfig.append(10)
            inimigoConfig.append(13)
            inimigoConfig.append("Tristeza")
            inimigoConfig.append("Atender caixa")
            inimigoConfig.append(7)
            inimigoConfig.append(4)
            inimigoConfig.append(30)
        elif inimigo == 5:
            inimigoConfig.append("Macaco")
            inimigoConfig.append(15)
            inimigoConfig.append(12)
            inimigoConfig.append("Drip")
            inimigoConfig.append("Monke")
            inimigoConfig.append(6)
            inimigoConfig.append(4)
            inimigoConfig.append(40)
        elif inimigo == 6:
            inimigoConfig.append("Tatu")
            inimigoConfig.append(4)
            inimigoConfig.append(17)
            inimigoConfig.append("Casco de tatu")
            inimigoConfig.append("Dor nas costas")
            inimigoConfig.append(4)
            inimigoConfig.append(4)
            inimigoConfig.append(35)
        elif inimigo == 7:
            inimigoConfig.append("IPVA")
            inimigoConfig.append(20)
            inimigoConfig.append(13)
            inimigoConfig.append("Governo")
            inimigoConfig.append("Cobrar Impostos")
            inimigoConfig.append(6)
            inimigoConfig.append(2)
            inimigoConfig.append(35)
        elif inimigo == 8:
            inimigoConfig.append("Cubo Gelatinoso")
            inimigoConfig.append(40)
            inimigoConfig.append(4)
            inimigoConfig.append("Translucido")
            inimigoConfig.append("Ataque Molenga")
            inimigoConfig.append(2)
            inimigoConfig.append(2)
            inimigoConfig.append(40)
        elif inimigo == 9:
            inimigoConfig.append("Diabrete")
            inimigoConfig.append(15)
            inimigoConfig.append(12)
            inimigoConfig.append("Pele vermelha")
            inimigoConfig.append("Tridente")
            inimigoConfig.append(6)
            inimigoConfig.append(4)
            inimigoConfig.append(40)
        elif inimigo == 10:
            inimigoConfig.append("Onça")
            inimigoConfig.append(35)
            inimigoConfig.append(16)
            inimigoConfig.append("Belza Mortal")
            inimigoConfig.append("Rasgar Gargantas")
            inimigoConfig.append(8)
            inimigoConfig.append(4)
            inimigoConfig.append(120)
    #DIFICIL
    elif dificuldade == 13:
        if inimigo == 1:
            inimigoConfig.append("Sereia")
            inimigoConfig.append(30)
            inimigoConfig.append(16)
            inimigoConfig.append("Corpo de Tilapia")
            inimigoConfig.append("Catada mal feita")
            inimigoConfig.append(10)
            inimigoConfig.append(6)
            inimigoConfig.append(90)
        elif inimigo == 2:
            inimigoConfig.append("Boto")
            inimigoConfig.append(45)
            inimigoConfig.append(14)
            inimigoConfig.append("Cor de Rosa")
            inimigoConfig.append(";)")
            inimigoConfig.append(10)
            inimigoConfig.append(3)
            inimigoConfig.append(90)
        elif inimigo == 3:
            inimigoConfig.append("Varias Góticas")
            inimigoConfig.append(40)
            inimigoConfig.append(13)
            inimigoConfig.append("Roupas Maléficas")
            inimigoConfig.append("Carência Paterna")
            inimigoConfig.append(12)
            inimigoConfig.append(2)
            inimigoConfig.append(90)
        elif inimigo == 4:
            inimigoConfig.append("Grifo Faminto")
            inimigoConfig.append(50)
            inimigoConfig.append(12)
            inimigoConfig.append("Correntes Quebradas")
            inimigoConfig.append("Sequência Furiosa Inabalável Aniquiladora de Garradas Extremamentes Afiadas")
            inimigoConfig.append(10)
            inimigoConfig.append(6)
            inimigoConfig.append(100)
        elif inimigo == 5:
            inimigoConfig.append("Ogro sem olho")
            inimigoConfig.append(60)
            inimigoConfig.append(8)
            inimigoConfig.append("Roupas Sujas")
            inimigoConfig.append("Um Pedação de Árvore")
            inimigoConfig.append(12)
            inimigoConfig.append(5)
            inimigoConfig.append(100)
        elif inimigo == 6:
            inimigoConfig.append("SERASA")
            inimigoConfig.append(55)
            inimigoConfig.append(15)
            inimigoConfig.append("Vish")
            inimigoConfig.append("ROBO NÉ ZÉ?")
            inimigoConfig.append(10)
            inimigoConfig.append(5)
            inimigoConfig.append(100)
        elif inimigo == 7:
            inimigoConfig.append("°°°¹³²³criatura_não_indentificada")
            inimigoConfig.append(80)
            inimigoConfig.append(10)
            inimigoConfig.append("???")
            inimigoConfig.append("Observar em silêncio profundo")
            inimigoConfig.append(12)
            inimigoConfig.append(10)
            inimigoConfig.append(120)
        elif inimigo == 8:
            inimigoConfig.append("Greve")
            inimigoConfig.append(65)
            inimigoConfig.append(14)
            inimigoConfig.append("Professores")
            inimigoConfig.append("Enrolação")
            inimigoConfig.append(10)
            inimigoConfig.append(5)
            inimigoConfig.append(90)
        elif inimigo == 9:
            inimigoConfig.append("Quantidade Exorbitante de Ouriços do Mar")
            inimigoConfig.append(70)
            inimigoConfig.append(8)
            inimigoConfig.append("Cara, perdi a criatividade")
            inimigoConfig.append("Espinhos em lugares onde não deveria ser possivel espetar um espinho")
            inimigoConfig.append(14)
            inimigoConfig.append(6)
            inimigoConfig.append(130)
        elif inimigo == 10:
            inimigoConfig.append("( ͡° ͜ʖ ͡°)")
            inimigoConfig.append(100)
            inimigoConfig.append(20)
            inimigoConfig.append("¯\\_(ツ)_/¯")
            inimigoConfig.append("(ง︡'-'︠)ง")
            inimigoConfig.append(8)
            inimigoConfig.append(10)
            inimigoConfig.append(200)

    return inimigoConfig

#ATAQUES
def ataqueJogador(config,escolha, receptor):
    acerto = (randint(1,20))
    bonus= vetor_efeitos[0]
    sleep(1.2)
    print(f"Você rolou um {acerto}")
    if bonus != 0:
        print(f'Com um bonus de {bonus}')
    sleep(0.5)
#         AGILIDADE     CHANCE     CA-INIMIGO
    if (config[0][4] + acerto+ bonus) >= receptor[2]:
        #ACERTOU
        if config[2][escolha] == None:
            print("Não há itens nesse slot, ataque perdido")
        else:
            #   NÃO É MAGO ?         '''DANO DA ARMA'''  '''FORÇA''' 
            if config[0][0] != 3:
                dano = randint(1, config[2][escolha]) + config[0][2]
                receptor[1] -= (dano)
                if vetor_efeitos[4] == 1:
                    receptor[1]-= 1
                    print(f'As chamas deram 1 de dano no inimigo')
                print(f"Você deu {dano} de dano no {receptor[0]}, e a vida dele agora é {receptor[1]}")
            #É MAGO, ENTÃO USE INTELIGENCIA NO DANO 
            else:
                dano = randint(1, config[2][escolha]) + config[0][3]
                receptor[1] -= (dano)
                print(f"Você deu {dano} de dano no {receptor[0]}, e a vida dele agora é {receptor[1]}")
        sleep(0.5)
        combate(config,receptor, "i")

    else:
        if vetor_efeitos[4] == 1:
            receptor[1]-= 1
            print(f'As chamas deram 1 de dano no inimigo')
        print("O inimigo desviou seu ataque")
        sleep(0.5)
        combate(config,receptor, "i")

def ataqueInimigo(inimigo,config):
    sleep(0.5)
    acerto = randint(1,20) + inimigo[6]- vetor_efeitos[1]
    if (acerto-vetor_efeitos[5]) >= config[2][5]:
        if vetor_efeitos[3] == 1:
            print('O ataque foi bloqueado')
            vetor_efeitos[3]= 0
            combate(config, inimigo, "j")
        else:
            print(f"O {inimigo[0]} acertou, e utilizando um {inimigo[4]} ele te deu {inimigo[5]} de dano!")
            config[0][2] -= inimigo[5]
            sleep(0.5)
            combate(config, inimigo, "j")
        vetor_efeitos[5]= 0
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
            e= e.upper()
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
                        e= e.upper()
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
            e= e.upper()
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
    print(f"|Vida : {config[0][2]}/{config[0][1]} |For: {config[0][3]} | Int: {config[0][4]} |Agl: {config[0][5]} | Xp: {config[3][5]} |")
    print("E olhando na mochila se percebe que... ")
    print("Você possui: ")
    while i < 5:
        if config[1][i] != None:
            print(f"° um(a) {config[1][i]}. Dano - > {config[2][i]}")
            i+=1
        else:
            i+=1
    i= 0
    while i < 4:
        if config[3][i] != None:
            print(f"° um(a) {config[3][i]}")
            i+=1
        else:
            i+=1
    print(f"Verificando a armadura que carrega você vê um(a) {config[1][5]}, que te faz ter {config[2][5]} de CA")
#COMBATE : (ATOS)

def itemsMapa(tipo_item, local, direcao): #Função controla o que cada item (quando usados no mapa) fazem
    posicaoAnalisada= mapa_gerado[local[0]][local[1]]
    
    match tipo_item:
        case 'Chave':
            if posicaoAnalisada[0] == 7:
                posicaoAnalisada[0]= 6
                print('O baú foi aberto')
        case 'Tocha':
            if (posicaoAnalisada[0] == 2) or (posicaoAnalisada[0] == 5):
                mapa_gerado[local[0]][local[1]][0]= 0
                print('Obstáculo virou cinzas')
            elif posicaoAnalisada[0] == 7:
                choice((1,2))
                if choice == 1:
                    print('O baú e o item dentro viraram cinzas')
                    posicaoAnalisada[0]= 0
                else:
                    print('O baú virou cinzas')
                    posicaoAnalisada[0]= 6
            mapa_gerado[local[0]][local[1]][1]= True
        case 'Pedra luminosa':
            Lcontador= 0
            while Lcontador < 6:
                try:
                    if direcao == 'w':
                        mapa_gerado[local[0]-Lcontador][local[1]][1]= True
                    if direcao == 'a':
                        mapa_gerado[local[0]][local[1]-Lcontador][1]= True
                    if direcao == 's':
                        mapa_gerado[local[0]+Lcontador][local[1]][1]= True
                    if direcao == 'd':
                        mapa_gerado[local[0]][local[1]+Lcontador][1]= True
                    Lcontador+= 1
                except IndexError:
                    pass
            print('O local foi iluminado')
        case 'Mapa completo':
            for linha in mapa_gerado:
                for coluna in linha:
                    coluna[1]= True
            print('Seu mapa está completo')
        case 'Orbe elétrico':
            mapa_gerado[local[0]][local[1]][1]= True
            if mapa_gerado[local[0]][local[1]][0] == 3:
                vetor_efeitos[6]= 2
            print('As águas dessa floresta foram eletrocutadas')
def itemsCombate(tipo_item):
    global vetor_efeitos
    vetor_efeitos= [0, 0, 0, 0, 0, 0, 0]
    match tipo_item:
        case 'Amuleto da sorte':
            vetor_efeitos[0]= 5
            print('Você está com sorte! Seus ataques praticamente nunca erram!')
        case 'Bomba de fumaça':
            vetor_efeitos[1]= 15
            print('Você está quase invisível')
        case 'Orbe elétrico':
            vetor_efeitos[2]= 1
            print('Seu inimigo foi paralizado')
        case 'Escudo':
            vetor_efeitos[3]= 1
            print('O próximo ataque será defendido')
        case 'Tocha':
            vetor_efeitos[4]= 1
            print('O inimigo está em chamas')
        case 'Pedra luminosa':
            vetor_efeitos[5]= 5
            print('Seu inimigo não consegue ver direito')

#ITEMS : (LEANDRO)

##################
#Início do programa principal
#Algums items que eu vou adicionar
vetor_items= ['Chave', 'Tocha', 'Pedra luminosa', 'Mapa completo', #Items do mapa
              'Bomba de fumaça', 'Orbe elétrico', 'Escudo', 'Amuleto da sorte', #Items de combate (não são ataques)
               'Poção', #Outros items
              ]
vetor_efeitos= [0, 0, 0, 0, 0, 0, 0]
tamanho_inicial_mapa= 14
sala= 0
r = inicio()
if r == 1:  
    config = EscolhaPersonagem()
    print('Antes de começar, um rápido tutorial sobre o jogo.')
    print('Seu objetivo é conseguir o máximo de pontos possíveis, ao mesmo tempo que atravessa o máximo de salas possiveis.')
    print('O mapa está totalmente escuro, e se revelará enquanto você anda por ele.')
    print("Haverá itens durante sua jornada, você descobrirá o que eles fazem quando achá-los")
    print("Caso uma luta deixe-o ferido lembre-se de descansar quando tiver uma poção!")
    print("Legenda: ")
    print("Árvore:")
    print(f"{Fore.GREEN}_  {Style.RESET_ALL}")
    print(f'{Fore.GREEN}T  {Style.RESET_ALL}')
    print("Água:")
    print(f"{Fore.BLUE}~  {Style.RESET_ALL}")
    print(f'{Fore.BLUE}~  {Style.RESET_ALL}')
    print("Pedra:")
    print(f'{Fore.LIGHTBLACK_EX}_  {Style.RESET_ALL}')
    print(f'{Fore.LIGHTBLACK_EX}o  {Style.RESET_ALL}')
    print("Parede de Madeira:")
    print(f'{Fore.YELLOW}{Style.DIM}#  {Style.RESET_ALL}')
    print(f'{Fore.YELLOW}{Style.DIM}#  {Style.RESET_ALL}')
    print("Item:")
    print(f'{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}§  {Style.RESET_ALL}')
    print("Baú:")
    print(f'{Fore.YELLOW}$  {Style.RESET_ALL}')
    print(f'{Fore.YELLOW}B  {Style.RESET_ALL}')
    print("Armadilha:")
    print(f'{Fore.LIGHTRED_EX}_  {Style.RESET_ALL}')
    print(f'{Fore.LIGHTRED_EX}X  {Style.RESET_ALL}')
    print("Chave:")
    print(f'{Fore.LIGHTWHITE_EX}{Style.BRIGHT}   {Style.RESET_ALL}')
    print(f'{Fore.LIGHTWHITE_EX}{Style.BRIGHT}f  {Style.RESET_ALL}')
    print("Inimigo:")
    print(f' {Fore.RED}O {Style.RESET_ALL}')
    print(f'{Fore.RED}| |{Style.RESET_ALL}')
    print("\nBom jogo!\n")

    iniciandoMapa(tamanho_inicial_mapa)
    while True: 
        MenuDeAcoes(config)
            
if r == 2:
    print('Que pena! Espero que volte logo!')
