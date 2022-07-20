"""
Integrantes do grupo:

Gabriel Sá
Fabio Adriano
Elberth Paulino
Luana Wiese 


"""


def ArqParaHamming():
    #Essa funcao serve para transformar um arquivo no seu formato original para um arquivo binario ja com o hamming incluso
    #O tamanho do hamming é definido por um algoritmo sendo assim ele muda para cada arquivo
    arqInicial = input("qual o local do arquivo?")
    binarioArq = open(r"Binario.txt", "w")   #É onde é depositado o binario do arquivo   
    
    melhorTamanhoHamming, contadorPotenciasDois = 8, 4                                                                                                                                                                                    
    
    with open(arqInicial, "rb") as main: #
        #Abre o arquivo desejado lendo ele em byte
        mainTexto = main.read()
        tamanhoTotal = len(mainTexto * 8)       #O tamanho multiplicado por 8 pois cada byte vai ter tamanho 8 em binario
        while (melhorTamanhoHamming - contadorPotenciasDois) * 100_000 < tamanhoTotal:
            #Ve qual o menor tamanho de hamming possivel sendo que nao pode haver mais de 100.000 hamming por arquivo
            melhorTamanhoHamming = (melhorTamanhoHamming * 2)
            contadorPotenciasDois += 1

        y = 0
        listaBinario = []
        listaSublistas = []
        for byte in mainTexto:
            #Separa a data ao tamanho ideal para embaralhar e fazer o hamming
            binario = bin(byte)[2:]
            #Pega o byte e transforma em binario, excluindo os 2 primeiros caracteres
            if len(binario) < 8: #Caso binario seja menor que 8, adiciona 0 a esquerda
                    qntZeros = 8 - len(binario)                                                             
                    binarioNovo = (f'{"0" * qntZeros}{binario}')
            else: #Caso já seja de tamanho 8, continua.
                binarioNovo = binario 
            for i in binarioNovo: #Adiciona o binario a uma lista
                listaBinario.append(i) 
                

            while len(listaBinario) >= ((melhorTamanhoHamming - contadorPotenciasDois)): #Enquanto o tamanho do binario novo for maior que a 
                #quantidade de data do Hamming
                mensagem = listaBinario[0:(melhorTamanhoHamming - contadorPotenciasDois)] #Separa os bytes de data da lista binario.
                mensagemLista,tamanhoHamming = dataParaLista(mensagem) #Roda a função data para a lista
                adicionarHamming = list(binarioParaHamming(mensagemLista,tamanhoHamming)) #Adiciona o Hamming
                listaSublistas.append(adicionarHamming) #Adiciona a lista com o hamming nas sublistas
                del(listaBinario[0:(melhorTamanhoHamming - contadorPotenciasDois)]) #Deleta os bits de data já utilizados
        
            if len(listaSublistas) == 300: #Caso tenha 300 hammings na sublista, embaralha eles e escreve no arquivo destino
                escreveNoHamming = embaralhar(listaSublistas)
                binarioArq.write(escreveNoHamming)
                listaSublistas = []

        if len(listaBinario) != 0: #Caso no fim do ciclo, ainda possua data não processadas, processa os hammings
            while len(listaBinario) < (melhorTamanhoHamming - contadorPotenciasDois):
                listaBinario.insert(0,"0")
            mensagem = listaBinario[0:(melhorTamanhoHamming - contadorPotenciasDois)]
            mensagemLista,tamanhoHamming = dataParaLista(mensagem)
            adicionarHamming = list(binarioParaHamming(mensagemLista,tamanhoHamming))
            listaSublistas.append(adicionarHamming)
        
        if len(listaSublistas): #Caso ainda tenha hammings não processados, embaralha e adiciona eles no arquivo
            escreveNoHamming = embaralhar(listaSublistas)
            binarioArq.write(escreveNoHamming)
        
    binarioArq.close()

    print("\n"*3, f"Terminei :D \rFoi feito um Hamming com {melhorTamanhoHamming} bits totais sendo {melhorTamanhoHamming - contadorPotenciasDois} bits de data e {contadorPotenciasDois}\
 de pariedade")


