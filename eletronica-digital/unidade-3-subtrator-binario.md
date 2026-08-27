# Unidade 3 — Eletrônica Digital: Subtrator Binário (Complemento de Dois)

## Contexto

Depois de fechar o somador completo de múltiplos bits (Unidade 2), o passo
seguinte foi construir a subtração binária em cima dele — sem criar um
circuito novo do zero, reaproveitando o mesmo `somador_completo` já
testado. Isso envolveu entender complemento de dois (por que inverter os
bits e somar 1 representa um número negativo), um caso especial que quebra
essa lógica se não houver bits suficientes, e como o mesmo mecanismo se
traduz em hardware com um único bit de controle.

## O problema: como subtrair usando só um somador

A ideia central: `A - B = A + (-B)`.
Em vez de construir um circuito de subtração separado, reaproveita-se o somador que já existe — só é preciso transformar `B` no seu valor negativo antes de somar.

**Por que é sempre `B` que é invertido, nunca `A`.** Só o segundo número (o
que está sendo subtraído) vira negativo; o primeiro (`A`) continua como
está. Exemplo fora de binário: `10 - 4` vira `10 + (-4) = 6` — não
`-10 + 4`, que seria outra conta (`4 - 10 = -6`, sinal trocado).

No código, isso significa que `complemento_de_dois()` é chamada sempre
com `B` como argumento, nunca com `A`:

```python
somador_completo(complemento_de_dois(B), A)
```

Inverter o argumento errado foi um dos erros que cometi ao escrever isso
pela primeira vez — o código rodava sem erro de sintaxe, mas calculava
`B - A` com o sinal trocado, em vez de `A - B`.

## Complemento de dois — revisão rápida

O Complemento de dois de um número X, em N bits é definido como: Comp2 = 2^N - X   -> complemento de dois é igual a dois elevado à n bits de um número x.
Uma forma de representar os números negativos em binário é com o método de Complemento de Dois.
O método se constitui na aritimética modular: em valor de 4 bits, o seu valor máximo é 1111 e o próximo valor seguinte a é 0000.
Para a representação negativa, devemos então inverter todos os bits de seu número e somar 1 após a inversão.

### Complemento de um (inverter os bits)

Complemento de um é só a primeira metade do processo: inverter cada bit do
número (todo `0` vira `1`, todo `1` vira `0`), sem somar nada ainda.

```python
for i in range(0, len(B)):
    bit_B = int(B[i])
    inverte = 1 - bit_B   # 1-0=1 (vira 1) / 1-1=0 (vira 0)
    comp_dois.append(inverte)
```

Sozinho, o complemento de um já tem um problema conhecido: o zero tem duas
representações diferentes (`0000` e `1111`, em 4 bits) — é o "zero
duplicado". Isso desperdiça um padrão de bits que poderia representar outro
número, e é o motivo de existir o passo seguinte (complemento de dois).

### Por que precisa somar 1 (complemento de dois)

Somar 1 depois de inverter os bits resolve o problema do zero duplicado:
testando com zero, em 4 bits, `0000` complemento de um vira `1111`; somando
1, `1111 + 1 = 10000`, que estoura os 4 bits e sobra `0000` de novo — ou
seja, o "zero negativo" colapsa no mesmo padrão do "zero positivo", sem
desperdiçar nenhum padrão de bits.

Matematicamente, complemento de um de `X` é `(2^N - 1) - X` (o máximo menos
X); somando 1, chega em `2^N - X`, que é exatamente a definição de
complemento de dois usada acima. É esse `+1` que transforma "quase
funciona" em "funciona de verdade".

## O caso especial: 2^(N-1)

O complemento de dois, em N bits, consegue representar números negativos até um
certo limite. O valor `2^(N-1)` é especial: ele é seu próprio complemento de dois
— ou seja, invertê-lo e somar 1 devolve o mesmo padrão de bits de novo, em vez de
um valor negativo diferente.

Exemplo com N=3 bits: `2^(3-1) = 4`. Em binário, `4 = 100`.

```
Complemento de um (inverte): 100 -> 011
Complemento de dois (+1):    011 + 1 = 100
```

Voltou para o mesmo valor. Isso não é bug — é consequência direta de `4 + 4 = 8`,
e `8` em 3 bits "estoura e vira 0" (a mesma lógica da roda de números / aritmética
modular). Nesse sistema de 3 bits, `4` e `-4` acabam representados pelo mesmo
padrão de bits.

