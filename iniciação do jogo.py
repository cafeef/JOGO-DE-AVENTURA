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
    Classe, Forc, Inte, Agl, Ca = 0, 0, 0, 0, 0
    Hab1, Hab2, Hab3, Hab4, Hab5 = 0, 0, 0, 0, 0
    item1, item2, item3, item4, item5, armadura = 0, 0, 0, 0, 0, 0
    d_item1, d_item2, d_item3, d_item4, d_item5 = 0, 0, 0, 0, 0
    xp = 20
    r = ApresentacaoPersonagem()
    if r == 1:
        Classe = r
        print('Você escolheu bárbaro. Você possui: ')
        vida, Forc, Inte, Agl, armadura, d_item1, Ca = 14, 5, 1, 4, 4, 5, 10
        item1 = 'machado'
        print(f'{Forc} DE FORÇA | {Inte} DE INTELIGÊNCIA | {Agl} DE AGILIDADE ')
        print('VOCÊ GANHOU SUA PRIMEIRA ARMA: MACHADO')
        atributos = [Classe, vida, Forc, Inte, Agl, Ca]
        itens = [item1, item2, item3, item4, item5, armadura]
        dano_itens = [d_item1, d_item2, d_item3, d_item4, d_item5, None]
        habilidades = [Hab1, Hab2, Hab3, Hab4, Hab5, xp]
        MaPerso = [[atributos], [itens], [dano_itens], [habilidades]]
        return MaPerso
    
    if r == 2:
        Classe = r
        print('Você escolheu guerreiro. Você possui: ')
        vida, Forc, Inte, Agl, armadura, d_item1, Ca = 14, 4, 3, 3, 4, 4, 10
        item1 = 'espada'
        print(f'{Forc} DE FORÇA | {Inte} DE INTELIGÊNCIA | {Agl} DE AGILIDADE ')
        print('VOCÊ GANHOU SUA PRIMEIRA ARMA: ESPADA')
        atributos = [Classe, vida, Forc, Inte, Agl, Ca]
        itens = [item1, item2, item3, item4, item5, armadura]
        dano_itens = [d_item1, d_item2, d_item3, d_item4, d_item5, None]
        habilidades = [Hab1, Hab2, Hab3, Hab4, Hab5, xp]
        MaPerso = [[atributos], [itens], [dano_itens], [habilidades]]
        return MaPerso

    if r == 3:
        Classe = r
        print('Você escolheu mago. Você possui: ')
        vida, Forc, Inte, Agl, armadura, d_item1, Ca = 10, 2, 4, 2, 2, 3, 7
        item1 = 'cajado'
        print(f'{Forc} DE FORÇA | {Inte} DE INTELIGÊNCIA | {Agl} DE AGILIDADE ')
        print('VOCÊ GANHOU SUA PRIMEIRA ARMA: CAJADO')
        atributos = [Classe, vida, Forc, Inte, Agl, Ca]
        itens = [item1, item2, item3, item4, item5, armadura]
        dano_itens = [d_item1, d_item2, d_item3, d_item4, d_item5, None]
        habilidades = [Hab1, Hab2, Hab3, Hab4, Hab5, xp]
        MaPerso = [[atributos], [itens], [dano_itens], [habilidades]]
        return MaPerso
    



#############
from random import randint
r = inicio()
if r == 1:
    MaPerso = EscolhaPersonagem()
if r == 2:
    print('Que pena! Espero que volte logo!')