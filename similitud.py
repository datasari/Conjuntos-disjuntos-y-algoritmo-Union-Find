def bigramas(texto):
    pares = []
    for i in range(len(texto) - 1):
        pares.append(texto[i:i + 2])
    return pares


def dice(a, b):
    if a == b:
        return 1.0
    pares_a = bigramas(a)
    pares_b = bigramas(b)
    if len(pares_a) == 0 or len(pares_b) == 0:
        return 0.0
    disponibles = list(pares_b)
    comunes = 0
    for par in pares_a:
        if par in disponibles:
            disponibles.remove(par)
            comunes += 1
    return 2 * comunes / (len(pares_a) + len(pares_b))


def similitud(r1, r2, pesos):
    suma = 0
    total = 0
    for columna in pesos:
        a = r1.valor(columna)
        b = r2.valor(columna)
        if a != "" and b != "":
            suma += pesos[columna] * dice(a, b)
            total += pesos[columna]
    if total == 0:
        return 0.0
    return suma / total