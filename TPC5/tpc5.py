import json
import ply.lex as lex
from datetime import datetime
import re
from decimal import Decimal, ROUND_HALF_UP


tokens = (
    'LISTAR',
    'MOEDA',
    'SELECIONAR',
    'ADICIONAR',
    'SAIR',
    'CODIGO',
    'NOME',
    'QUANTIDADE',
    'PRECO',
    'VALOR_MOEDA',
)

t_LISTAR = r'LISTAR'
t_SELECIONAR = r'SELECIONAR'
t_ADICIONAR = r'ADICIONAR'
t_SAIR = r'SAIR'
t_CODIGO = r'[A-Z][0-9]+'
t_NOME = r'\".*\"'
t_QUANTIDADE = r'[0-9]+'
t_PRECO = r'[0-9]+e[0-9]+c'
t_VALOR_MOEDA = r'(1|2|5|10|20|50)e|(1|2|5)c'

t_ignore = ' \n'

# Função para processar o token MOEDA
def t_MOEDA(t):
    r'MOEDA\s+((2|5|10|20|50)c|(1|2)e)(\s*,\s*((2|5|10|20|50)c|(1|2)e))*\.?'
    
    # Inicializar saldo
    saldo = 0

    # Processar moedas e calcular saldo
    for moeda in re.finditer(r'(?:(?P<cent>2|5|10|20|50)c|(?P<euro>1|2)e)', t.value):
        if moeda.lastgroup == "cent":
            saldo += int(moeda.group("cent"))
        else:
            saldo += int(moeda.group("euro")) * 100

    # Retorna o saldo como um token
    t.value = saldo
    return t

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def formatar_saldo(saldo):
    saldo_euro, saldo_cent = divmod(saldo, 100)
    return f"{saldo_euro}e{saldo_cent}c"

def selecionar_produto(codigo, saldo, stock):
    for produto in stock:
        if produto['cod'] == codigo:
            preco_produto = Decimal(produto['preco']) * 100  # Convertendo o preço para centimos
            if produto['quant'] > 0 and preco_produto <= saldo:
                produto['quant'] -= 1
                saldo -= preco_produto
                saldo = saldo.quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
                print(f"Pode retirar o produto dispensado \"{produto['nome']}\"")
                print(f"Saldo = {formatar_saldo(int(saldo))}")
            elif produto['quant'] == 0:
                print("Produto esgotado.")
            else:
                print("Saldo insuficiente para satisfazer o seu pedido")
                preco_euro, preco_cent = divmod(preco_produto, 100)
                print(f"Saldo = {formatar_saldo(int(saldo))}")
                print(f"Pedido = {preco_euro}e{int(preco_cent)}c")
            return saldo
    print("Produto inexistente.")
    return saldo

# Função para adicionar produto ao stock
def adicionar_produto(codigo, nome, quantidade, preco, stock):
    for produto in stock:
        if produto['cod'] == codigo:
            produto['quant'] += quantidade
            print(f"Adicionadas {quantidade} unidades de \"{nome}\" ao stock.")
            return
    novo_produto = {"cod": codigo, "nome": nome, "quant": quantidade, "preco": preco}
    stock.append(novo_produto)
    print(f"Produto \"{nome}\" adicionado ao stock.")

def calcular_troco(saldo):
    moedas = [200, 100, 50, 20, 10, 5, 2, 1]
    troco = []
    saldo_cent = saldo
    for moeda in moedas:
        quantidade, saldo_cent = divmod(saldo_cent, moeda)
        if quantidade > 0:
            if moeda >= 100:
                troco.append(f"{quantidade}x {moeda//100}e")
            else:
                troco.append(f"{quantidade}x {moeda}c")
    return ', '.join(troco)

# Função principal
def main():
    # Carregar dados do arquivo stock.json
    with open('TPC5/stock.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Obter o stock do arquivo JSON
    stock = data["stock"]

    # Obter a data atual e formatá-la
    data_atual = datetime.now().strftime('%Y-%m-%d')

    print(f"maq: {data_atual}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")

    saldo = 0  # Inicializa o saldo como zero

    while True:
        comando = input(">> ")
        lexer.input(comando)

        # Processa cada token do comando
        for tok in lexer:
            if tok.type == 'LISTAR':
                print("maq:")
                print("cod | nome | quantidade | preço")
                print("-" * 33)
                for produto in stock:
                    print(f"{produto['cod']} {produto['nome']} {produto['quant']} {produto['preco']}")
                print()
            elif tok.type == 'SELECIONAR':
                codigo = input("Código do produto: ")
                saldo = selecionar_produto(codigo, saldo, stock)
            elif tok.type == 'ADICIONAR':
                codigo = input("Código do produto: ")
                nome = input("Nome do produto: ")
                quantidade = int(input("Quantidade: "))
                preco = input("Preço (em centimos): ")
                adicionar_produto(codigo, nome, quantidade, preco, stock)
            elif tok.type == 'SAIR':
                if saldo > 0:
                    troco = calcular_troco(int(saldo))
                    print(f"maq: Pode retirar o troco: {troco}.")
                print("maq: Até à próxima")
                return
            elif tok.type == 'MOEDA':
                saldo += tok.value
                print(f"maq: Saldo = {formatar_saldo(saldo)}")
            else:
                print(f"Comando inválido: {tok.value}")

if __name__ == "__main__":
    main()
