import os

from union_find import UnionFind
from registros import Registro, normalizar, leer_registros
from similitud import bigramas, dice, similitud
from bloques import clave, armar_bloques
from bloques import pares_por_bloques, todos_los_pares
from deduplicador import Deduplicador
from evaluacion import entidad, pares_de, evaluar
from configuracion import DATASETS

os.chdir(os.path.dirname(os.path.abspath(__file__)))

bien = 0
mal = 0


def revisar(nombre, condicion):
    global bien, mal
    if condicion:
        bien += 1
    else:
        mal += 1
        print("❌", nombre)


def probar_union_find():
    uf = UnionFind(6)
    revisar("empiezan 6 conjuntos", uf.count() == 6)
    revisar("union nueva", uf.union(0, 1))
    revisar("union repetida", not uf.union(1, 0))
    uf.union(2, 3)
    uf.union(1, 3)
    revisar("conectados por transitividad", uf.connected(0, 2))
    revisar("no conectados", not uf.connected(0, 5))
    revisar("quedan 3 conjuntos", uf.count() == 3)
    revisar("tamaño del grupo", uf.size(3) == 4)
    revisar("makeSet", uf.makeSet() == 6 and uf.count() == 4)
    cadena = UnionFind(5)
    cadena.parent = [1, 2, 3, 4, 4]
    revisar("find de la cadena", cadena.find(0) == 4)
    revisar("compresión de caminos", cadena.parent == [4, 4, 4, 4, 4])
    grupos = uf.grupos()
    revisar("grupos", sorted(len(g) for g in grupos) == [1, 1, 1, 4])
    print("✅ union_find.py")


def probar_registros():
    texto = normalizar("  Jac-ob  O'Neil ")
    revisar("normalizar", texto == "jac ob o neil")
    revisar("vacío", normalizar("Unknown") == "")
    r = Registro(0, "a", {"nombre": "ana", "ciudad": "bello"})
    revisar("valor", r.valor("ciudad") == "bello")
    revisar("texto", str(r) == "a: ana | bello")
    regs = leer_registros("datos/restaurantes.tsv", "id",
                          {"name": 1, "phone": 1}, "\t")
    revisar("lee el tsv", len(regs) == 864)
    revisar("posiciones", regs[10].posicion == 10)
    revisar("primer restaurante", regs[0].valor("name")
            == "arnie morton s of chicago")
    print("✅ registros.py")


def probar_similitud():
    revisar("bigramas", bigramas("casa") == ["ca", "as", "sa"])
    revisar("iguales", dice("jacob", "jacob") == 1.0)
    revisar("distintos", dice("ab", "cd") == 0.0)
    revisar("night y nacht", dice("night", "nacht") == 0.25)
    revisar("una letra", dice("a", "ab") == 0.0)
    r1 = Registro(0, "a", {"n": "ana", "c": ""})
    r2 = Registro(1, "b", {"n": "ana", "c": "bello"})
    valor = similitud(r1, r2, {"n": 1, "c": 1})
    revisar("ignora vacíos", valor == 1.0)
    r3 = Registro(2, "c", {"n": "ana", "c": "itagui"})
    r4 = Registro(3, "d", {"n": "ana", "c": "bello"})
    revisar("pesos", similitud(r3, r4, {"n": 3, "c": 1}) == 0.75)
    print("✅ similitud.py")


def probar_bloques():
    regs = [Registro(0, "a", {"x": "1", "y": "p"}),
            Registro(1, "b", {"x": "1", "y": "q"}),
            Registro(2, "c", {"x": "2", "y": "p"}),
            Registro(3, "d", {"x": "", "y": "p"})]
    revisar("clave vacía", clave(regs[3], ["x"]) == "")
    revisar("clave doble", clave(regs[0], ["x", "y"]) == "1|p")
    bloques = armar_bloques(regs, ["x"])
    revisar("bloques", bloques == {"1": [0, 1], "2": [2]})
    pares = pares_por_bloques(regs, [["x"], ["y"], ["x"]])
    esperados = [(0, 1), (0, 2), (0, 3), (2, 3)]
    revisar("pares sin repetir", pares == esperados)
    revisar("todos los pares", len(todos_los_pares(regs)) == 6)
    print("✅ bloques.py")


def probar_deduplicador():
    regs = [Registro(0, "rec-1-org", {"n": "jacob lanyon"}),
            Registro(1, "rec-1-dup-0", {"n": "jacob lanyln"}),
            Registro(2, "rec-1-dup-1", {"n": "jaco lanyln"}),
            Registro(3, "rec-2-org", {"n": "sarah bruhn"})]
    dedup = Deduplicador(regs, {"n": 1}, 0.8)
    dedup.procesar([(0, 1), (1, 2), (0, 2), (0, 3)])
    revisar("transitividad", dedup.uf.connected(0, 2))
    revisar("se salta el par ya unido", dedup.saltados == 1)
    revisar("comparaciones", dedup.comparaciones == 3)
    revisar("grupos", dedup.grupos_duplicados() == [[0, 1, 2]])
    revisar("sobrantes", dedup.registros_sobrantes() == 2)
    revisar("entidad", entidad("rec-712-dup-0") == "712")
    esperados = {(0, 1), (0, 2), (1, 2)}
    revisar("pares de", pares_de([[0, 1, 2]]) == esperados)
    resultado = evaluar(regs, [[0, 1]])
    revisar("evaluar", resultado == (3, 1, 1, 1.0, 1 / 3))
    print("✅ deduplicador.py y evaluacion.py")


def probar_datasets():
    for nombre in ["febrl2", "febrl4b"]:
        datos = DATASETS[nombre]
        regs = leer_registros(datos["archivo"], datos["id"],
                              datos["pesos"], datos["separador"])
        dedup = Deduplicador(regs, datos["pesos"], datos["umbral"])
        dedup.procesar(pares_por_bloques(regs, datos["claves"]))
        resultado = evaluar(regs, dedup.grupos_duplicados())
        revisar(f"{nombre} precisión", resultado[3] == 1.0)
        revisar(f"{nombre} exhaustividad", resultado[4] > 0.99)
    print("✅ datasets febrl")


probar_union_find()
probar_registros()
probar_similitud()
probar_bloques()
probar_deduplicador()
probar_datasets()
print(f"{bien} bien, {mal} mal")
