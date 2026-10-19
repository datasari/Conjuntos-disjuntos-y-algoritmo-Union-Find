# Deduplicación de registros con Union-Find

## Descripción

Este proyecto tiene como objetivo identificar registros duplicados en diferentes conjuntos de datos, incluso cuando la información está escrita de forma diferente.

Para ello, se implementa la estructura de datos **Union-Find**, que permite agrupar registros que corresponden a una misma entidad. El programa utiliza técnicas de normalización de texto, comparación por similitud y bloqueo de registros para identificar posibles duplicados de manera eficiente.

## Dataset

El proyecto utiliza diferentes conjuntos de datos para probar el proceso de deduplicación:

- **FEBRL2:** 
- **FEBRL4B:** 
- **Restaurantes:**
- **Consumidores:**

Los archivos de datos se encuentran en la carpeta `datos/` del proyecto.

## Tecnologías

- **Lenguaje de programación:** Python.
- **Estructura de datos:** Union-Find.
- **Módulos utilizados:** `csv`, `os` y `time`.
- **Herramientas adicionales:** Git y GitHub para el control de versiones y el trabajo colaborativo.

## Implementación

El proyecto se desarrolla mediante los siguientes componentes:...

## Ejecución

1. Clonar el repositorio.
2. Abrir la carpeta del proyecto en el entorno de desarrollo.
3. Verificar que los archivos de código y la carpeta `datos/` estén ubicados correctamente.
4. Ejecutar el programa principal:

```bash
python main.py
```

5. Seleccionar en el menú el conjunto de datos que se desea procesar.
6. Consultar los resultados en la consola y los archivos generados en la carpeta `resultados/`.

Para ejecutar las pruebas automatizadas:

```bash
python pruebas.py
```

Para realizar el experimento de comparación entre todos los pares y el método por bloques:

```bash
python experimento.py
```

## Resultados

Según las pruebas documentadas del proyecto, se obtuvieron los siguientes resultados:

- **Pruebas automatizadas:**
- **Dataset FEBRL2:** 
- **Comparación mediante bloques:** 
- **Archivos de salida:** 

Los resultados muestran que la combinación de Union-Find, la similitud textual y el bloqueo permite identificar duplicados y reducir la cantidad de comparaciones necesarias.

## Autores

- Veronica Roca Moreno
- Sara Gaviria Giraldo
- Valentina Castaño Saldarriaga
- Enrique Almanza Saucedo

**Institución:** Instituto Tecnológico Metropolitano (ITM)

**Asignatura:** Estructuras de Datos
