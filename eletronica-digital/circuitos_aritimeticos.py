def somador_completo(A,B):
# Sum = A xor B xor Cin
# Cout = AB + BCin + ACin

    resultado = []
    carry = 0
    novo_A = A[:]
    novo_B = B[:] # criar copias das listas evita de alterar a lista original. 
    diferenca_tamanho = len(novo_A) - len(novo_B)

    if len(novo_A) > len(novo_B): # igualando tamanho das listas
        for i in range(diferenca_tamanho):
            novo_B.insert(0, 0)
    elif len(novo_B) > len(novo_A):
        for i in range(abs(diferenca_tamanho)):
            novo_A.insert(0, 0)

    # total = A + B + carry (resulta em decimal)
    # bit resultado (unidade) -> total % 2 "quanto fica" (analogia com base 10: 42%10=2 -> unidade, fica)   
    # carry out (decimal) -> total // 2 "quanto sobe" (analogia com base 10: 42//10=4 -> dezena, "não cabe ali", sobe)

    for i in range(-1, -len(novo_A) - 1, -1):  # começa no último valor da lista, vai até o primeiro, num passo de -1
        bit_A = int(novo_A[i])  # bit de A na posição atual - contando da direita para esquerda
        bit_B = int(novo_B[i])  # bit de B na posição atual - contando da direita para esquerda
        total = bit_A + bit_B + carry  # soma = valores dos bits atuais mais o carry
        resultado.append(total % 2)  # juntando bit de resultado da soma à lista
        carry = total // 2  # atualizando carry
    if carry > 0:  # se o carry, depois da última iteração, estiver com valor 1, ele é o bit mais significativo
        
        resultado.append(carry)

    resultado.reverse()  # a lista foi construída do bit menos significativo para o mais significativo — precisa inverter pra ficar na ordem de leitura normal
    return resultado

def complemento_de_dois(B): # A - B = A + (-B)
    B = B[:]
    comp_dois = []
    for i in range(0, len(B)):
        bit_B = int(B[i])
        inverte = 1 - bit_B
        comp_dois.append(inverte)
    resultado = somador_completo(comp_dois, [1])
    return resultado

def subtrator_completo(A, B):
    A = A[:]
    B = B[:]
    tamanho_final = max(len(A), len(B)) + 1 # valor limite 2^(N-1)
    while len(A) < tamanho_final:
        A.insert(0, 0)
    while len(B) < tamanho_final:
        B.insert(0,0)

    resultado = somador_completo(complemento_de_dois(B), A)
    return resultado[-tamanho_final::]


A = ['1', '0', '1', '0']
B = ['1', '0', '0']
print(somador_completo(A, B))
print(subtrator_completo(A,B))