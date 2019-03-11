numero = 5
b = round(numero/10)*10

entero = int(numero)
decimal = int(round((numero - entero)*100))

a = entero % 10

print(entero)
print(decimal)
print(a)

c = int(len(str(numero))) / 10
print(c)