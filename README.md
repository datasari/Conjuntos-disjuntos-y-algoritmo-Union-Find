# Deduplicación de registros con Union-Find

## Descripción

Este proyecto tiene como objetivo identificar registros duplicados en diferentes conjuntos de datos, incluso cuando la información está escrita de forma diferente: «jacob lanyon» y «jacob lanyln», o «second street grille» y «second street grill». Si nadie limpia esos registros, se cuentan clientes de más, se mandan correos repetidos y los análisis salen inflados.

Para ello, se implementa la estructura de datos **Union-Find**, que permite agrupar registros que corresponden a una misma entidad. El programa utiliza técnicas de normalización de texto, comparación por similitud y bloqueo de registros para identificar posibles duplicados de manera eficiente. Cada registro es un elemento de Union-Find; cuando dos registros se parecen lo suficiente se unen sus conjuntos, y la transitividad hace el resto: si A se parece a B y B se parece a C, A, B y C quedan en el mismo grupo aunque A y C no se hayan comparado.

## Dataset

El proyecto utiliza diferentes conjuntos de datos para probar el proceso de deduplicación:

- **FEBRL2** (`febrl_dataset2.csv`, 5000 registros): personas con copias que tienen errores de digitación. Viene de FEBRL (Australian National University), tomado del repositorio de la librería [recordlinkage](https://github.com/J535D165/recordlinkage/tree/master/recordlinkage/datasets/febrl) (`dataset2.csv`). Trae la respuesta correcta en `rec_id` (`rec-712-org`, `rec-712-dup-0`…), así que sirve para medir la precisión.
- **FEBRL4B** (`febrl_dataset4b.csv`, 5000 registros): de la misma fuente ([recordlinkage](https://github.com/J535D165/recordlinkage/tree/master/recordlinkage/datasets/febrl), `dataset4b.csv`), pero ninguna persona se repite. Es un control: debe dar 0 grupos.
- **Restaurantes** (`restaurantes.tsv`, 864 registros): restaurantes de las guías Fodor's y Zagat juntas, tomado del [Hasso Plattner Institute](https://hpi.de/naumann/projects/repeatability/datasets/restaurants-dataset.html). Tiene duplicados reales entre las dos guías: la fuente reporta 112.
- **Consumidores** (`consumidores.csv`, 2000 registros): tomado del repositorio [Customer-Data-Deduplication-Pipeline](https://github.com/hiteshkumawat101/Customer-Data-Deduplication-Pipeline/blob/main/merged_consumers.csv) (`merged_consumers.csv`). Tiene homónimos (mismo nombre, otra persona), que no deben unirse.

Los archivos de datos se encuentran en la carpeta `datos/` del proyecto.

## Tecnologías

- **Lenguaje de programación:** Python 3.
- **Estructura de datos:** Union-Find (unión por rango y compresión de caminos).
- **Módulos utilizados:** `csv`, `os` y `time`, todos de la librería estándar. No se usa pandas ni librerías de deduplicación: la estructura y la comparación están hechas desde cero.
- **Herramientas adicionales:** Git y GitHub para el control de versiones y el trabajo colaborativo.

## Implementación

El proyecto se desarrolla mediante los siguientes componentes:

| Archivo | Qué hace |
|---|---|
| `registros.py` | `Registro`, `normalizar` (minúsculas, sin signos) y `leer_registros` (CSV o TSV) |
| `configuracion.py` | Para cada dataset: archivo, columnas con su peso, claves de bloque y umbral |
| `union_find.py` | `UnionFind` con `makeSet`, `find` (con compresión de caminos), `union` (por rango), `connected`, `count`, `size` y `grupos` |
| `similitud.py` | Bigramas, coeficiente de Dice y similitud ponderada entre dos registros |
| `bloques.py` | Bloqueo: solo se comparan registros que comparten una clave exacta |
| `deduplicador.py` | `Deduplicador`: recorre los pares candidatos, une los parecidos y guarda los grupos |
| `evaluacion.py` | Precisión y exhaustividad contra la respuesta correcta de FEBRL |
| `main.py` | Menú para correr cada dataset |
| `experimento.py` | Compara todos los pares contra el bloqueo (tiempo y calidad) |
| `pruebas.py` | 42 pruebas automáticas de todos los archivos |

**Cómo funciona:**

1. Se lee cada fila y se normaliza el texto (`"  Jac-ob "` → `"jac ob"`).
2. **Bloqueo:** comparar todos contra todos son n(n−1)/2 pares (12 497 500 con 5000 registros). En vez de eso, solo se comparan los registros que comparten una clave exacta (el mismo documento, la misma fecha de nacimiento o el mismo apellido y código postal). Se hacen varias pasadas con claves distintas: un error de digitación en un campo no impide que coincidan en otro.
3. **Similitud:** el coeficiente de Dice sobre bigramas (pares de letras seguidas) da un número entre 0 y 1 por columna; se promedia con pesos (en restaurantes el nombre pesa 3).
4. **Union-Find:** si la similitud llega al umbral, `union(a, b)`. Si `a` y `b` ya estaban conectados, ni se comparan: la estructura ahorra trabajo.
5. Los conjuntos de más de un elemento son los grupos de duplicados.

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

Para realizar el experimento de comparación entre todos los pares y el método por bloques (tarda cerca de un minuto, porque compara todos los pares a propósito):

```bash
python experimento.py
```

## Resultados

Según las pruebas documentadas del proyecto, se obtuvieron los siguientes resultados:

- **Pruebas automatizadas:** 42 pruebas, todas correctas («42 bien, 0 mal»).
- **Dataset FEBRL2:** 5000 registros, 426 grupos de duplicados y 4007 entidades distintas. Precisión 1,000 (todas las uniones son correctas) y exhaustividad 0,992 (encontró 1918 de los 1934 pares duplicados). Tarda unos 0,15 s.
- **Controles:** FEBRL4B y Consumidores dan 0 grupos: el programa no se inventa duplicados, ni siquiera con homónimos. Restaurantes da 98 grupos.
- **Comparación mediante bloques:** con los primeros 1000 registros de FEBRL2, todos los pares hacen 499 492 comparaciones en unos 28 s; el bloqueo hace 69 en 0,02 s y pierde poco (exhaustividad 0,955 contra 0,970).
- **Archivos de salida:** `resultados/<dataset>_grupos.csv`, con una fila por registro duplicado (número de grupo, tamaño, id y registro).
- **Un falso positivo:** en Restaurantes, «cafe ritz carlton buckhead» y «dining room ritz carlton buckhead» quedaron en el mismo grupo. Son dos restaurantes del mismo hotel: comparten dirección, teléfono y casi todo el nombre, así que su similitud (0,87) pasa el umbral. Y como Union-Find es transitivo, esa sola unión equivocada junta los dos pares en un grupo de 4.

Los resultados muestran que la combinación de Union-Find, la similitud textual y el bloqueo permite identificar duplicados y reducir la cantidad de comparaciones necesarias.

## Autores

- Veronica Roca Moreno
- Sara Gaviria Giraldo
- Valentina Castaño Saldarriaga
- Enrique Almanza Saucedo

**Institución:** Instituto Tecnológico Metropolitano (ITM)

**Asignatura:** Estructuras de Datos
