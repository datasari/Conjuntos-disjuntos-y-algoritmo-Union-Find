import os
import time

from configuracion import DATASETS
from registros import leer_registros
from bloques import pares_por_bloques
from deduplicador import Deduplicador
from evaluacion import evaluar

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def deduplicar(nombre):
    datos = DATASETS[nombre]
    inicio = time.time()
    registros = leer_registros(datos["archivo"], datos["id"],
                               datos["pesos"], datos["separador"])
    pares = pares_por_bloques(registros, datos["claves"])
    dedup = Deduplicador(registros, datos["pesos"], datos["umbral"])
    dedup.procesar(pares)
    segundos = time.time() - inicio
    grupos = dedup.grupos_duplicados()

    print(f"\n--- {nombre} ---")
    print(f"Registros leídos:       {len(registros)}")
    print(f"Pares candidatos:       {len(pares)}")
    print(f"Comparaciones hechas:   {dedup.comparaciones}")
    print(f"Pares que ya estaban unidos: {dedup.saltados}")
    print(f"Entidades distintas:    {dedup.uf.count()}")
    print(f"Grupos con duplicados:  {len(grupos)}")
    print(f"Registros sobrantes:    {dedup.registros_sobrantes()}")
    print(f"Tiempo:                 {segundos:.2f} s")

    for grupo in grupos[:3]:
        print(f"\nGrupo de {len(grupo)} registros:")
        for posicion in grupo:
            print("  ", registros[posicion])

    if datos["verdad"]:
        resultado = evaluar(registros, grupos)
        reales, encontrados, aciertos = resultado[:3]
        precision, exhaustividad = resultado[3:]
        print(f"\nPares duplicados reales:   {reales}")
        print(f"Pares encontrados:         {encontrados}")
        print(f"Aciertos:                  {aciertos}")
        print(f"Precisión:                 {precision:.3f}")
        print(f"Exhaustividad:             {exhaustividad:.3f}")

    os.makedirs("resultados", exist_ok=True)
    ruta = f"resultados/{nombre}_grupos.csv"
    dedup.guardar(ruta)
    print(f"\nGrupos guardados en {ruta}")


def menu():
    nombres = list(DATASETS.keys())
    opcion = ""
    while opcion != "0":
        print("\n=== Deduplicación de registros con Union-Find ===")
        for i in range(len(nombres)):
            print(f"{i + 1}. {nombres[i]}")
        print(f"{len(nombres) + 1}. Todos")
        print("0. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "0":
            print("Hasta luego")
        elif opcion == str(len(nombres) + 1):
            for nombre in nombres:
                deduplicar(nombre)
        elif opcion.isdigit() and 1 <= int(opcion) <= len(nombres):
            deduplicar(nombres[int(opcion) - 1])
        else:
            print("Opción no válida")


if __name__ == "__main__":
    menu()
