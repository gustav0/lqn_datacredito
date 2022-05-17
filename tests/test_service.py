import json

import pytest

from service import handler

CLIENTE = {

        "clave": "02ZOG",
        "identificacion": "72541735",
        "primerApellido": "FONTECHA",
        "producto": "64",
        "tipoIdentificacion": "1",
        "usuario": "900986913",
}

def pretty_dict(self, **kwargs):
    return json.dumps(self.dict(**kwargs), indent=2)

def test_check_send_all_fields():
    """Consultar historial crediticio del cliente
    """
    with pytest.raises(Exception) as e_info:
        # pass
        handler(
            {
                "service": "consultar_historial",
                "data": CLIENTE,
            },
            None
        )
        
    assert "Campos requeridos no encontrados" in str(e_info.value)
    
def test_check_send_all_fields2():
    """Consultar historial crediticio del cliente
    """
    result = handler(
        {
            "service": "consultar_historial",
            "data": CLIENTE,
        },
        None
    )
    result = json.loads(result)
    assert result["Informes"]["Informe"]["@respuesta"] == "09"

    

