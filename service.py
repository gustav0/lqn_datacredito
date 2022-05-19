import json

from lib.client import DataCreditoClient


def handler(event, context):
    service = event.get("service")
    data = event.get("data", None)

    client = DataCreditoClient()

    map_services = {"consultar_historial": "consultar_hc2"}

    if service not in map_services:
        return {"error": True, "message": "Ningun servicio utilizado"}

    result = getattr(client, map_services[service])(data)
    return json.dumps(result.dict())