def arquivoHammingParaBinario(localArquivo):
    binarioArq = open(localArquivo, "r") #Abre um arquivo pelo local informado
    listaBits,semHammingList1 = [], [] #Cria duas listas
    extensao = input("Qual era a extensão do arquivo?") 
    des = "Destino." + extensao #Cria um arquivo com a Extensão fornecida
    y = binarioArq.read() #Lê o arquivo fornecido
    z = (len(y)) #Verifica o tamanho total do arquivo
    errosLista,listaHammings = 0,[] 
    tamanhoHammingVolta = 8 
    hammina = 0
    
    while tamanhoHammingVolta * 100_000 < z: #Verifica o tamanho do hamming utilizado se é menor que o original
            tamanhoHammingVolta = (tamanhoHammingVolta * 2) 
    
    if z % tamanhoHammingVolta != 0: #Caso nao seja divisivel exatamente:
        print("Foram adicionados ou removidos bits, a recuperação do arquivo não é possivel")
        return() #Encerra o programa

    with open(des, "wb") as file: #Abre o arquivo fornecido
        for bit in y: #Lê o arquivo
            listaHammings.append(bit) #adiciona bits a uma lista de hamming
            if len(listaHammings) == (300 * tamanhoHammingVolta): #Caso possua 300 hammings
                hammingOrdem = desembaralhar(listaHammings,tamanhoHammingVolta) #Desembaralha o hamming
                listaHammings = [] #Reseta a lista Hamming
                for chr in hammingOrdem: #Lê o hamming em ordem
                    listaBits.append(chr) #Adiciona a uma lista
                    if len(listaBits) == tamanhoHammingVolta: #Caso o tamanho da lista seja o suficiente para fazer o hamming
                        hammina += 1 
                        semHammingStr,erros = HammingParaBinario(listaBits) #Processa o Hamming, removendo as paridades
                        for i in semHammingStr: #Lê o binario sem o hamming
                            semHammingList1.append(i) #Adiciona a uma lista
                        while len(semHammingList1) >= 8: #Enquando a Lista sem hamming for maior igual que 8 (tamanho configurado do byte)
                            semHammingint = int("".join([i for i in semHammingList1[0:8]]),2) #Adiciona em uma String
                            file.write(semHammingint.to_bytes(1,"little")) #Escreve o aquivo como byte
                            del(semHammingList1[0:8]) #Deleta os bytes já processados
                        if erros: #Caso possua erros
                            errosLista += 1 #Adiciona na quantidade de erros corrigidos
                        del(listaBits[0:tamanhoHammingVolta]) #Retira o hamming já processado
        if len(listaHammings) != 0: #Caso ao final do ciclo, ainda possua hammings não processados
            #repete o processo para processa-los
            hammingOrdem = desembaralhar(listaHammings,tamanhoHammingVolta) 
            listaHammings = []
            for chr in hammingOrdem:
                listaBits.append(chr)
                if len(listaBits) == tamanhoHammingVolta:
                    hammina += 1
                    semHammingStr,erros = HammingParaBinario(listaBits)
                    for i in semHammingStr:
                        semHammingList1.append(i)
                    while len(semHammingList1) >= 8:
                        semHammingint = int("".join([i for i in semHammingList1[0:8]]),2)
                        file.write(semHammingint.to_bytes(1,"little"))
                        del(semHammingList1[0:8])
                    if erros:
                        errosLista += 1
                    del(listaBits[0:tamanhoHammingVolta])
    if not errosLista:
        print("\n"*3,"Não foram encontrados erros, o arquivo foi convertido ao seu formato original :D")
    elif errosLista:
        print("\n"*3,f"Foram encontrados e corrigidos {errosLista} erros. O arquivo foi arrumado e exportado ao seu formato original :D")


