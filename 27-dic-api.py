from odoo import fields, models, api
from odoo.tools import config
import requests
import re
import json
import logging

_logger = logging.getLogger(__name__)


class AccountMigrationAsset(models.Model):
    _inherit = 'account.asset.asset'

    API_URL = f"""http://{config['gserp14_host']}:{config['gserp14_port']}/jsonrpc/""" if config[
                                                                                              'gserp14_host'] != '' else f"""https://{config['gserp14_host_url']}/jsonrpc/"""

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
        id_profile = self.search_category_id(vals['category_id'])

        data_values = {
            "code": vals['code'],
            "company_currency_id": 2,  # TODO: Moneda de la compañia
            "company_id": vals['company_id'],
            "create_uid": vals['currency_id'],
            "date_start": vals['date'],
            "id_active": id_recien_creado,
            "marca_act": vals['marca'],
            "method": vals['method'],
            "method_number": vals['method_number'],
            "method_progress_factor": vals['method_progress_factor'],
            "method_time": vals['method_time'],
            "modelo_act": vals['modelo'],
            "name": vals['name'],
            "partner_id": vals['partner_id'],  # TODO: Comprobar si es el proveedor
            "profile_id": id_profile if id_profile else vals['category_id'],
            "prorata": vals['prorata'],
            "purchase_value": vals['value'],
            "salvage_value": vals['salvage_value'],
            "serie_act": vals['serie'],
            "state": vals['state'],
            # "invoice_id": vals['invoice_id'],# TODO: No existe en odoo 14
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
            response = requests.post(self.API_URL, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})

            response.raise_for_status()
            result = response.json()
            _logger.info(
                f"Resultado de la llamada a la API: {result} de la base de datos {config['gserp_db_name']} en el metodo create_asset_odoo14")

        except Exception as e:
            _logger.error(f"Error al crear el registro en la base de datos {config['gserp_db_name']}: {str(e)}")

    def search_category_id(self, id_profile):
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                         "account.asset.profile", "search", [["id_profile", "=", id_profile]]]
            }
        }

        try:
            response = requests.post(self.API_URL, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            result = response.json()

            if 'result' in result and not result['result']:
                return ''

            _logger.info(f"Resultado de la llamada a la API: {result} en el metodo search_category_id")
            return result['result'][0]
        except Exception as e:
            _logger.error(f"Error haciendo la llamada a la API: {e} en el metodo search_category_id")
            return False

    def write(self, vals):
        rest = super(AccountMigrationAsset, self).write(vals)
        self.write_active_odoo14(vals)
        return rest

    def write_active_odoo14(self, vals):
        #TODO: Realizar el legacy del write
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'], "account.asset",
                         "search", [["id_active", "=", self.id if self.id else self._origin.id]]]
            }
        }

        try:
            response = requests.post(self.API_URL, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})

            response.raise_for_status()
            result = response.json()
            _logger.info(f"Resultado de la llamada a la API: {result} en el metodo write_active_odoo14")

            if 'result' in result and not result['result']:
                return ''

            id_asset = result['result'][0]

            data_values = {
                "code": vals['code'] if 'code' in vals else self.code,
                "company_currency_id": 2,
                "date_start": vals['date'] if 'date' in vals else self.date,
                "id_active": self.id if self.id else self._origin.id,
                "method": vals['method'] if 'method' in vals else self.method,
                "method_number": vals['method_number'] if 'method_number' in vals else self.method_number,
                "method_progress_factor": vals[
                    'method_progress_factor'] if 'method_progress_factor' in vals else self.method_progress_factor,
                "method_time": vals['method_time'] if 'method_time' in vals else self.method_time,
                "name": vals['name'] if 'name' in vals else self.name,
                "partner_id": vals['partner_id'] if 'partner_id' in vals else self.partner_id.id,
                "profile_id": vals['category_id'] if 'category_id' in vals else self.category_id.id,
                "prorata": vals['prorata'] if 'prorata' in vals else self.prorata,
                "purchase_value": vals['value'] if 'value' in vals else self.value,
                "salvage_value": vals['salvage_value'] if 'salvage_value' in vals else self.salvage_value,
                "state": vals['state'] if 'state' in vals else self.state,
            }

            api_payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                             "account.asset", "write", [id_asset], data_values]
                }
            }
            _logger.info(f"Resultado de la llamada a la API: {result} en el metodo write_active_odoo14")

            response = requests.post(self.API_URL, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})

            response.raise_for_status()
            result = response.json()
            _logger.info(
                f"Resultado de la llamada a la API: {result} en la base de datos {config['gserp_db_name']} en el metodo write_active_odoo14")
            return result
        except Exception as e:
            _logger.error(f"Error haciendo la llamada a la API: {e} en el metodo write_active_odoo14")
            return False

    def write_active_odoo14_legacy(self, vals):
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'], "account.asset",
                         "search", [["id", "=", self.id if self.id else self._origin.id]]]
            }
        }

        try:
            response = requests.post(self.API_URL, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})

            response.raise_for_status()
            result = response.json()
            _logger.info(f"Resultado de la llamada a la API: {result} en el metodo write_active_odoo14")

            if 'result' in result and not result['result']:
                return ''

            id_asset = result['result'][0]

            data_values = {
                "code": vals['code'] if 'code' in vals else self.code,
                "company_currency_id": 2,
                "date_start": vals['date'] if 'date' in vals else self.date,
                "id_active": self.id if self.id else self._origin.id,
                "method": vals['method'] if 'method' in vals else self.method,
                "method_number": vals['method_number'] if 'method_number' in vals else self.method_number,
                "method_progress_factor": vals[
                    'method_progress_factor'] if 'method_progress_factor' in vals else self.method_progress_factor,
                "method_time": vals['method_time'] if 'method_time' in vals else self.method_time,
                "name": vals['name'] if 'name' in vals else self.name,
                "partner_id": vals['partner_id'] if 'partner_id' in vals else self.partner_id.id,
                "profile_id": vals['category_id'] if 'category_id' in vals else self.category_id.id,
                "prorata": vals['prorata'] if 'prorata' in vals else self.prorata,
                "purchase_value": vals['value'] if 'value' in vals else self.value,
                "salvage_value": vals['salvage_value'] if 'salvage_value' in vals else self.salvage_value,
                "state": vals['state'] if 'state' in vals else self.state,
            }

            api_payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                             "account.asset", "write", [id_asset], data_values]
                }
            }

            _logger.info(f"Resultado de la llamada a la API: {result} en el metodo write_active_odoo14")

            response = requests.post(self.API_URL, data=json.dumps(api_payload),
                                        headers={'Content-Type': 'application/json'})

            response.raise_for_status()
            result = response.json()
            _logger.info(
                f"Resultado de la llamada a la API: {result} en la base de datos {config['gserp_db_name']} en el metodo write_active_odoo14")
            return result

        except Exception as e:
            _logger.error(f"Error haciendo la llamada a la API: {e} en el metodo write_active_odoo14")
            return False
        

    def unlink(self):
        result = super(AccountMigrationAsset, self).unlink()
        self.unlink_active_odoo14()
        self.unlink_active_odoo14_legacy()
        return result


    def unlink_active_odoo14(self):
        list_id_account = []
        for record in self:
            list_id_account.append(record.id)

        for id_account in list_id_account:
            api_payload_search = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [
                        config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                        "account.asset",
                        "search",
                        [["id_active", "=", id_account]]
                    ]
                }
            }

            try:
                response_search = requests.post(self.API_URL, json=api_payload_search)
                result_search = response_search.json()
                _logger.info(
                    f"Resultado de la búsqueda del registro en la base de datos {config['gserp_db_name']}: {result_search}")
                id_profile = result_search['result'][0]

                api_payload_delete = {
                    "jsonrpc": "2.0",
                    "method": "call",
                    "params": {
                        "service": "object",
                        "method": "execute",
                        "args": [
                            config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                            "account.asset",
                            "unlink",
                            [id_profile]
                        ]
                    }
                }

                response_delete = requests.post(self.API_URL, json=api_payload_delete)
                result_delete = response_delete.json()
                _logger.info(
                    f"Resultado de la eliminación del registro en la base de datos {config['gserp_db_name']}: {result_delete}")
            except Exception as e:
                _logger.error(
                    f"Error al eliminar el registro en la base de datos {config['gserp_db_name']}: {str(e)}")


    def unlink_active_odoo14_legacy(self):
        list_id_account = []
        for record in self:
            list_id_account.append(record.id)

        for id_account in list_id_account:
            api_payload_search = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [
                        config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                        "account.asset",
                        "search",
                        [["id", "=", id_account]]
                    ]
                }
            }

            try:
                response_search = requests.post(self.API_URL, json=api_payload_search)
                result_search = response_search.json()
                _logger.info(
                    f"Resultado de la búsqueda del registro en la base de datos {config['gserp_db_name']}: {result_search}")
                id_profile = result_search['result'][0]

                api_payload_delete = {
                    "jsonrpc": "2.0",
                    "method": "call",
                    "params": {
                        "service": "object",
                        "method": "execute",
                        "args": [
                            config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                            "account.asset",
                            "unlink",
                            [id_profile]
                        ]
                    }
                }

                response_delete = requests.post(self.API_URL, json=api_payload_delete)
                result_delete = response_delete.json()
                _logger.info(
                    f"Resultado de la eliminación del registro en la base de datos {config['gserp_db_name']}: {result_delete}")
            except Exception as e:
                _logger.error(
                    f"Error al eliminar el registro en la base de datos {config['gserp_db_name']}: {str(e)}")
