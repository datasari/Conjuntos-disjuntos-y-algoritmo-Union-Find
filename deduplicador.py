import csv

from union_find import UnionFind
from similitud import similitud


class Deduplicador:
    def __init__(self, registros, pesos, umbral):
        self.registros = registros
        self.pesos = pesos
        self.umbral = umbral
        self.uf = UnionFind(len(registros))
        self.comparaciones = 0
        self.saltados = 0

    def procesar(self, pares):
        for a, b in pares:
            if self.uf.connected(a, b):
                self.saltados += 1
            else:
                self.comparaciones += 1
                r1 = self.registros[a]
                r2 = self.registros[b]
                if similitud(r1, r2, self.pesos) >= self.umbral:
                    self.uf.union(a, b)
        return self.uf.count()

    def grupos_duplicados(self):
        duplicados = []
        for grupo in self.uf.grupos():
            if len(grupo) > 1:
                duplicados.append(grupo)
        duplicados.sort(key=len, reverse=True)
        return duplicados

    def registros_sobrantes(self):
        return len(self.registros) - self.uf.count()

    def guardar(self, ruta):
        with open(ruta, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["grupo", "tamano", "id", "registro"])
            numero = 1
            for grupo in self.grupos_duplicados():
                for posicion in grupo:
                    r = self.registros[posicion]
                    escritor.writerow([numero, len(grupo),
                                       r.identificador, str(r)])
                numero += 1
