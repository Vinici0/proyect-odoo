## API Postman
```
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "object",
    "method": "execute",
    "args": [
      "gserp11",//name = 11
      2, //id = user
      "admin",
      "botpress_comunication.agendar_cobro",
      "create",
  {
    "nombre":"Vinicio Borja",
    "cid":"1791728114001",
    "phone":"0994958942",
    "caso":"593994958942",
    "contrato":"126005",
    "fecha":"12-12-2024",
    "lugar":"Santo Domingo"
}
    ]
  }
}
```

## ODOO CONFIG
```
password_odoo11_api = admin
id_user_api = 1
; gserp14_host = ''
gserp11_host_url = gruposcanner.com
user_odoo11_api = admin
gserp11_host = 192.168.15.245
gserp11_port = 8070
```

## URL API
```
API_URL = f"""http://{config['gserp11_host']}:{config['gserp11_port']}/jsonrpc/""" if config[
                                                                                              'gserp11_host'] != '' else f"""https://{config['gserp11_host_url']}/jsonrpc/"""

```

## Api Agendar Cobro
```
  @http.route('/agendar-fecha-cobro/', type="json", auth='none', method=['POST'], cors="*", csrf=False)
    def _agendar_fecha_cobro(self, **kw):
        try:
            data = request.jsonrequest
            print(data)
            im_chat = None
            if 'caso' in data:
                im_chat = http.request.env['im_chat'].sudo().search([('caso', '=', data['caso'])], limit=1)
            data_json = {
                'name': data['nombre'],
                'ref': data['cid'],
                'phone': data['phone'],
                'contrato': int(data['contrato']),
                'fecha': data['fecha'],
                'lugar': data['lugar'],
                'caso': im_chat.id if im_chat else None
            }
            self._agendar_fecha_cobro_api(data_json)
            http.request.env['botpress_comunication.agendar_cobro'].sudo().create(data_json)
            return {'status': 200, 'status_response': "ok"}
        except Exception as e:
            _logger.info("Error en la creacion de de fecha de cobro " + str(e))
            return {'status': 500, 'status_response': "error"}
```

```
 def _agendar_fecha_cobro_api(self, data_json):
        try:
            api_payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [
                        config['botpress_comunication.agendar_cobro'], config['id_user_api'], config['password_odoo11_api'],
                        "account.account",
                        "create",
                        data_json
                    ]

                }
            }

            try:
                response = requests.post(self.API_URL, json=api_payload)
                result = response.json()
                _logger.info(
                    f"Resultado de la creación del registro en la base de datos {config['gserp_db_name']}: {result}")
            except Exception as e:
                _logger.error(f"Error al crear el registro en la base de datos {config['gserp_db_name']}: {str(e)}")

        except Exception as e:
            _logger.info("Error en la creacion de de fecha de cobro " + str(e))
```
