def clave(registro, columnas):
    partes = []
    for columna in columnas:
        valor = registro.valor(columna)
        if valor == "":
            return ""
        partes.append(valor)
    return "|".join(partes)


def armar_bloques(registros, columnas):
    bloques = {}
    for registro in registros:
        k = clave(registro, columnas)
        if k != "":
            if k not in bloques:
                bloques[k] = []
            bloques[k].append(registro.posicion)
    return bloques


def pares_por_bloques(registros, claves):
    vistos = set()
    pares = []
    for columnas in claves:
        bloques = armar_bloques(registros, columnas)
        for bloque in bloques.values():
            for i in range(len(bloque)):
                for j in range(i + 1, len(bloque)):
                    par = (bloque[i], bloque[j])
                    if par not in vistos:
                        vistos.add(par)
                        pares.append(par)
    return pares


def todos_los_pares(registros):
    pares = []
    for i in range(len(registros)):
        for j in range(i + 1, len(registros)):
            pares.append((i, j))
    return pares