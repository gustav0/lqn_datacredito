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

from lib import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOLICITUD_CAMPOS_REQUERIDOS = [
    "clave",
    "identificacion",
    "primerApellido",
    "producto",
    "tipoIdentificacion",
    "usuario",
]


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
            getattr(settings, "WSDL"),
            wsse=self.custom_signature(),
            transport=self.transport(),
        )

    def custom_signature(self) -> CustomSignature:
        signature = Signature(
            certfile=settings.CERTIFICATE_PATH,
            key_file=settings.KEY_PATH,
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
            settings.CERTIFICATE_PATH,
            settings.KEY_PATH,
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
            settings.USERNAME,
            settings.PASSWORD,
            timestamp_token=timestamp_token,
        )

    def consultar_hc2(self, solicitud: dict) -> DataCreditoResponse:
        self.agregar_user_password(solicitud)
        self.validar_campo_solicitud(solicitud)

        return DataCreditoResponse(
            raw_body=self.client.service.consultarHC2(
                solicitud=solicitud,
                _soapheaders=None,
            ),
        )

    def agregar_user_password(self, solicitud: dict) -> None:
        solicitud.update(
            {"usuario": settings.USERNAME.split("-")[1], "clave": settings.SHORT_PASSWORD, "producto": "64"}
        )

    def validar_campo_solicitud(self, solicitud):
        campos_requeridos = set(SOLICITUD_CAMPOS_REQUERIDOS)
        campos_solicitud = set(solicitud.keys())
        if campos_requeridos - campos_solicitud:
            raise Exception("Campos requeridos no encontrados")
