from random import randint
from random import choice
from colorama import Fore
from colorama import Style
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

##################
#Início do programa principal
tamanho= 14
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
'''
Movimentação é liberada
'''
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