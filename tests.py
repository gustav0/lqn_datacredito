import json
from pprint import pprint

from service import handler

CONSULTA = {
    "service": "consultar_historial",
    "data": {
        "clave": "02ZOG",
        "identificacion": "6469739",
        "primerApellido": "ALFONSO",
        "producto": "64",
        "tipoIdentificacion": "1",
        "usuario": "900986913",
    },
}

resultado = handler(CONSULTA, None)
print(type(resultado))
pprint(json.loads(resultado))
