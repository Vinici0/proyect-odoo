from odoo import fields, models, api
from odoo.tools import config
import requests
import re
import json
import logging
import psycopg2

_logger = logging.getLogger(__name__)


class AccountInvoiceLineInherit(models.Model):
    _inherit = 'account.asset.asset'
    api_url = 'http://localhost:8070/jsonrpc/'
    des_db_config = {
        'host': config['db_host'],
        'dbname': config['db_name_14'],
        'user': config['db_user'],
        'password': config['db_password']
    }

    from_group_asset_button = fields.Boolean(
        string='From_group_asset_button?',
        required=False)
    account_invoice_line_ids = fields.Many2many(
        comodel_name='account.invoice.line',
        string='Activos',
        required=False)

    @api.onchange('account_invoice_line_ids')
    def onchange_account_invoice_line_ids(self):
        value = 0
        for account_invoice_line_id in self.account_invoice_line_ids:
            value += account_invoice_line_id.price_unit
        self.value = value

    @api.model
    def create(self, values):
        if 'account_invoice_line_ids' in values:
            account_invoice_lines = self.env['account.invoice.line'].search(
                [('id', 'in', values['account_invoice_line_ids'][0][2])])
            for account_invoice_line in account_invoice_lines:
                account_invoice_line.asset_done = True

        """Sincronizacion con Odoo 14 - Responsable: Vinicio Borja"""
        id_recien_creado = 0
        nuevo_registro = super(AccountInvoiceLineInherit, self).create(values)
        match = re.search(r'\((\d+),\)', str(nuevo_registro))
        if match:
            id_recien_creado = int(match.group(1))
            _logger.info(f'ID del registro recién creado: {id_recien_creado}')

        self.create_asset_odoo14(values, id_recien_creado)
        return nuevo_registro

    def create_asset_odoo14(self, vals, id_recien_creado):
        try:

            databas_connector = DatabaseConnector(self.des_db_config)
            conn = databas_connector.connect_to_database()
            cursor = conn.cursor()

            query_insert = """
                INSERT INTO account_asset (id, code, company_id, company_currency_id, method_number, method_progress_factor, method_time, method, name, prorata, profile_id, purchase_value, salvage_value, state, date_start)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            cursor.execute(query_insert, (
                id_recien_creado,
                vals['code'],
                vals['company_id'],
                vals['currency_id'],
                vals['method_number'],
                vals['method_progress_factor'],
                vals['method_time'],
                vals['method'],
                vals['name'],
                vals['prorata'],
                1,  # Perfil de activos fijo
                vals['value'],
                vals['salvage_value'],
                vals['state'],
                vals['date'],
            ))
            conn.commit()
            cursor.close()
        except Exception as e:
            _logger.error(f"Error al crear el registro en la base de datos {config['db_name_14']}: {str(e)}")

    def write(self, values):
        _logger.info(f'Values: {values}')
        self.write_active(values)


    def write_active(self, vals):

        #Consulta en la base de 11 el todos los valores de la tabla de los valores recione creados utiliza la conexion de la base de 11 self.des_db_config

        try:
            databas_connector = DatabaseConnector(self.des_db_config)
            conn = databas_connector.connect_to_database()
            cursor = conn.cursor()
            query = f"""SELECT * FROM account_asset WHERE id = {self.id}"""
            cursor.execute(query)
            asset = cursor.fetchone()


        data_asset = {
            "code": vals['code'],
            "company_id": vals['company_id'],
            "company_currency_id": vals['currency_id'],
            "method_number": vals['method_number'],
            "method_progress_factor": vals['method_progress_factor'],
            "method_time": vals['method_time'],
            "method": vals['method'],
            "name": vals['name'],
            "prorata": vals['prorata'],
            "profile_id": 1,
            "purchase_value": vals['value'],
            "salvage_value": vals['salvage_value'],
            "state": vals['state'],
            "date_start": vals['date'],
        }

        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [config['db_name_14'], 2, config['password_odoo14_api'], "account.asset", "write", [self.id], data_asset]
            }
        }

        try:
            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})
            result = response.json()
            print(result)
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error haciendo la llamada a la API: {e}")

    def unlink(self):
        super(AccountInvoiceLineInherit, self).unlink()

        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [config['db_name_14'], 2, config['password_odoo14_api'], "account.asset", "unlink", [self.id]]
            }
        }

        try:
            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})
            result = response.json()
            print(result)
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error haciendo la llamada a la API: {e}")



class DatabaseConnector:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect_to_database(self):
        try:
            conn_string = f"host={self.db_config['host']} dbname={self.db_config['dbname']} user={self.db_config['user']} password={self.db_config['password']}"
            conn = psycopg2.connect(conn_string)
            _logger.info(f"Connection to database {self.db_config['dbname']} successful")
            return conn
        except Exception as e:
            _logger.error(f"Error while connecting to database {self.db_config['dbname']}: {str(e)}")
            return None
