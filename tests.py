import json
from pprint import pprint

from service import handler


CONSULTA = {
    "service": "consultar_historial",
    "data": {
        "identificacion": "6469739",
        "primerApellido": "ALFONSO",
        "tipoIdentificacion": "1",
    },
}

resultado = handler(CONSULTA, None)

# print(type(resultado))
# pprint(json.loads(resultado))
