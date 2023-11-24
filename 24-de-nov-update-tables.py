import psycopg2
import logging
import time
from odoo import fields, models, api, _
from psycopg2.extras import RealDictCursor
from odoo.tools import config

_logger = logging.getLogger(__name__)


class SyncCategory(models.Model):
    _name = "master_pruebas.sync_category"
    _description = "Módelo para la sincronizacion de usuarios"
    

    @api.model
    def sync_category(self):
        conn11 = None
        conn14 = None

        try:
            conn11 = psycopg2.connect(
                host=config['gserp_db_host'],
                database=config['gserp_db_name'],
                user=config['gserp_db_user'],
                password=config['gserp_db_password'])

            cursor11 = conn11.cursor(cursor_factory=RealDictCursor)

            conn14 = psycopg2.connect(
                host=config['db_host'],
                database=config['db_name'],
                user=config['db_user'],
                password=config['db_password'])
            cursor14 = conn14.cursor(cursor_factory=RealDictCursor)

            # Obtener categorías de Odoo 11
            categories_odoo11_query = f"""SELECT * FROM product_category WHERE name IS NOT NULL"""
            cursor11.execute(categories_odoo11_query)
            categories_odoo11 = cursor11.fetchall()
            # Imprimir las 10 primeras categorías en el log

            # Obtener categorías de Odoo 14
            categories_odoo14_query = f"""SELECT * FROM product_category"""
            cursor14.execute(categories_odoo14_query)
            categories_odoo14 = cursor14.fetchall()

            for category_odoo11 in categories_odoo11: 
                exist = False
                # Recorrer las categorías de Odoo 14 para verificar si la categoría ya existe
                for category_odoo14 in categories_odoo14:
                    # print(category_odoo14)
                    if category_odoo11['id'] == category_odoo14['id']:
                        exist = True
                        parent_path = SyncCategory.convert_parent_path(category_odoo11['parent_id'])
                        path_new = f"{parent_path}/{category_odoo11['id']}/" if parent_path else f"{category_odoo11['id']}/"
                        print(path_new)
                        
    
                        if category_odoo11['parent_id']:
                            print('Verificando claves foráneas')
                            self.foreign_key_validate(category_odoo11)

                        self.foreign_key_validate(category_odoo11)

                        # Actualizar solo el campo 'name' en Odoo 14
                        query = f"""UPDATE product_category SET
                                    name = '{category_odoo11['name']}',
                                    parent_id = {category_odoo11['parent_id']},
                                    write_uid = {category_odoo11['write_uid']},
                                    create_uid = {category_odoo11['create_uid']},
                                    write_date = '{category_odoo11['write_date']}',
                                    create_date = '{category_odoo11['create_date']}',
                                    parent_path = '{path_new}',
                                    complete_name = '{category_odoo11['complete_name']}'
                                    WHERE id = {category_odoo11['id']}"""

                        cursor14.execute(query)
                        print('Actualizando categoría (solo name)')
                # Mensaje en el log
                # Si no existe la categoría, se crea
                if not exist:
                    print('Creando categoría')
                    # Convertir la representación de la jerarquía
                    parent_path = SyncCategory.convert_parent_path(category_odoo11['parent_id'])
                    path_new = f"{parent_path}/{category_odoo11['id']}/" if parent_path else f"{category_odoo11['id']}/"


                    # Insertar solo el campo 'name' en Odoo 14
                    query = f"""INSERT INTO product_category (id, name, write_uid, create_uid, write_date, create_date, parent_path, complete_name)
                                VALUES ({category_odoo11['id']}, '{category_odoo11['name']}', {category_odoo11['write_uid']}, {category_odoo11['create_uid']}, '{category_odoo11['write_date']}', '{category_odoo11['create_date']}', '{path_new}', '{category_odoo11['complete_name']}')"""

                    cursor14.execute(query)

            conn14.commit()

        except Exception as e:
            _logger.error("Error: %s", e)

    @staticmethod
    def convert_parent_path(parent_id):
        conn11 = psycopg2.connect(
            host=config['gserp_db_host'],
            database=config['gserp_db_name'],
            user=config['gserp_db_user'],
            password=config['gserp_db_password'])

        cursor11 = conn11.cursor(cursor_factory=RealDictCursor)

        parent_path = []

        while parent_id:
            # Fetch the parent category information
            cursor11.execute(f"SELECT id, parent_id, name FROM product_category WHERE id = {parent_id}")
            parent_category = cursor11.fetchone()

            if parent_category:
                # Insert the parent category id into the list
                parent_path.insert(0, str(parent_category['id']))

                # Update parent_id to continue the loop
                parent_id = parent_category['parent_id']
            else:
                # Break the loop if the parent category is not found
                break

        conn11.close()

        return '/'.join(parent_path)

    @staticmethod
    def foreign_key_validate(category_odoo11):
        category_odoo11['parent_id'] = 'null' if not category_odoo11['parent_id'] else category_odoo11['parent_id']
        category_odoo11['write_uid'] = 'null' if not category_odoo11['write_uid'] else category_odoo11['write_uid']
        category_odoo11['create_uid'] = 'null' if not category_odoo11['create_uid'] else category_odoo11['create_uid']
        category_odoo11['write_date'] = 'null' if not category_odoo11['write_date'] else category_odoo11['write_date']
        category_odoo11['create_date'] = 'null' if not category_odoo11['create_date'] else category_odoo11[
            'create_date']
