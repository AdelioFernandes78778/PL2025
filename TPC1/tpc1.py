import sys

def somador_on_off(texto):
    soma = 0
    ativo = True
    numero_atual = ""
    resultado = []
    
    palavras = texto.split()
    
    for palavra in palavras:
        palavra_lower = palavra.lower()
        
        if "off" in palavra_lower:
            ativo = False
        elif "on" in palavra_lower:
            ativo = True
        
        numero = ""
        for char in palavra:
            if char.isdigit():
                numero += char
            else:
                if numero and ativo:
                    soma += int(numero)
                numero = ""
                
            if char == "=":
                resultado.append(f">> {soma}")
                
        if numero and ativo:
            soma += int(numero)
    
    resultado.append(f">> {soma}")
    
    print("\n".join(resultado))
    
if __name__ == "__main__":
    # Teste
    exemplo = "Hoje, 7 de Fevereiro de 2025, o professor de Processamento de Linguagens deu-nos este trabalho para fazer.=OfF\nE deu-nos 7= dias para o fazer... ON\nCada trabalho destes vale 0.25 valores da nota final!"
    print(exemplo)
    somador_on_off(exemplo)
