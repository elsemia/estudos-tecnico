## tinha preguica de fazer o mapa de karnaugh entao eu decidi fazer esse codigo para me poupar algo como o tempo. Para isso, minha maior dificuldade foi
## o entendimento e implementacao de Quine-McCluskey

def binario_em_linha(binario):
    binario = str(binario)
    bits = []
    for c in binario:
        bits.append(int(c))
    return bits


def pedir_quantidade_entradas():
    while True:
        try:
            n = int(input("quantidade de variáveis: "))
            if n < 1:
                print("A quantidade de variáveis deve ser pelo menos 1.")
                continue
            return n
        except ValueError:
            print("Isso não é um valor válido. Digite apenas um número inteiro.")


def gerar_tabela_entradas(n):
    tabela = []
    for i in range(2**n): ## calcula numero de linhas
        binario = f"{i:0{n}b}" ## calcula o binario daquela linha -> b: formatar em binário. 0: preencher esquerda com zeros.
        ## n -> largura total do resultado deverá ser n. i -> valor da iteracao
        linha = binario_em_linha(binario)
        tabela.append(linha)
    return tabela

def pedir_saidas(tabela):
    saidas = []
    for linha in tabela:
        print(linha)
        while True:
            valor = input("Valor de saída [0 ou 1 ou X]: ")
            if valor not in ["0", "1", "X"]:
                print("Isso não é um valor válido.\nDigite apenas 0, 1 ou X.")
            else:
                saidas.append(valor)
                break
    return saidas


def gerar_tabela_verdade(): ## Single Responsibility Principle
    n = pedir_quantidade_entradas()
    entradas = gerar_tabela_entradas(n)
    saidas = pedir_saidas(entradas)
    for entrada, saida in zip(entradas, saidas): ## unpacking
        print(entrada, saida)
    return entradas, saidas, n


def linha_em_termo(linha):
    return "".join(str(bit) for bit in linha)


## Fase 1: encontrar implicantes primos (combinação de Quine-McCluskey)

def contar_uns(termo):
    return termo.count('1')

def agrupar_por_numero_de_uns(termos):
    grupos = {}
    for termo in termos:
        grupos.setdefault(contar_uns(termo), []).append(termo)
    return grupos

def tentar_combinar(termo_a, termo_b):
    diferenca_encontrada = False
    resultado = []
    for c_a, c_b in zip(termo_a, termo_b):
        if c_a != c_b:
            if c_a == '-' or c_b == '-':
                return None ## traco em posicoes diferentes: não combina
            if diferenca_encontrada:
                return None ## mais de uma posicao diferente: não combina
            diferenca_encontrada = True
            resultado.append('-')
        else:
            resultado.append(c_a)
    if not diferenca_encontrada:
        return None ## termos idênticos, não é uma combinacao válida
    return "".join(resultado)

def encontrar_implicantes_primos(termos_iniciais):
    termos_atuais = set(termos_iniciais)
    implicantes_primos = set()

    while termos_atuais:
        grupos = agrupar_por_numero_de_uns(termos_atuais)
        chaves = sorted(grupos.keys())
        usados = set()
        novos_termos = set()

        for i in range(len(chaves) - 1): ## só faz sentido comparar grupos com número de 1s "vizinho"
            for termo_a in grupos[chaves[i]]:
                for termo_b in grupos[chaves[i + 1]]:
                    combinado = tentar_combinar(termo_a, termo_b)
                    if combinado is not None:
                        novos_termos.add(combinado)
                        usados.add(termo_a)
                        usados.add(termo_b)

        for termo in termos_atuais:
            if termo not in usados:
                implicantes_primos.add(termo) ## nunca combinado nesta rodada = implicante primo

        termos_atuais = novos_termos

    return implicantes_primos


## Fase 2: tabela de cobertura e seleção dos implicantes

def termo_cobre_minterm(termo, minterm):
    for c_termo, c_minterm in zip(termo, minterm):
        if c_termo != '-' and c_termo != c_minterm:
            return False
    return True

def montar_tabela_cobertura(implicantes_primos, minterms_obrigatorios):
    return {
        minterm: [imp for imp in implicantes_primos if termo_cobre_minterm(imp, minterm)]
        for minterm in minterms_obrigatorios
    }

def selecionar_implicantes(implicantes_primos, minterms_obrigatorios):
    tabela = montar_tabela_cobertura(implicantes_primos, minterms_obrigatorios)
    selecionados = set()

    for minterm, cobrem in tabela.items():
        if len(cobrem) == 1:
            selecionados.add(cobrem[0]) ## coluna com um único implicante = essencial

    restantes = {
        m for m in minterms_obrigatorios
        if not any(termo_cobre_minterm(imp, m) for imp in selecionados)
    }

    ## cobertura gulosa do que sobrou: a cada rodada escolhe quem cobre mais minterms restantes.
    ## não é o método de Petrick, então não garante o mínimo absoluto em "prime implicant charts" cíclicos.
    while restantes:
        melhor_implicante, melhor_cobertura = None, set()
        for imp in implicantes_primos:
            cobertura = {m for m in restantes if termo_cobre_minterm(imp, m)}
            if len(cobertura) > len(melhor_cobertura):
                melhor_implicante, melhor_cobertura = imp, cobertura
        selecionados.add(melhor_implicante)
        restantes -= melhor_cobertura

    return selecionados


## Fase 3: formatação da expressão booleana

def formatar_termo(termo):
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    partes = []
    for i, bit in enumerate(termo):
        if bit == '1':
            partes.append(letras[i])
        elif bit == '0':
            partes.append(letras[i] + "'")
        ## '-' -> variável eliminada, omitida do termo
    return "".join(partes) if partes else "1" ## termo todo '-' cobre tudo -> literal 1

def formatar_expressao(implicantes_selecionados):
    return " + ".join(formatar_termo(t) for t in implicantes_selecionados)


def simplificar_expressao():
    entradas, saidas, n = gerar_tabela_verdade()

    termos_iniciais = set()
    minterms_obrigatorios = set()
    for linha, saida in zip(entradas, saidas):
        termo = linha_em_termo(linha)
        if saida in ("1", "X"):
            termos_iniciais.add(termo) ## don't cares entram na combinação...
        if saida == "1":
            minterms_obrigatorios.add(termo) ## ...mas não são exigidos na cobertura final

    if not minterms_obrigatorios:
        print("Expressão simplificada: 0")
        return

    implicantes_primos = encontrar_implicantes_primos(termos_iniciais)
    implicantes_selecionados = selecionar_implicantes(implicantes_primos, minterms_obrigatorios)
    print("Expressão simplificada:", formatar_expressao(implicantes_selecionados))


simplificar_expressao()
