# -*- coding: utf-8 -*-
import requests
import re
import json
import logging

from odoo.tools import config
from odoo import models, fields, api
import re

_logger = logging.getLogger(__name__)


class AccountMigrationAccount(models.Model):
    _inherit = 'account.account'
    api_url = f"""http://{config['gserp14_host']}:{config['gserp14_port']}/jsonrpc/"""

    @api.model
    def create(self, vals):
        id_new = 0
        new_record = super(AccountMigrationAccount, self).create(vals)
        match = re.search(r'\((\d+),\)', str(new_record))
        if match:
            id_new = int(match.group(1))
            _logger.info(f'ID del registro recién creado: {id_new}')

        self.create_account_odoo14(vals, id_new)
        return new_record

    def create_account_odoo14(self, vals, id_new):

        data_values = {
            "name": vals['name'],
            "code": vals['code'],
            "deprecated": vals['deprecated'],
            "user_type_id": 15, #TODO: Tipo de cuenta
            # "internal_type": vals['internal_type'],
            "reconcile": vals['reconcile'],
            # "note": vals['note'],
            "company_id": vals['company_id'],
            # "internal_group": vals['report_type'],
            "id_account": id_new,
        }
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [
                    config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                    "account.account",
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
        self.update_account_odoo14(vals)
        super(AccountMigrationAccount, self).write(vals)

    def update_account_odoo14(self, vals):
        print(vals)
        id_profile = self.get_profile_id()
        match = re.search(r'\((\d+),\)', str(self.user_type_id))
        id_user_type = 0
        if match:
            id_user_type = int(match.group(1))
            _logger.info(f'ID del registro recién creado: {id_user_type}')


        if id_profile:
            data_values = {
                "name": self.name,
                "code": self.code,
                "deprecated": self.deprecated,
                "user_type_id": 15,
                "internal_type": self.internal_type,
                "reconcile": self.reconcile,
                # "note": self.note,
                # "internal_group": self.report_type,
            }

            api_payload_update = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [
                        config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                        "account.account",
                        "write",
                        id_profile, vals
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
        self.unlink_account_odoo14()
        super(AccountMigrationAccount, self).unlink()



    def unlink_account_odoo14(self):

        id_profile = 0
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [
                    config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                    "account.account",
                    "search",
                    [["id_account", "=", self.id]]
                ]
            }
        }

        try:
            response = requests.post(self.api_url, json=api_payload)
            result = response.json()
            _logger.info(
                f"Resultado de la búsqueda del registro en la base de datos {config['gserp_db_name']}: {result}")
            id_profile = result['result'][0]
            # Eliminar el registro en la base de datos de Odoo 14
            api_payload_delete = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [
                        config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                        "account.account",
                        "unlink",
                        [
                            id_profile
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

        except Exception as e:
            _logger.error(f"Error al buscar el registro en la base de datos {config['gserp_db_name']}: {str(e)}")



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
                    "account.account",
                    "search",
                    [["id_account", "=", self.id]]
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

