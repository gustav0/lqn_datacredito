import datetime
import json
import os
from dataclasses import dataclass
from html import unescape

import xmltodict
from requests import Session
from zeep import Client, Transport
from zeep.wsse.signature import Signature
from zeep.wsse.username import UsernameToken
from zeep.wsse.utils import WSU
from zeep.exceptions import Fault

from lib.conf import ENVIRONMENT_VARIABLE, settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



try:
    
    certfile_path = os.path.join(BASE_DIR, getattr(settings, "CERTIFICATE_PATH"))
    key_file_path = os.path.join(BASE_DIR, getattr(settings, "KEY_PATH"))
    datacredito_username = getattr(settings, "DATACREDITO_USERNAME")
    datacredito_password = getattr(settings, "DATACREDITO_PASSWORD")
    # breakpoint()
except AttributeError:
    raise Exception(
        f"""
        Asegurese de agregar la variable de entorno {ENVIRONMENT_VARIABLE} con el PATH a su configuracion (ej: "lqn_datacredito.settings").
        En su archivo de configuracion agregue las constantes (CERTIFICATE_PATH, KEY_PATH, DATACREDITO_USERNAME, DATACREDITO_PASSWORD)
        """
    )


class CustomSignature(object):
    def __init__(self, wsse_list):
        self.wsse_list = wsse_list

    def apply(self, envelope, headers):
        for wsse in self.wsse_list:
            envelope, headers = wsse.apply(envelope, headers)
        return envelope, headers

    def verify(self, _envelope):
        pass


@dataclass
class DataCreditoResponse:
    raw_body: str

    def dict(self) -> dict:
        json_resp = json.dumps(xmltodict.parse(unescape(self.raw_body)))
        return json.loads(json_resp)


class DataCreditoClient:
    def __init__(self) -> None:
        self.client = Client(
            getattr(settings, "DATACREDITO_WSDL_URL"),
            wsse=self.custom_signature(),
            transport=self.transport(),
        )

    def custom_signature(self) -> CustomSignature:
        signature = Signature(
            certfile=certfile_path,
            key_file=key_file_path,
        )

        return CustomSignature(
            [
                self.token_with_timestamp(),
                signature,
            ]
        )

    def transport(self) -> Transport:
        session = Session()

        session.verify = False

        session.cert = (
            certfile_path,
            key_file_path,
        )

        return Transport(session=session)

    def token_with_timestamp(self) -> UsernameToken:
        timestamp_token = WSU.Timestamp()
        today_datetime = datetime.datetime.today()
        expires_datetime = today_datetime + datetime.timedelta(minutes=360)

        timestamp_elements = [
            WSU.Expires(expires_datetime.strftime(getattr(settings, "EXPIRES_FORMAT"))),
            WSU.Created(today_datetime.strftime(getattr(settings, "EXPIRES_FORMAT"))),
        ]

        timestamp_token.extend(timestamp_elements)

        return UsernameToken(
            datacredito_username,
            datacredito_password,
            timestamp_token=timestamp_token,
        )

    def consultar_hc2(self, solicitud: dict) -> DataCreditoResponse:
        return DataCreditoResponse(
            raw_body=self.client.service.consultarHC2(
                solicitud=solicitud,
                _soapheaders=None,
            ),
        )


def capture_soap_error(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Fault as error:
            raise
            return render_soap_error(error, from_function=function.__name__)
        # except Exception as error:
        #     # raise
        #     print(traceback.format_exc())
        #     return build_reply_message(True, f"{type(error)}: {str(error)}", None, from_function=function.__name__)

    return wrapper