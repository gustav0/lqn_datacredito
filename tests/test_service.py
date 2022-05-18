import json
import random

import pytest

from service import handler

DATA_CLIENTE= {
    "clave": "02ZOG",
    "identificacion": "9865790",
    "primerApellido": "ARANGO",
    "producto": "64",
    "tipoIdentificacion": "1",
    "usuario": "900986913",
}

CONSULTAR_CLIENTE ={
    "service": "consultar_historial",
    "data":DATA_CLIENTE
}

    
def test_query_response_identification_not_exist():
    """Consultar historial crediticio del cliente
    """
    consultar = CONSULTAR_CLIENTE.copy()
    consultar["data"] = {**consultar["data"] , "identificacion":"106148792"}
    response= handler(
        consultar,
        None,
    )
    response = json.loads(response)
    assert response["Informes"]["Informe"]["@respuesta"] == "09"
    
def test_query_response_identification_exist():
    """Consultar historial crediticio del cliente
    """
    response= handler(
        CONSULTAR_CLIENTE,
        None,
    )
    response = json.loads(response)
    assert response["Informes"]["Informe"]["@respuesta"] == "13"

def test_check_send_empty_random_fields():
    """Valida la excepción cuando falta un campo 
    """
    consultar = CONSULTAR_CLIENTE.copy()
    delete_field = random.choice(list(DATA_CLIENTE.keys()))
    consultar["data"].pop(delete_field)
    
    with pytest.raises(Exception) as e_info:
        handler(
            consultar,
            None,
        )
        
    assert "Campos requeridos no encontrados" in str(e_info.value)  

