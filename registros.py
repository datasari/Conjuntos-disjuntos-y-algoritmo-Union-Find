import csv

VACIOS = ["", "unknown", "nan", "null", "none"]


class Registro:
    def __init__(self, posicion, identificador, campos):
        self.posicion = posicion
        self.identificador = identificador
        self.campos = campos

    def valor(self, columna):
        return self.campos[columna]

    def __str__(self):
        valores = []
        for columna in self.campos:
            valores.append(self.campos[columna])
        return f"{self.identificador}: " + " | ".join(valores)


def normalizar(texto):
    limpio = ""
    for letra in texto.lower():
        if letra.isalnum():
            limpio += letra
        else:
            limpio += " "
    limpio = " ".join(limpio.split())
    if limpio in VACIOS:
        return ""
    return limpio


def leer_registros(ruta, columna_id, columnas, separador=","):
    registros = []
    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo, delimiter=separador,
                                skipinitialspace=True)
        for fila in lector:
            campos = {}
            for columna in columnas:
                campos[columna] = normalizar(fila[columna])
            identificador = fila[columna_id].strip()
            registros.append(Registro(len(registros), identificador,
                                      campos))
    return registros