def embaralhar(listaHamming): #Embaralha o Hamming
    tamanhoHamming = len(listaHamming[0]) #Recebe o tamanho da lista hamming
    listaRetorno = "" #Retorna uma String
    for posicao in range(tamanhoHamming): #Ordena os hammings
        for hamming, _ in enumerate(listaHamming): #Percorre o Hamming de acordo com o tamanho definido
            listaRetorno = listaRetorno + str(listaHamming[hamming][posicao]) #Adiciona o bit adequado de acordo com as variaveis dos for
    return(listaRetorno)


def desembaralhar(listaHamming,tamanhoHamming): #Desembaralha o Hamming
    numeroHammings = len(listaHamming) // tamanhoHamming #Calcula a quantidade de Hammings dentro da Lista
    strRetorno = ""
    for hamming in range(numeroHammings): #Percorre o Hamming de acordo com o tamanho definido
        for posicao in range(tamanhoHamming): #Recupera o byte adequado para cada hamming
            strRetorno = strRetorno + listaHamming[hamming + (posicao * numeroHammings)] #Adiciona o bit adequado de acordo com as variaveis dos for
    return(strRetorno)


def dataParaLista(mensagem):
    #Essa funcao serve paratransformar a data em uma lista do tamnaho apropriado
    #Ela tambem serve para colocar as posicoes dos bit de paridade e configurar o tamanho ideal para o hamming
    potenciaDeDois = 8      #Tamnaho minimo para o hamming é 8 bits                                                           
    marcadorDois = 2                                                            
    while potenciaDeDois < len(mensagem):       #Enquanto ammensagem fot maior que o tamanho do hamming aumente para o proximo tamanho de hamming
        potenciaDeDois = potenciaDeDois * 2
    mensagemLista = [i for i in mensagem]       #Transforma a mensagem em uma lista 
    bitsem8 = ["*"] * potenciaDeDois        #Cria uma lista com o tamanho do hamming com * em todas suas posicoes
    posicao8 = 0
    for posicao, _ in enumerate(bitsem8):       #Precorre a lista com o tamanho ideal e coloca a data pulando as posicoes dos bits de pariedade
        if posicao == marcadorDois:
            marcadorDois = marcadorDois * 2           
            continue
        if posicao > 2:
            bitsem8[posicao] = int(mensagemLista[posicao8])
            posicao8 += 1

    return(bitsem8,marcadorDois)        #Retorna o tamanho do hamming e a lista sem os bits de pariedade
                                        #Exemplo: entrada -> 1010, saida -> [*,*,*,1,*,0,1,0], tamnho de hamming de 8 bits


def binarioParaHamming(bitsemHamming,tamanhoHamming):
    #Essa funcao serve para colocar os bits de pariedeade nas posicoes adequadas
    #A funcao recebe uma lista só com os bits de data pulando onde deveria haver os bits de pariedade
    #e o tamanho do hamming, a funcao consegue fazer hamming de qualquer tamanho desde que seja uma potencia de 2
    grupos = []
    bitsDeParidade,potenciasDois = 3,8      #bitsdePariedade recebe a menor quantidade de bits de pariedade posivel(a posicao 0 nao conta)
        
    for contadorNeutro in range(1, tamanhoHamming + 1):  
        #Determina quantos bits de pariedade serao necessarios para a lista
        if contadorNeutro > potenciasDois:
            potenciasDois = potenciasDois * 2
            bitsDeParidade += 1
        
    for _ in range(bitsDeParidade):
        #Cria sub listas dentro da lista grupos para cada grupo que a list precisaria para fazer o hamming
        grupos.append([]) 

    for posicaoHamming, _ in enumerate(bitsemHamming):
        #Serve para Separar as posicoes em seus repectivos grupos do hamming
        contadorGrupo = -1      #O contador comeca do -1 pois od grupos sao adicionados de tras para frente 
        posicaoHammingBin = [int(i) for i in bin(posicaoHamming) if i != "b"]       #Transforma o numero da posicao em binario removendo o 'b'
        
        #Padroniza todos os binarios para o numero de digitos maximo para a matrix
        while len(posicaoHammingBin) < bitsDeParidade:
            posicaoHammingBin.insert(0, 0)
        if len(posicaoHammingBin) > bitsDeParidade:
            posicaoHammingBin.pop(0)
        
        #Adiciona as posicoes nos respectivos grupos
        for posicaoBinario, bitBinario in enumerate(posicaoHammingBin):
            if bitBinario:
                grupos[contadorGrupo].append(posicaoHamming)
            contadorGrupo -= 1

    for subGrupo in grupos:
        #Percorre a lista que contem os sub grupos
        pariedade = 0       #Reseta a pariedade de cada grupo
        for bit in subGrupo:
            #Percorre os sub grupos
            pariedade = pariedade ^ int(bitsemHamming[bit]) if bitsemHamming[bit] != "*" else pariedade
            #Faz a priedade com a posicao se na posicao nao estiver *
        bitsemHamming[subGrupo[0]] = pariedade
        #Coloca os bits os de pariedade na posicao adequada

    pariedade = 0
    for posicaoGeral in bitsemHamming:
        #Calcula e coloca o bite pariedade extra na posicao 0
        if posicaoGeral != "*":
            pariedade = pariedade ^ posicaoGeral
    bitsemHamming[0] = pariedade

    return("".join([str(i) for i in bitsemHamming]))


