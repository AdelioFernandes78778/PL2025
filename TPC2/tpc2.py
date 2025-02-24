import sys
import os
import re
import json

DELIMITER = ';'
OUTPUT_FILE = 'out/resultados.json'

if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

resultados = {
    'compositores': set(),  
    'distr': {},            
    'obras': {}             
}

with open(input_file, 'r', encoding='utf-8') as f:
    data = f.read()

# Regex to match full rows:
# Any line followed by 0 or more lines indented with 8 spaces
pattern = r'^(.*)(?:\n {8}(.*?))*$'

rows = re.findall(pattern, data, re.MULTILINE)

rows = rows[1:]

for i, row in enumerate(rows):
    full_row = "".join(row) 

    pattern = rf'({DELIMITER}")|("{DELIMITER})|({DELIMITER})'
    tokens = re.split(pattern, full_row)

    tokens = [t for t in tokens if t is not None and t != '']

    fields = []
    field = ""
    on = True

    for token in tokens:
        if token == f'{DELIMITER}"':
            fields.append(field)
            field = ""
            on = False
        elif token == f'"{DELIMITER}':
            fields.append(field)
            field = ""
            on = True
        elif token == f'{DELIMITER}':
            if on:
                fields.append(field)
                field = ""
            else:
                field += token
        else:
            field += token

    if field != "":
        fields.append(field)

    if len(fields) < 7:
        print(f"Row number {i + 1} has less than 7 fields")
        continue

    nome       = fields[0]
    periodo    = fields[3]
    compositor = fields[4]

    resultados['compositores'].add(compositor)
    resultados['distr'][periodo] = resultados['distr'].get(periodo, 0) + 1
    resultados['obras'][periodo] = resultados['obras'].get(periodo, []) + [nome]

# ordenar compositores
resultados['compositores'] = sorted(resultados['compositores'])

# ordenar obras
for periodo in resultados['obras']:
    resultados['obras'][periodo] = sorted(resultados['obras'][periodo])

# ficheiro output

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

print("Compositores:")
print(json.dumps(resultados['compositores'], indent=2, ensure_ascii=False))

print("\nDistribuição por período:")
print(json.dumps(resultados['distr'], indent=2, ensure_ascii=False))

print("\nObras por período:")
print(json.dumps(resultados['obras'], indent=2, ensure_ascii=False))

print(f"Processed {len(rows)} rows")