Isso vira um problema real de verdade quando `B` (o número a ser invertido) tem
exatamente N bits e vale exatamente `2^(N-1)` — foi o que aconteceu no meu código
com `B = 100` (4 em decimal, 3 bits): o complemento de dois não mudava, e a
subtração dava resultado errado.

**A solução:** usar mais bits do que o mínimo necessário para representar os
números. No código, isso é o `bits_de_folga = max(len(A), len(B)) + 1` — sempre
garante pelo menos 1 bit a mais do que o necessário, o que "empurra" qualquer
valor para longe do ponto `2^(N-1)` daquele tamanho específico.

## Como o hardware faz isso com um único bit de controle

Um único bit de controle (aqui chamado `sub`) transforma um somador comum
em somador/subtrator combinado, ligado em dois pontos do mesmo circuito.

**Ponto 1 — porta XOR na frente de cada bit de B.** Cada bit de `B` passa
por uma porta XOR junto com o bit `sub`, antes de entrar no somador:

- `sub = 0` (modo soma): `bit_B XOR 0 = bit_B` — o bit passa sem alteração.
- `sub = 1` (modo subtração): `bit_B XOR 1 = NOT bit_B` — o bit é invertido.

É essa porta XOR que faz o papel do "complemento de um" (inverter os bits)
que a função `complemento_de_dois()` faz em software com um laço `for`.

**Ponto 2 — o mesmo `sub` alimenta o carry-in da posição 0.** Até agora, o
carry-in da primeira posição (a mais à direita) sempre foi fixo em `0`,
porque não existe posição anterior de verdade. No circuito somador/
subtrator, esse fio deixa de ser fixo e passa a ser ligado ao próprio bit
`sub`.

Isso funciona porque um carry-in de `1` na posição 0, dentro da fórmula do
somador (`total = bit_A + bit_B + carry`), é matematicamente idêntico a
somar `1` separadamente ali — o somador não sabe (nem precisa saber) se
aquele `1` veio de outra posição ou foi ligado direto por um fio de
controle. É por isso que o `+1` do complemento de dois não exige nenhum
somador extra em hardware: ele é "emprestado" do carry-in que já existia.

**Resumo do circuito de 1 bit:**

```
        sub ──┬─────────────────────────┐
              │                         │
   B ────► XOR (inverte se sub=1)       │
              │                         │
              ▼                         ▼
        Somador Completo (A, B', carry-in = sub)
              │
              ▼
         Sum, Carry-out
```

O `Carry-out` de cada posição continua alimentando o `Carry-in` da próxima,
exatamente como no somador de múltiplos bits do dia anterior — a única
mudança é que a primeira posição da cadeia recebe `sub` em vez de `0` fixo,
e todos os bits de `B` passam pela porta XOR antes de entrar.

Com `sub=0`, o circuito inteiro se comporta como um somador comum (soma
normal). Com `sub=1`, o mesmo circuito calcula `A - B`, sem nenhuma peça
extra além das portas XOR e do fio de controle redirecionado.

## O código

### somador_completo(A, B) — reaproveitado do dia anterior

```python
def somador_completo(A, B):
    # Sum = A xor B xor Cin
    # Cout = AB + BCin + ACin

    resultado = []
    carry = 0
    novo_A = A[:]
    novo_B = B[:]  # criar cópias das listas evita alterar a lista original
    diferenca_tamanho = len(novo_A) - len(novo_B)

    if len(novo_A) > len(novo_B):  # igualando tamanho das listas
        for i in range(diferenca_tamanho):
            novo_B.insert(0, 0)
    elif len(novo_B) > len(novo_A):
        for i in range(abs(diferenca_tamanho)):
            novo_A.insert(0, 0)

    # total = A + B + carry (resulta em decimal)
    # bit resultado (unidade) -> total % 2 "quanto fica" (analogia com base 10: 42%10=2 -> unidade, fica)
    # carry out (decimal)     -> total // 2 "quanto sobe" (analogia com base 10: 42//10=4 -> dezena, "não cabe ali", sobe)

    for i in range(-1, -len(novo_A) - 1, -1):  # do último valor da lista até o primeiro, passo -1
        bit_A = int(novo_A[i])
        bit_B = int(novo_B[i])
        total = bit_A + bit_B + carry
        resultado.append(total % 2)
        carry = total // 2

    if carry > 0:  # carry sobrando após a última iteração vira o bit mais significativo
        resultado.append(carry)

    resultado.reverse()  # construída do menos significativo pro mais significativo — inverte pra ordem de leitura normal
    return resultado
```

