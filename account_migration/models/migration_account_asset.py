from odoo import fields, models, api
from odoo.tools import config
import requests
import re
import json
import logging

_logger = logging.getLogger(__name__)

class AccountMigrationAsset(models.Model):
    _inherit = 'account.asset.asset'
    api_url = f"""http://{config['gserp14_host']}:{config['gserp14_port']}/jsonrpc/"""


    @api.model
    def create(self, values):
        id_recien_creado = 0
        nuevo_registro = super(AccountMigrationAsset, self).create(values)
        match = re.search(r'\((\d+),\)', str(nuevo_registro))
        if match:
            id_recien_creado = int(match.group(1))
            _logger.info(f'ID del registro recién creado: {id_recien_creado}')

        self.create_asset_odoo14(values, id_recien_creado)
        return nuevo_registro

    def create_asset_odoo14(self, vals, id_recien_creado):
        data_values = {
            "code": vals['code'],
            "company_id": vals['company_id'],
            "create_uid": vals['currency_id'],
            "company_currency_id": 2, #TODO: Moneda de la compañia
            "method_number": vals['method_number'],
            "method_progress_factor": vals['method_progress_factor'],
            "method_time": vals['method_time'],
            "method": vals['method'],
            "name": vals['name'],
            "prorata": vals['prorata'],
            "profile_id": 1, #TODO: Perfil de activos fijo
            "purchase_value": vals['value'],
            "salvage_value": vals['salvage_value'],
            "state": vals['state'],
            "date_start": vals['date'],
            "id_active": id_recien_creado
        }

        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                         "account.asset", "create", data_values]
            }
        }

        try:

            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})

            response.raise_for_status()
            result = response.json()
            _logger.info(f"Resultado de la llamada a la API: {result}")

        except Exception as e:
            _logger.error(f"Error al crear el registro en la base de datos {config['db_name_14']}: {str(e)}")


    def write(self, vals):
        rest = super(AccountMigrationAsset, self).write(vals)
        self.write_active_odoo14(vals)
        return rest

    def write_active_odoo14(self, vals):
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'], "account.asset", "search", [["id_active", "=", self.id if self.id else self._origin.id]]]
            }
        }

        try:
            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})

            response.raise_for_status()
            result = response.json()
            _logger.info(f"Resultado de la llamada a la API: {result} en el metodo write_active_odoo14")
            _logger.info(f"Resultado de la llamada a la API: {result['result']}")
            if result['result'] == []:
                return ''

            id_asset = result['result'][0]


            data_values = {
                "code": self.code,
                "company_currency_id": 3,
                "method_number": self.method_number,
                "method_progress_factor": self.method_progress_factor,
                "method_time": self.method_time,
                "method": self.method,
                "name": self.name,
                "prorata": self.prorata,
                "profile_id": 1, # TODO: Perfil de activos fijo
                "purchase_value": self.value,
                "salvage_value": self.salvage_value,
                "state": self.state,
                "date_start": self.date,
                "id_active": self.id
            }

            api_payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'], "account.asset", "write", [id_asset], data_values]
                }
            }
            _logger.info(f"Resultado de la llamada a la API: {result}")

            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                        headers={'Content-Type': 'application/json'})

            response.raise_for_status()
            result = response.json()
            _logger.info(f"Resultado de la llamada a la API: {result}")

        except requests.exceptions.RequestException as e:
            _logger.error(f"Error haciendo la llamada a la API: {e}")


    def unlink(self):
        super(AccountMigrationAsset, self).unlink()
        self.unlink_active_odoo14()

    def unlink_active_odoo14(self):
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'], "account.asset", "search", [["id_active", "=", self.id]]]
            }
        }

        try:
            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            result = response.json()
            _logger.info(f"Resultado de la llamada a la API: {result} en el metodo unlink_active_odoo14")
            id_asset = result['result'][0]

            api_payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'], "account.asset", "unlink", [id_asset]]
                }
            }
            _logger.info(f"Resultado de la llamada a la API: {result}")

            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                        headers={'Content-Type': 'application/json'})

            response.raise_for_status()
            result = response.json()
            _logger.info(f"Resultado de la llamada a la API: {result}")

        except requests.exceptions.RequestException as e:
            _logger.error(f"Error haciendo la llamada a la API: {e}")













