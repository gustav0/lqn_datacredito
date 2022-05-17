import os
import json


def lqn_datacredito_client():
    os.environ["DATACREDITO_SETTINGS_MODULE"] = "lqn_soap_datacredito.settings"

    try:
        from lib.client import DataCreditoClient
    except:
        raise Exception("No fue posible cargar el modulo de datacredito")

    return DataCreditoClient()


def pretty_dict(self, **kwargs):
    return json.dumps(self.dict(**kwargs), indent=2)

