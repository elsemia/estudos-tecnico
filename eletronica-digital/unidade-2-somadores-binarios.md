# Unidade 2 — Eletrônica Digital: Circuitos Somadores

Anotações sobre circuitos somadores e uma breve explicação do código que implementa a soma binária.

## Contexto

Tive um pouco de dificuldade para entender a lógica do carry no somador completo, então passei algumas horas até compreender e conseguir escrever um algoritmo que realiza uma soma binária completa. A dificuldade estava em entender como o carry é calculado "pelas portas lógicas". Com o Mapa de Karnaugh, entendi a junção das portas para o tratamento do carry.

## O problema

Para somar números binários com mais de 2 bits, é necessário um **circuito somador completo**.

Exemplo: somar `A = 1001` e `B = 1101`. Precisamos somar cada bit individualmente, da direita para a esquerda.

O circuito somador completo tem três entradas: `bit_A`, `bit_B` e `Carry`. `bit_A` e `bit_B` referem-se à casa mais à direita do valor binário; `Carry` sempre começa em `0`.

Como a soma precisa percorrer os valores da direita para a esquerda, optei por tratar `A` e `B` como listas, e uma lista vazia para guardar o resultado.

## Soma binária: conceitos rápidos

- **Carry out**: valor que "vai" na soma.
- **Carry in**: valor que "vem" na soma.

(duas formas de olhar para o mesmo valor, dependendo de qual bloco do circuito está sendo observado)

### Soma — porta XOR

| A | B | A XOR B |
|---|---|---------|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

### Carry — porta AND

| A | B | A AND B |
|---|---|---------|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

Para somar 2 bits, uma porta XOR calcula o `Sum` e uma porta AND calcula o `Carry Out`.

## Tabela-verdade — meio-somador (2 bits)

| A | B | Cout | Sum |
|---|---|------|-----|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 0 |

## Somador completo (3 entradas)

Para valores com mais de 2 bits, o Carry Out de uma posição vira uma entrada (Carry In) na próxima posição. Usando o Mapa de Karnaugh:

```
Cout = A.Cin + A.B + B.Cin
```

A soma sempre começa pelo bit menos significativo (o mais à direita), e `Cin` começa em `0`.

## Tabela-verdade — somador completo (3 bits)

| A | B | Cin | Cout | Sum |
|---|---|-----|------|-----|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 | 1 |
| 1 | 0 | 1 | 1 | 0 |
| 1 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 1 |

## Por que usar `%` e `//` em vez das portas lógicas diretamente

As fórmulas booleanas acima (`Sum = A xor B xor Cin`, `Cout = A.Cin + A.B + B.Cin`) e a conta `total = bit_A + bit_B + carry` com `%2` e `//2` calculam exatamente a mesma coisa, só que por caminhos diferentes — um em lógica booleana, o outro em aritmética comum.

Somando `bit_A + bit_B + carry` como números normais, o resultado (`total`) só pode ser `0`, `1`, `2` ou `3`, já que cada um dos três só vale `0` ou `1`. Escrevendo esses 4 valores possíveis em binário, com 2 dígitos:

```
total=0 -> 00
total=1 -> 01
total=2 -> 10
total=3 -> 11
```

O dígito da direita (casa das unidades) é sempre o `Sum` daquela posição; o dígito da esquerda (casa dos 2) é sempre o `Cout`. Por isso:

- `total % 2` (resto da divisão por 2) extrai o dígito da direita → é o bit de `Sum`.
- `total // 2` (divisão inteira por 2) extrai o dígito da esquerda → é o `Carry Out`.

Comparando com a tabela-verdade acima: quando `total` é `2` ou `3` (pelo menos dois dos três bits são `1`), `Cout=1` — exatamente quando `total // 2 = 1`. E quando `total` é `1` ou `3` (quantidade ímpar de bits em `1`), `Sum=1` — exatamente quando `total % 2 = 1`.

## Código

```python
# Sum = A xor B xor Cin
# Cout = AB + BCin + ACin

A = ['1', '0', '0', '1']
B = ['1', '1', '0', '1']
resultado = []
carry = 0

# total = A + B + carry (resulta em decimal)
# bit resultado (unidade) -> total % 2 "quanto fica" (analogia com base 10: 42%10=2 -> unidade, fica)
# carry out (decimal)     -> total // 2 "quanto sobe" (analogia com base 10: 42//10=4 -> dezena, "não cabe ali", sobe)

for i in range(-1, -len(A) - 1, -1):  # começa no último valor da lista, vai até o primeiro, passo -1
    bit_A = int(A[i])   # bit de A na posição atual, contando da direita para a esquerda
    bit_B = int(B[i])   # bit de B na posição atual, contando da direita para a esquerda
    total = bit_A + bit_B + carry   # soma dos bits atuais mais o carry
    resultado.append(total % 2)     # bit de resultado da soma, adicionado à lista
    carry = total // 2              # atualizando o carry

if carry > 0:   # se sobrar carry após a última iteração, ele é o bit mais significativo
    resultado.append(carry)

resultado.reverse()   # a lista foi construída do bit menos significativo para o mais significativo, precisa inverter para ficar na ordem de leitura normal

print(resultado)
```

## Materiais de apoio

- [Nivaldo Junior — Circuitos Somadores](https://youtu.be/YYuTJexKqCw?si=ePXvstCqVO7B_EIG)
- [Saber com Lógica — A soma binária](https://sabercomlogica.com/pt/a-soma-binaria/)
- [Fábrica de Noobs — Somadores e Subtratores](https://youtu.be/IQkYBmNVo_U?si=Emn0QLTxCkYRWWFc)
- [Global Science Network — Full Adder](https://www.gsnetwork.com/full-adder/)
- [Circuit Digest — Full Adder Circuit and its Construction](https://circuitdigest.com/tutorial/full-adder-circuit-theory-truth-table-construction)
-  meu irmão!
