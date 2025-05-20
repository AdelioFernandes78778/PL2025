# Título - TPC6: Recursivo Descendente para expressões aritméticas

## Autor
Adélio José Ferreira Fernandes, A78778

## Resumo
Neste TPC, é pedido que se desenvolva um analisador léxico e sintático em Python, utilizando o ply.lex e o ply.yacc. O analisador léxico identifica tokens como operadores e números inteiros, enquanto que o analisador sintático analisa, avalia e resolve expressões matemáticas que contêm operações básicas (adição, subtração, multiplicação e divisão) respeitando a precedência das mesmas.

Baseado nos materiais fornecidos na aula, cria um parser LL(1) recursivo descendente que reconheça expressões aritméticas e calcule o respetivo valor.

Exemplos de algumas frases:

2+3
67-(2+3*4)
(9-2)*(13-4)