from lqn_soap_datacredito.utils import lqn_datacredito_client

def handler(event, context):
    client = lqn_datacredito_client()
    service = event.get("service")
    data = event.get("data", None)
    result = {"error": True, "message": "Ningun servicio utilizado"}
    if service == "consultar_historial":
        result = client.consultar_hc2(data)
    return result


CONSULTA = {
    "service": "consultar_historial",
    "data":{
        "clave": "02ZOG",
        "identificacion": "7254173",
        "primerApellido": "FONTECHA",
        "producto": "64",
        "tipoIdentificacion": "1",
        "usuario": "900986913",
    }
}

resultado = handler(CONSULTA, None)

print(resultado.dict())