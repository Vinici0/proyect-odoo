import requests
import re
import json
import logging

from odoo.tools import config
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class AccountMigrationProfile(models.Model):
    _inherit = 'account.asset.category'

    API_URL = f"""http://{config['gserp14_host']}:{config['gserp14_port']}/jsonrpc/""" if config[
                                                                                              'gserp14_host'] != '' else f"""https://{config['gserp14_host_url']}/jsonrpc/"""

    @api.model
    def create(self, vals):
        id_new = 0
        new_record = super(AccountMigrationProfile, self).create(vals)
        match = re.search(r'\((\d+),\)', str(new_record))
        if match:
            id_new = int(match.group(1))
            _logger.info(f'ID del registro recién creado: {id_new}')

        self.create_profile_odoo14(vals, id_new)
        return new_record

    def create_profile_odoo14(self, vals, id_new):

        data_values = {
            # TODO: Revisar los campos que se deben enviar
            "account_asset_id": vals['account_asset_id'],
            "account_depreciation_id": vals['account_depreciation_id'],
            "account_expense_depreciation_id": vals['account_depreciation_expense_id'],
            "company_id": 1,  # TODO: Revisar si es el ID de la compañia
            "id_profile": id_new,
            "journal_id": vals['journal_id'],
            "method": vals['method'],
            "method_number": vals['method_number'],
            "method_progress_factor": vals['method_progress_factor'],
            "method_time": vals['method_time'],
            "name": vals['name'],
            "open_asset": vals['open_asset'],
            "prorata": vals['prorata'],
        }

        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [
                    config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                    "account.asset.profile",
                    "create",
                    data_values
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

    def write(self, vals):
        self.update_profile_odoo14(vals)
        super(AccountMigrationProfile, self).write(vals)

    def update_profile_odoo14(self, vals):
        if not self.id:
            return False

        id_profile = self.get_profile_id()
        if not id_profile:
            return False

        if id_profile:
            try:
                data_values = {
                    "account_asset_id": vals[
                        'account_asset_id'] if 'account_asset_id' in vals else self.account_asset_id.id,
                    "account_depreciation_id": vals[
                        'account_depreciation_id'] if 'account_depreciation_id' in vals else self.account_depreciation_id.id,
                    "account_expense_depreciation_id": vals[
                        'account_depreciation_expense_id'] if 'account_depreciation_expense_id' in vals else self.account_expense_depreciation_id.id,
                    "company_id": vals['company_id'] if 'company_id' in vals else self.company_id.id,
                    "id_profile": self.id,
                    "journal_id": vals['journal_id'] if 'journal_id' in vals else self.journal_id.id,
                    "method": vals['method'] if 'method' in vals else self.method,
                    "method_number": vals['method_number'] if 'method_number' in vals else self.method_number,
                    "method_progress_factor": vals[
                        'method_progress_factor'] if 'method_progress_factor' in vals else self.method_progress_factor,
                    "method_time": vals['method_time'] if 'method_time' in vals else self.method_time,
                    "name": vals['name'] if 'name' in vals else self.name,
                    "open_asset": vals['open_asset'] if 'open_asset' in vals else self.open_asset,
                    "prorata": vals['prorata'] if 'prorata' in vals else self.prorata,
                }

                api_payload_update = {
                    "jsonrpc": "2.0",
                    "method": "call",
                    "params": {
                        "service": "object",
                        "method": "execute",
                        "args": [
                            config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                            "account.asset.profile",
                            "write",
                            [id_profile, data_values]
                        ]
                    }
                }

                response = requests.post(self.API_URL, json=api_payload_update)
                result = response.json()
                _logger.info(
                    f"Resultado de la actualización del registro en la base de datos {config['gserp_db_name']}: {result}")
            except Exception as e:
                _logger.error(
                    f"Error al actualizar el registro en la base de datos {config['gserp_db_name']}: {str(e)}")

    def unlink(self):
        self.unlink_profile_odoo14()
        super(AccountMigrationProfile, self).unlink()

    def unlink_profile_odoo14(self):

        api_payload_delete = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [
                    config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                    "account.asset.profile",
                    "unlink",
                    [
                        ["id_profile", "=", self.id]
                    ]
                ]
            }
        }

        try:
            response = requests.post(self.API_URL, json=api_payload_delete)
            result = response.json()
            _logger.info(
                f"Resultado de la eliminación del registro en la base de datos {config['gserp_db_name']}: {result}")
        except Exception as e:
            _logger.error(f"Error al eliminar el registro en la base de datos {config['gserp_db_name']}: {str(e)}")

    def get_profile_id(self):
        """
        Obtiene el ID del perfil en base al ID actual.
        """
        if not self.id and not self._origin.id:
            return ''
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [
                    config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                    "account.asset.profile",
                    "search",
                    [["id_profile", "=", self.id if self.id else self._origin.id]]
                ]
            }
        }

        try:
            response = requests.post(self.API_URL, json=api_payload)
            result = response.json()
            _logger.info(
                f"Resultado de la búsqueda del registro en la base de datos {config['gserp_db_name']}: {result}")
            if result['result'] == [] or result['result'] is None or not result['result'] or 'result':
                return ''

            id_profile = result['result'][0]
            return id_profile
        except Exception as e:
            _logger.error(f"Error al buscar el registro en la base de datos {config['gserp_db_name']}: {str(e)}")
            return False
