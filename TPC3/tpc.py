import sys
import re

def markdown_para_html(markdown):
    html = []
    linhas = markdown.split('\n')
    dentro_lista = False

    for linha in linhas:
        linha = linha.strip()

        # Cabeçalhos
        if linha.startswith('### '):
            html.append(f"<h3>{linha[4:]}</h3>")
        elif linha.startswith('## '):
            html.append(f"<h2>{linha[3:]}</h2>")
        elif linha.startswith('# '):
            html.append(f"<h1>{linha[2:]}</h1>")

        # Lista numerada
        elif re.match(r'\d+\.\s', linha):
            if not dentro_lista:
                html.append("<ol>")
                dentro_lista = True
            item = re.sub(r'^\d+\.\s', '', linha)
            html.append(f"<li>{item}</li>")
        else:
            if dentro_lista:
                html.append("</ol>")
                dentro_lista = False

            # Processa bold, itálico, links e imagens
            linha = re.sub(r'!\[([^\]]+)\]\(([^)]+)\)', r'<img src="\2" alt="\1"/>', linha)
            linha = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', linha)
            linha = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', linha)
            linha = re.sub(r'\*([^\*]+)\*', r'<i>\1</i>', linha)

            if linha:
                html.append(linha)

    if dentro_lista:
        html.append("</ol>")

    return '\n'.join(html)

# Exemplo de uso:
entrada = """# Cabeçalho
Este é um **texto em bold** e este é um *texto em itálico*.
1. Primeiro item
2. Segundo item
3. Terceiro item
Veja mais em [site oficial](http://www.example.com)
Veja a imagem: ![alt](http://www.imagem.com/img.png)
"""

saida = markdown_para_html(entrada)
print(saida)
