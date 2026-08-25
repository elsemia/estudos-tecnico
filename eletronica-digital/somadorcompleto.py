# Sum = A xor B xor Cin
# Cout = AB + BCin + ACin

A = ['1', '0', '0', '1']
B = ['1', '0', '1']
resultado = []
carry = 0
# total = A + B + carry (resulta em decimal)
# bit resultado (unidade) -> total % 2 "quanto fica" (analogia com base 10: 42%10=2 -> unidade, fica)
# carry out (decimal) -> total // 2 "quanto sobe" (analogia com base 10: 42//10=4 -> dezena, "não cabe ali", sobe)
diferenca_tamanho = len(A) - len(B)

if len(A) > len(B):
    for i in range(diferenca_tamanho):
        B.insert(0, 0)
elif len(B) > len(A):
    for i in range(abs(diferenca_tamanho)):
        A.insert(0, 0)

print(A)
print(B)

for i in range(-1, -len(A) - 1, -1):  # começa no último valor da lista, vai até o primeiro, num passo de -1
    bit_A = int(A[i])  # bit de A na posição atual - contando da direita para esquerda
    bit_B = int(B[i])  # bit de B na posição atual - contando da direita para esquerda
    total = bit_A + bit_B + carry  # soma = valores dos bits atuais mais o carry
    resultado.append(total % 2)  # juntando bit de resultado da soma à lista
    carry = total // 2  # atualizando carry

if carry > 0:  # se o carry, depois da última iteração, estiver com valor 1, ele é o bit mais significativo
    resultado.append(carry)
resultado.reverse()  # a lista foi construída do bit menos significativo para o mais significativo — precisa inverter pra ficar na ordem de leitura normal

print(resultado)