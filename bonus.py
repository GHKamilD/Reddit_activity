import ast
import statistics

def read_existing_data(filename):
    data = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            author, count = ast.literal_eval(line.strip())
            data[author] = count
    return data

filename = 'komentarze.txt'  # or 'posty.txt' for post data
data = read_existing_data(filename)
suma = 0
for number in data.values():
    suma += number
print(suma)
suma_pom = suma
suma = 0
i=0
for number in data.values():
    print(number)
    suma += number
    if i==30: break
    else: i+=1
print(suma/suma_pom)

