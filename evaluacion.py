def entidad(identificador):
    return identificador.split("-")[1]


def pares_de(grupos):
    pares = set()
    for grupo in grupos:
        for i in range(len(grupo)):
            for j in range(i + 1, len(grupo)):
                pares.add((grupo[i], grupo[j]))
    return pares


def grupos_reales(registros):
    por_entidad = {}
    for r in registros:
        e = entidad(r.identificador)
        if e not in por_entidad:
            por_entidad[e] = []
        por_entidad[e].append(r.posicion)
    return list(por_entidad.values())


def evaluar(registros, grupos):
    reales = pares_de(grupos_reales(registros))
    encontrados = pares_de(grupos)
    aciertos = len(reales & encontrados)
    if len(encontrados) == 0:
        precision = 1.0
    else:
        precision = aciertos / len(encontrados)
    if len(reales) == 0:
        exhaustividad = 1.0
    else:
        exhaustividad = aciertos / len(reales)
    return (len(reales), len(encontrados), aciertos, precision,
            exhaustividad)
