import os
import time

from configuracion import DATASETS
from registros import leer_registros
from bloques import pares_por_bloques, todos_los_pares
from deduplicador import Deduplicador
from evaluacion import evaluar

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def medir(registros, pares, datos):
    inicio = time.time()
    dedup = Deduplicador(registros, datos["pesos"], datos["umbral"])
    dedup.procesar(pares)
    segundos = time.time() - inicio
    resultado = evaluar(registros, dedup.grupos_duplicados())
    return dedup.comparaciones, segundos, resultado[3], resultado[4]


def experimento():
    datos = DATASETS["febrl2"]
    todos = leer_registros(datos["archivo"], datos["id"],
                           datos["pesos"], datos["separador"])
    print("n     método           comparaciones  segundos  "
          "precisión  exhaustividad")
    for n in [250, 500, 1000]:
        registros = todos[:n]
        metodos = [
            ("todos los pares", todos_los_pares(registros)),
            ("bloques", pares_por_bloques(registros, datos["claves"])),
        ]
        for nombre, pares in metodos:
            comparaciones, segundos, precision, exhaustividad = medir(
                registros, pares, datos)
            print(f"{n:<5} {nombre:<16} {comparaciones:>13} "
                  f"{segundos:>9.2f} {precision:>10.3f} "
                  f"{exhaustividad:>14.3f}")
    n = len(todos)
    print(f"\nCon los {n} registros, todos los pares serían "
          f"{n * (n - 1) // 2} comparaciones.")


if __name__ == "__main__":
    experimento()