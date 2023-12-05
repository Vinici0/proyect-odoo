from odoo import fields, models, api
from odoo.tools import config
import requests
import re
import json
import logging

_logger = logging.getLogger(__name__)


class AccountMigrationJournal(models.Model):
    _inherit = 'account.journal'
    api_url = f"""http://{config['gserp14_host']}:{config['gserp14_port']}/jsonrpc/"""

    @api.model
    def create(self, values):
        id_new = 0
        new_record = super(AccountMigrationJournal, self).create(values)
        match = re.search(r'\((\d+),\)', str(new_record))
        if match:
            id_new = int(match.group(1))
            _logger.info(f'ID del registro recién creado: {id_new}')

        self.create_journal_odoo14(values, id_new)
        return new_record

    def create_journal_odoo14(self, vals, id_new):

        data_values = {
            "name": vals['name'],
            "code": vals['code'],
            "active": vals['active'],
            "type": vals['type'],
            "payment_credit_account_id": vals['default_credit_account_id'],
            "payment_debit_account_id": vals['default_debit_account_id'],
            "company_id": vals['company_id'],
            "refund_sequence": vals['refund_sequence'],
            "bank_statements_source": vals['bank_statements_source'],
            "show_on_dashboard": vals['show_on_dashboard'],
            "invoice_reference_type": 'invoice',
            "invoice_reference_model": 'odoo',
            "id_journal": id_new,
        }

        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [
                    config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                    "account.journal",
                    "create",
                    data_values
                ]
            }
        }

        try:

            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})

            response.raise_for_status()
            result = response.json()

            _logger.info(f'Respuesta de la API: {result}')
        except Exception as e:
            _logger.info(f'Error al crear el registro en la base de datos {config["gserp_db_name"]}: {e}')

    def write(self, vals):
        super(AccountMigrationJournal, self).write(vals)
        self.update_journal_odoo14()

    def update_journal_odoo14(self):
        id_profile = self.get_profile_id()

        data_values = {
            "name": self.name,
            "active": self.active,
            "type": self.type,
            "code": self.code,
            "payment_credit_account_id": self.default_credit_account_id.id,
            "payment_debit_account_id": self.default_debit_account_id.id,
            "company_id": self.company_id.id,
            "refund_sequence": self.refund_sequence,
            "bank_statements_source": self.bank_statements_source,
            "show_on_dashboard": self.show_on_dashboard,
        }

        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [
                    config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                    "account.journal",
                    "write",
                    [id_profile], data_values
                ]
            }
        }

        try:
            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})

            response.raise_for_status()
            result = response.json()

            _logger.info(f'Respuesta de la API: {result}')
        except Exception as e:
            _logger.info(f'Error al crear el registro en la base de datos {config["gserp_db_name"]}: {e}')

    def get_profile_id(self):
        """
        Obtiene el ID del journal en la base de datos de Odoo 14
        """
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [
                    config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                    "account.journal",
                    "search",
                    [["id_journal", "=", self.id]]
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

    def unlink(self):
        self.unlink_journal_odoo14()
        super(AccountMigrationJournal, self).unlink()

    def unlink_journal_odoo14(self):
        # Buscar el ID del registro en la base de datos de Odoo 14
        id_profile = 0
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [
                    config['gserp_db_name'], config['id_user_api'], config['password_odoo14_api'],
                    "account.journal",
                    "search",
                    [["id_journal", "=", self.id]]
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
                        "account.journal",
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


