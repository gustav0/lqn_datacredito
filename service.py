from lib import client
from lqn_soap_datacredito.utils import lqn_datacredito_client

data_credito_client = lqn_datacredito_client()

consultar_hc2 = data_credito_client.consultar_hc2(
    {
        "clave": "02ZOG",
        "identificacion": "7254173",
        "primerApellido": "FONTECHA",
        "producto": "64",
        "tipoIdentificacion": "1",
        "usuario": "900986913",
    }
)

print(consultar_hc2.dict())


# def handler(event, context):
#     client = lqn_datacredito_client()
#     service = event.get("service")
#     data = event.get("data", None)
#     result = {"error": True, "message": "Ningun servicio utilizado"}
    
#     result = client.consultar_hc2(data)
#     return result


# data = {
#         "clave": "02ZOG",
#         "identificacion": "7254173",
#         "primerApellido": "FONTECHA",
#         "producto": "64",
#         "tipoIdentificacion": "1",
#         "usuario": "900986913",
# }

# resultado = handler(data, none)

# print(resultado.dict())