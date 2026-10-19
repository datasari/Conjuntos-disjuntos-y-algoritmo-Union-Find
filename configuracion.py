PESOS_FEBRL = {
    "given_name": 1,
    "surname": 1,
    "street_number": 1,
    "address_1": 1,
    "suburb": 1,
    "postcode": 1,
    "date_of_birth": 1,
    "soc_sec_id": 1,
}

CLAVES_FEBRL = [
    ["soc_sec_id"],
    ["date_of_birth"],
    ["surname", "postcode"],
]

DATASETS = {
    "febrl2": {
        "archivo": "datos/febrl_dataset2.csv",
        "separador": ",",
        "id": "rec_id",
        "pesos": PESOS_FEBRL,
        "claves": CLAVES_FEBRL,
        "umbral": 0.6,
        "verdad": True,
    },
    "febrl4b": {
        "archivo": "datos/febrl_dataset4b.csv",
        "separador": ",",
        "id": "rec_id",
        "pesos": PESOS_FEBRL,
        "claves": CLAVES_FEBRL,
        "umbral": 0.6,
        "verdad": True,
    },
    "restaurantes": {
        "archivo": "datos/restaurantes.tsv",
        "separador": "\t",
        "id": "id",
        "pesos": {"name": 3, "address": 1, "city": 1, "phone": 1},
        "claves": [["phone"], ["name"], ["address"]],
        "umbral": 0.75,
        "verdad": False,
    },
    "consumidores": {
        "archivo": "datos/consumidores.csv",
        "separador": ",",
        "id": "consumer_id",
        "pesos": {"first_name": 1, "last_name": 1, "street": 1,
                  "city": 1, "zip": 1, "email": 1, "phone": 1},
        "claves": [["email"], ["phone"], ["last_name", "zip"],
                   ["first_name", "last_name"]],
        "umbral": 0.75,
        "verdad": False,
    },
}
