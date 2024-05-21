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
    Classe, Forc, Inte, Agl = 0, 0, 0, 0
    ataque1, ataque2, ataque3, ataque4, ataque5, armadura = 0, 0, 0, 0, 0, 0
    d_ataque1, d_ataque2, d_ataque3, d_ataque4, d_ataque5, Ca = 0, 0, 0, 0, 0, 0
    item1, item2, item3, item4, item5, xp = 0, 0, 0, 0, 0, 20
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
    
def MenuDeAcoes(config):
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
        Ataque()
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



#############
from random import randint
r = inicio()
if r == 1:
    config = EscolhaPersonagem()
    print(config[0])
    print(config[1])
    print(config[2])
    print(config[3])
    while True: 
        MenuDeAcoes(config)
if r == 2:
    print('Que pena! Espero que volte logo!')