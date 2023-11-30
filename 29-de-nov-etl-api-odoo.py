# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json
import re
import logging
import psycopg2
_logger = logging.getLogger(__name__)


class sing_test(models.Model):
    _name = 'master_pruebas.master_pruebas'
    _description = 'master_pruebas.master_pruebas'
    api_url = 'http://localhost:8069/jsonrpc/'  # Replace with your actual API endpoint


    apellido = fields.Char(string='Apellidos')
    name = fields.Char(string='Nombres')

    @api.model
    def create(self, vals):
        nuevo_registro = super(sing_test, self).create(vals)
        match = re.search(r'\((\d+),\)', str(nuevo_registro))
        id_recien_creado = 0
        if match:
            id_recien_creado = int(match.group(1))
            _logger.info(f'ID del registro recién creado: {id_recien_creado}')

        self.sav_product(nuevo_registro, id_recien_creado)
        return nuevo_registro

    def write(self, vals):
        super(sing_test, self).write(vals)
        self.write_product(vals)


    def write_product(self, vals):
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": ["gserp11", 1, "admin", "master_test.master_test", "write", [self.id], vals]
            }
        }

        try:
            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error haciendo la llamada a la API: {e}")

    def unlink(self):
        super(sing_test, self).unlink()
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": ["gserp11", 1, "admin", "master_test.master_test", "unlink", [self.id]]
            }
        }

        try:
            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})
            response.raise_for_status()  # Verifica si hay errores HTTP
            result = response.json()
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error haciendo la llamada a la API: {e}")

    @api.model
    def sync_category(self):
        print('Categorias')

    def sav_product(self, vals, id_recien_creado):
        # Define el endpoint y el payload de la API para la creación
        api_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": ["gserp11", 1, "admin", "master_test.master_test", "create", {
                    "name": vals.name
                    # Puedes añadir más campos según la estructura de tu modelo "employee.employee"
                }]
            }
        }

        # Hacer la llamada a la API usando requests
        try:
            response = requests.post(self.api_url, data=json.dumps(api_payload),
                                     headers={'Content-Type': 'application/json'})
            result = response.json()
            nuevo_id = result.get('result')  # Obtener el nuevo id asignado por Odoo

            # Actualizar el registro con el id deseado
            if nuevo_id and nuevo_id != id_recien_creado:
                src_db_config = {
                    'host': 'localhost',
                    'dbname': 'gserp11',
                    'user': 'vborja',
                    'password': 'Vborja@2023'
                }
                databas_connector = DatabaseConnector(src_db_config)
                conn = databas_connector.connect_to_database()
                cursor = conn.cursor()

                cursor.execute(f"UPDATE master_test_master_test SET id = {id_recien_creado} WHERE id = {nuevo_id};")
                conn.commit()

                cursor.close()

        except requests.exceptions.RequestException as e:
            _logger.error(f"Error haciendo la llamada a la API: {e}")


#  Editar registro
class DatabaseConnector:

    def __init__(self, db_config):
        self.db_config = db_config

    def connect_to_database(self):
        try:
            conn_string = f"host={self.db_config['host']} dbname={self.db_config['dbname']} user={self.db_config['user']} password={self.db_config['password']}"
            conn = psycopg2.connect(conn_string)
            print(f"Conexión exitosa a la base de datos {self.db_config['dbname']}")
            return conn
        except Exception as e:
            print(f"Error en la conexión a la base de datos {self.db_config['dbname']}: {str(e)}")
            return None
