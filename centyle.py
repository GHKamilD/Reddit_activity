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
num_of_authors = len(data.values())
centyle = {}
i=100
check=0
suma = 0
i = 0
for number in data.values():
    suma += number
    if i==100: break
    else: i+=1
print(suma)
suma = 0
for number in data.values():
    suma += number
print(suma)
suma = 0
for number in data.values():
    suma+=number
    check+=1
    if check==num_of_authors//100:
        centyle[i] = suma
        suma = 0
        check = 0
        i-=1
print(centyle)