### complemento_de_dois(B)

```python
def complemento_de_dois(B):
    B = B[:]  # cópia, para não alterar o B original
    comp_dois = []
    for i in range(0, len(B)):
        bit_B = int(B[i])
        inverte = 1 - bit_B  # complemento de um: inverte cada bit
        comp_dois.append(inverte)
    resultado = somador_completo(comp_dois, [1])  # soma 1 ao invertido -> complemento de dois
    return resultado
```

### subtrator_completo(A, B)

```python
def subtrator_completo(A, B):
    A = A[:]
    B = B[:]
    bits_de_folga = max(len(A), len(B)) + 1  # margem para evitar o caso especial 2^(N-1)

    while len(A) < bits_de_folga:
        A.insert(0, 0)
    while len(B) < bits_de_folga:
        B.insert(0, 0)

    resultado = somador_completo(complemento_de_dois(B), A)  # A + (-B)
    return resultado[-bits_de_folga:]  # descarta o carry extra que sobra à esquerda


A = ['1', '0', '1', '0']
B = ['1', '0', '0']
print(somador_completo(A, B))     # [1, 1, 1, 0]  -> 10 + 4 = 14
print(subtrator_completo(A, B))   # [0, 0, 1, 1, 0] -> 10 - 4 = 6
```

## Erros que apareci ao longo do caminho (e o que aprendi com eles)

- `.insert()` sem a proteção de cópia — chamou `.insert()` diretamente em `A` e `B` dentro de `subtrator_completo`, alterando as listas originais fora da função (antes de adicionar `A = A[:]` e `B = B[:]`).
- Chamada de função sem parênteses — `somador_completo(complemento_de_dois, B)` passou a função `complemento_de_dois` em si (sem chamar), em vez de `complemento_de_dois(A)`. Deu `TypeError: 'function' object is not subscriptable`.
- Argumento no formato errado — `somador_completo(comp_dois, 1)` passou o número `1` sozinho, quando `somador_completo` esperava uma lista (`[1]`).
- Subtração de tipos incompatíveis — `1 - nums` tentando subtrair de uma string (`nums` vinha de `A` sem conversão com `int()`), gerando `TypeError: unsupported operand type(s) for -: 'int' and 'str'`.
- Argumento invertido na fórmula do complemento de dois — `complemento_de_dois(A)` em vez de `complemento_de_dois(B)`, calculando `-A + B` em vez de `A - B` (resultado com sinal trocado).
- `max()` com parênteses errados — `max(len(A), len(B) + 1)` aplicava o `+1` só a `len(B)`, em vez de aplicar ao resultado do `max()` inteiro.
- `.append()` em vez de `.insert()`, com argumentos errados — `A.append(0, 0)` (dois problemas: `.append()` só aceita um argumento, e insere no final, não no início).
- Fatiamento com índices errados pra remover o carry extra — tentativas com `[:-5]` e `[-5:-1]` antes de chegar em `[-bits_de_folga:]`, cada uma cortando a parte errada da lista.
- O caso especial do `2^(N-1)` — `B = 100` (4 em 3 bits) sendo seu próprio complemento de dois, fazendo a subtração dar resultado errado até adicionar o bit de folga.

## Materiais de apoio

- https://youtu.be/iEoQg52G1bA?si=-DulHG7SGSmB2IOD - Emmanuel Andrade - Somador-Subtrator
- https://eaulas.usp.br/portal/video?idItem=7720 - eaulas USP - Módulo Operações Aritméticas
- https://pt.wikipedia.org/wiki/Aritm%C3%A9tica_modular - Aritimética Modular (Wikipedia)
- https://eaulas.usp.br/portal/video.action?idItem=7738 - eaulas USP - Subtratores
- https://portaldaobmep.impa.br/index.php/modulo/ver?modulo=63&tipo=7 - IMPA - módulo
- https://embarcados.com.br/sinal-e-overflow-no-mips/ - Embarcados - Como funciona sinal e overflow no MIPS
