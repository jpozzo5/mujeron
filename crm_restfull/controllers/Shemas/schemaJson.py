import json
import jsonschema
from jsonschema import validate
#FORMATO DEL JSON A RECIBIR en el endpoint.

class Shema:
    def __init__(self):
        self._SHEMA ={
                "phone":{"type": "string"},
                "mobile":{"type": "string"},
                "name":{"type": "string"},
                "email":{"type": "string"},
                "id_odoo_seller":{"type": "number"},
                "chanel_sell":{"type": "string"},
                "name_lead":{"type": "string"},
                "id_lead_todofull":{"type": "number"},
                "data_seller":{
                        "email_seller":{"type": "string"},
                        "name":{"type": "string"},
                        "phone":{"type": "string"},
                },
        }

    def validateJson(self,jsonData):
        try:
            validate(instance=jsonData, schema=self._SHEMA)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True