# Función de un generador
def numerosPares():
    for i in range(2,201):
        if i % 2 == 0:
            yield i
            print(i)

genPares = numerosPares()

for i in genPares:
    next(genPares)