def HammingParaBinario(bitsComHamming): #Recebe uma string com o hamming adicionado
    listaBits = [int(i) for i in bitsComHamming] #Transforma em lista
    erros = [] #Cria uma lista
    pariedade = 0 
    potenciaDois = 4 #Recebe o valor 4
    listaBitsPariedade = []

    for posicao,bite in enumerate(listaBits): #Percorre a lista com hamming
        pariedade = pariedade ^ posicao if bite else pariedade #Checa a pariedade
    if pariedade: #Caso a pariedade seja 1
        erros.append(pariedade) #Há um erro
        listaBits[pariedade] = int(not listaBits[pariedade]) #Corrige um erro
    
    for posicao, _ in enumerate(listaBits): #Retirar os bits de pariedade
        if posicao > 2: #Se a posição for maior que 2
            if posicao == potenciaDois: #Posição igual a potencia de dois
                listaBitsPariedade.insert(0,posicao) #Inserta a posição do bit de pariedade na lista
                potenciaDois = potenciaDois * 2 #Dobra a potencia de dois
                continue
        elif posicao <= 2: #Se a posição for menor igual a 2
            listaBitsPariedade.insert(0,posicao) #Inserta a posição do bit de pariedade na lista

    for posicaoPariedade in listaBitsPariedade: #Remove as posições de pariedade começando pela maior
        del(listaBits[posicaoPariedade]) #Deleta os bits de pariedade
    
    bitsComHamming = "".join([str(i) for i in listaBits]) #Retorna a String
    return(bitsComHamming, erros)


def main():
    print("Escolha uma opção: \n [1] Binario para hamming \t \t [2] Hamming para binario \t \t [3] Arquvio para hamming \t \t [4] Arquivo com Hamming para arquivo original")
    opcao = input("")
    
    if opcao == "1":
        mensagem = input("qual os bits de data?")
        mensagemLista,tamanhoHamming = dataParaLista(mensagem)
        print (binarioParaHamming(mensagemLista,tamanhoHamming))
    elif opcao == "2":
        mensagem = input("qual os bits com Hamming? ")
        binario, erros = HammingParaBinario(mensagem)
        if erros:
            print(f'\nTeve um erro na posição {erros[0]} \nA mensagem corrigida ficou {binario}')
        else:
            print(f'Nao teve erros, sua mensagem é {binario}')
    elif opcao == "3":
        ArqParaHamming()
    elif opcao == "4":
        localArquivo = input("qual o local do arquivo com o hamming? ")
        arquivoHammingParaBinario(localArquivo)


if __name__ == '__main__':
    main()

