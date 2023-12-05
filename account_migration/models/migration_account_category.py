# -*- coding: utf-8 -*-
import requests
import re
import json
import logging

from odoo.tools import config
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class AccountMigrationProfile(models.Model):
    _inherit = 'account.asset.category'
    api_url = f"""http://{config['gserp14_host']}:{config['gserp14_port']}/jsonrpc/"""

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
            "name": vals['name'],
            "account_asset_id": 1,
            "account_depreciation_id": 1,
            "account_expense_depreciation_id": 1,
            "journal_id": 1,
            "company_id": 1,
            "method": vals['method'],
            "method_number": vals['method_number'],
            "method_progress_factor": vals['method_progress_factor'],
            "method_time": vals['method_time'],
            "prorata": vals['prorata'],
            "open_asset": vals['open_asset'],
            "id_profile": id_new,
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
            response = requests.post(self.api_url, json=api_payload)
            result = response.json()
            _logger.info(f"Resultado de la creación del registro en la base de datos {config['gserp_db_name']}: {result}")
        except Exception as e:
            _logger.error(f"Error al crear el registro en la base de datos {config['gserp_db_name']}: {str(e)}")

    def write(self, vals):
        self.update_profile_odoo14(vals)
        super(AccountMigrationProfile, self).write(vals)

    def update_profile_odoo14(self, vals):

        id_profile = self.get_profile_id()

        if id_profile:
            data_values = {
                "name": self.name,
                "account_asset_id": self.account_asset_id.id,
                "account_depreciation_id": self.account_depreciation_id.id,
                "account_expense_depreciation_id": self.account_depreciation_expense_id.id,
                "journal_id": self.journal_id.id,
                "company_id": self.company_id.id,
                "method": self.method,
                "method_number": self.method_number,
                "method_progress_factor": self.method_progress_factor,
                "method_time": self.method_time,
                "prorata": self.prorata,
                "open_asset": self.open_asset,
                "id_profile": self.id,
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

            try:
                response = requests.post(self.api_url, json=api_payload_update)
                result = response.json()
                _logger.info(f"Resultado de la actualización del registro en la base de datos {config['gserp_db_name']}: {result}")
            except Exception as e:
                _logger.error(f"Error al actualizar el registro en la base de datos {config['gserp_db_name']}: {str(e)}")

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
            response = requests.post(self.api_url, json=api_payload_delete)
            result = response.json()
            _logger.info(f"Resultado de la eliminación del registro en la base de datos {config['gserp_db_name']}: {result}")
        except Exception as e:
            _logger.error(f"Error al eliminar el registro en la base de datos {config['gserp_db_name']}: {str(e)}")


    def get_profile_id(self):
        """
        Obtiene el ID del perfil en base al ID actual.
        """
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
                    [["id_profile", "=", self.id]]
                ]
            }
        }

        try:
            response = requests.post(self.api_url, json=api_payload)
            result = response.json()
            _logger.info(
                f"Resultado de la búsqueda del registro en la base de datos {config['gserp_db_name']}: {result}")
            id_profile = result['result'][0]
            return id_profile
        except Exception as e:
            _logger.error(f"Error al buscar el registro en la base de datos {config['gserp_db_name']}: {str(e)}")
            return False
