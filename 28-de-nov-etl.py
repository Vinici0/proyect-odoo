import psycopg2 # Para conectarse a la base de datos
import logging # Para imprimir mensajes en el log
import time # Para medir el tiempo de ejecución
from odoo import fields, models, api, _
from psycopg2.extras import RealDictCursor # Para obtener los resultados de las consultas en formato diccionario
from odoo.tools import config # Para obtener la configuración de la base de datos
import datetime # Para obtener la fecha y hora actual
_logger = logging.getLogger(__name__)


class SyncCategory(models.Model):
    _name = "master_pruebas.sync_category"
    _description = "Módelo para la sincronizacion de usuarios"

    @api.model
    def sync_category(self):
        conn11 = None
        conn14 = None
        # Se llama a la clase DatabaseComparator
        dest_db_config = {
            'host': 'localhost',
            'dbname': 'gserp14_new',
            'user': 'vborja',
            'password': 'Vborja@2023'
        }

        # Configuración de la base de datos de destino
        src_db_config = {
            'host': 'localhost',
            'dbname': 'gserp11',
            'user': 'vborja',
            'password': 'Vborja@2023'
        }

        src_db_connector = DatabaseConnector(src_db_config)
        dest_db_connector = DatabaseConnector(dest_db_config)
        db_comparator = DatabaseComparator(src_db_connector, dest_db_connector)

        """
        # db_comparator.update_or_insert_records('res_partner_title')
        # db_comparator.update_or_insert_records('res_company')
        # db_comparator.update_or_insert_records('res_country_state')
        # db_comparator.update_or_insert_records('res_country')

        # db_comparator.update_or_insert_records('sri_forma_pago')
        # db_comparator.update_or_insert_records('res_partner_industry')
        # db_comparator.update_or_insert_records('res_partner_canton')
        # db_comparator.update_or_insert_records('res_partner_parroquia')
        # db_comparator.update_or_insert_records('sale_order')
        # db_comparator.update_or_insert_records('website_support_sla')
        # db_comparator.update_or_insert_records('type_partner')
        """

        """
            Pendientes
        """
        # db_comparator.update_or_insert_records('mail_alias')
        # db_comparator.update_or_insert_records('crm_team')
        # db_comparator.update_or_insert_records('res_users')
        # db_comparator.update_or_insert_records('resource_resource')
        # db_comparator.update_or_insert_records('hr_employee')

        """
            Completado: 
        """
        # db_comparator.update_or_insert_records('resource_resource')
        # db_comparator.update_or_insert_records('res_partner')
        # db_comparator.update_or_insert_records('hr_employee')
        # db_comparator.update_or_insert_records('product_category')
        db_comparator.update_or_insert_records('product_template')
        # res_country
        # db_comparator.update_or_insert_records('res_currency')
        # db_comparator.update_or_insert_records('res_country')
        # db_comparator.update_or_insert_records('res_country_state')

    #
    #     try:
    #
    #         conn11 = psycopg2.connect(
    #             host=config['gserp_db_host'],
    #             database=config['gserp_db_name'],
    #             user=config['gserp_db_user'],
    #             password=config['gserp_db_password'])
    #
    #         cursor11 = conn11.cursor(cursor_factory=RealDictCursor)
    #
    #         conn14 = psycopg2.connect(
    #             host=config['db_host'],
    #             database=config['db_name'],
    #             user=config['db_user'],
    #             password=config['db_password'])
    #         cursor14 = conn14.cursor(cursor_factory=RealDictCursor)
    #
    #         # Obtener categorías de Odoo 11
    #         categories_odoo11_query = f"""SELECT * FROM product_category WHERE name IS NOT NULL"""
    #         cursor11.execute(categories_odoo11_query)
    #         categories_odoo11 = cursor11.fetchall()
    #         # Imprimir las 10 primeras categorías en el log
    #
    #         # Obtener categorías de Odoo 14
    #         categories_odoo14_query = f"""SELECT * FROM product_category"""
    #         cursor14.execute(categories_odoo14_query)
    #         categories_odoo14 = cursor14.fetchall()
    #
    #         for category_odoo11 in categories_odoo11:
    #             exist = False
    #             # Recorrer las categorías de Odoo 14 para verificar si la categoría ya existe
    #             for category_odoo14 in categories_odoo14:
    #                 # print(category_odoo14)
    #                 if category_odoo11['id'] == category_odoo14['id']:
    #                     exist = True
    #                     parent_path = SyncCategory.convert_parent_path(category_odoo11['parent_id'])
    #                     path_new = f"{parent_path}/{category_odoo11['id']}/" if parent_path else f"{category_odoo11['id']}/"
    #                     print(path_new)
    #
    #
    #                     if category_odoo11['parent_id']:
    #                         print('Verificando claves foráneas')
    #                         self.foreign_key_validate(category_odoo11)
    #
    #                     self.foreign_key_validate(category_odoo11)
    #
    #                     # Actualizar solo el campo 'name' en Odoo 14
    #                     query = f"""UPDATE product_category SET
    #                                 name = '{category_odoo11['name']}',
    #                                 parent_id = {category_odoo11['parent_id']},
    #                                 write_uid = {category_odoo11['write_uid']},
    #                                 create_uid = {category_odoo11['create_uid']},
    #                                 write_date = '{category_odoo11['write_date']}',
    #                                 create_date = '{category_odoo11['create_date']}',
    #                                 parent_path = '{path_new}',
    #                                 complete_name = '{category_odoo11['complete_name']}'
    #                                 WHERE id = {category_odoo11['id']}"""
    #
    #                     cursor14.execute(query)
    #                     print('Actualizando categoría (solo name)')
    #             # Mensaje en el log
    #             # Si no existe la categoría, se crea
    #             if not exist:
    #                 print('Creando categoría')
    #                 # Convertir la representación de la jerarquía
    #                 parent_path = SyncCategory.convert_parent_path(category_odoo11['parent_id'])
    #                 path_new = f"{parent_path}/{category_odoo11['id']}/" if parent_path else f"{category_odoo11['id']}/"
    #
    #
    #                 # Insertar solo el campo 'name' en Odoo 14
    #                 query = f"""INSERT INTO product_category (id, name, write_uid, create_uid, write_date, create_date, parent_path, complete_name)
    #                             VALUES ({category_odoo11['id']}, '{category_odoo11['name']}', {category_odoo11['write_uid']}, {category_odoo11['create_uid']}, '{category_odoo11['write_date']}', '{category_odoo11['create_date']}', '{path_new}', '{category_odoo11['complete_name']}')"""
    #
    #                 cursor14.execute(query)
    #
    #         conn14.commit()
    #
    #     except Exception as e:
    #         _logger.error("Error: %s", e)
    #
    # @staticmethod
    # def convert_parent_path(parent_id):
    #     conn11 = psycopg2.connect(
    #         host=config['gserp_db_host'],
    #         database=config['gserp_db_name'],
    #         user=config['gserp_db_user'],
    #         password=config['gserp_db_password'])
    #
    #     cursor11 = conn11.cursor(cursor_factory=RealDictCursor)
    #
    #     parent_path = []
    #
    #     while parent_id:
    #         # Fetch the parent category information
    #         cursor11.execute(f"SELECT id, parent_id, name FROM product_category WHERE id = {parent_id}")
    #         parent_category = cursor11.fetchone()
    #
    #         if parent_category:
    #             # Insert the parent category id into the list
    #             parent_path.insert(0, str(parent_category['id']))
    #
    #             # Update parent_id to continue the loop
    #             parent_id = parent_category['parent_id']
    #         else:
    #             # Break the loop if the parent category is not found
    #             break
    #
    #     conn11.close()
    #
    #     return '/'.join(parent_path)
    #
    # @staticmethod
    # def foreign_key_validate(category_odoo11):
    #     category_odoo11['parent_id'] = 'null' if not category_odoo11['parent_id'] else category_odoo11['parent_id']
    #     category_odoo11['write_uid'] = 'null' if not category_odoo11['write_uid'] else category_odoo11['write_uid']
    #     category_odoo11['create_uid'] = 'null' if not category_odoo11['create_uid'] else category_odoo11['create_uid']
    #     category_odoo11['write_date'] = 'null' if not category_odoo11['write_date'] else category_odoo11['write_date']
    #     category_odoo11['create_date'] = 'null' if not category_odoo11['create_date'] else category_odoo11[
    #         'create_date']

class DatabaseConnector:
    """
        Descripción:
        Clase para conectar a una base de datos.

        Atributos:
        db_config: Diccionario con la configuración de la base de datos.

        Métodos:
        connect_to_database: Conecta a la base de datos.
    """
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



class DatabaseComparator:
    """
        Descripción:
        Clase para comparar tablas de dos bases de datos.

        Atributos:
        src_db_connector: Instancia de la clase DatabaseConnector para la base de datos de origen.
        dest_db_connector: Instancia de la clase DatabaseConnector para la base de datos de destino.

        Métodos:
        compare_tables: Compara las tablas de dos bases de datos.
        update_or_insert_records: Actualiza o inserta registros en la tabla de destino.
    """
    def __init__(self, src_db_connector, dest_db_connector):
        self.src_db_connector = src_db_connector
        self.dest_db_connector = dest_db_connector
        self.table_name = ''

    
    def update_or_insert_records(self, table_name):
        self.table_name = table_name
        matching_fields, non_matching_fields = self.compare_tables(table_name)
        
        dest_conn = self.dest_db_connector.connect_to_database()
        src_conn = self.src_db_connector.connect_to_database()

        if not dest_conn:
            print("No se puede conectar a la base de datos de destino.")
            return

        dest_cursor = dest_conn.cursor()
        src_cursor = src_conn.cursor()

        try:
            self.update_or_insert_matching_records(dest_cursor,src_cursor, table_name, matching_fields)

            dest_conn.commit()
            print("Operación completada con éxito.")
        except Exception as e:
            dest_conn.rollback()
            print(f"Error durante la operación: {str(e)}")
        finally:
            dest_conn.close()

    def compare_tables(self, table_name):
        src_conn = self.src_db_connector.connect_to_database()
        dest_conn = self.dest_db_connector.connect_to_database()

        if not src_conn or not dest_conn:
            print("No se pueden comparar las tablas debido a problemas de conexión.")
            return

        src_cursor = src_conn.cursor()
        dest_cursor = dest_conn.cursor()

        # Fuente (14)
        # Fuente (14)
        src_cursor.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND column_name NOT IN ('write_date', 'create_uid');")
        src_fields = src_cursor.fetchall()

        # Destino (11)
        dest_cursor.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND column_name NOT IN ('write_date', 'create_uid');")
        dest_fields = dest_cursor.fetchall()


        #Eliminar campos campos "write_date" y "create_uid"
        # src_fields = [field for field in src_fields if field[0] not in ['write_date', 'create_uid']]
        # dest_fields = [field for field in dest_fields if field[0] not in ['write_date', 'create_uid']]

        print(src_fields)
        print(dest_fields)
        matching_fields = set(src_fields) & set(dest_fields)
        non_matching_fields = set(src_fields) ^ set(dest_fields)

        # Mapear nombres equivalentes
        equivalent_names = {
            "combination_indices": "equivalent_name_1",
            "can_image_variant_1024_be_zoomed": "equivalent_name_2",
            "message_main_attachment_id": "equivalent_name_3",
            # Agrega otros nombres equivalentes según sea necesario
        }

        # Imprimir o manejar los resultados como desees
        count_matching = 0
        count_non_matching = 0

        print("Campos coincidentes:")
        for field in matching_fields:
            count_matching += 1
            print(f"Fuente (14): {field[0]}")

        print(f"Total de campos coincidentes: {count_matching}\n")

        print("Campos no coincidentes:")
        for field in non_matching_fields:
            count_non_matching += 1
            # Determinar si el campo no coincidente proviene de la Fuente (14) o el Destino (11)
            if field in src_fields:
                print(f"Fuente (14): {field[0]}")
            elif field in dest_fields:
                print(f"Destino (11): {field[0]}")
                # Verificar si el nombre tiene un equivalente conocido
                equivalent_name = equivalent_names.get(field[0])
                if equivalent_name:
                    print(f"Fuente (14): {equivalent_name}")

        fields_to_ignore = {'write_uid', 'create_uid', 'team_id', 'sale_team_id' ,'user_id'}

        # Eliminar campos que no coinciden write_date y create_uid
        matching_fields = [field for field in matching_fields if field[0] not in fields_to_ignore]
        non_matching_fields = [field for field in non_matching_fields if field[0] not in fields_to_ignore]

        # Retornar los campos que coinciden y los que no coinciden
        return matching_fields, non_matching_fields

        print(f"Total de campos que no coinciden: {count_non_matching}\n")

        # Llamar al método para actualizar o insertar registros
        self.update_or_insert_records(table_name, matching_fields, non_matching_fields)

        # Cerrar conexiones
        src_conn.close()
        dest_conn.close()


    def update_or_insert_matching_records(self, dest_cursor, src_cursor, table_name, matching_fields):
        """
        Descripción:
        Actualiza o inserta registros en la tabla de destino basándose en los campos coincidentes.
        """
        # Convertir el conjunto de tuplas a una lista de tuplas
        matching_fields_list = list(matching_fields)

        # Crear la cadena de campos coincidentes para la consulta
        matching_fields_str = ', '.join([field[0] for field in matching_fields_list])

        # Realizar la consulta para obtener los campos coincidentes de la tabla fuente
        sqlSelect = f"""SELECT id, {matching_fields_str} FROM {table_name} WHERE id IS NOT NULL ORDER BY id;"""
        src_cursor.execute(sqlSelect)
        source_records = src_cursor.fetchall()

        # if 'parent_path' in matching_fields_str:
        #     for record in source_records:
        #         parent_path = self.convert_parent_path(record[1], src_cursor)
        #         record[1] = parent_path

        # Actualizar o insertar registros en la tabla de destino
        for record in source_records:
            # Limpiar las listas
            joinSqlScriptAndmatchingUpdate_fields_list = []
            joinSqlScriptAndmatchingInsert_fields_list = []
            id = record[0]  # El primer campo es el id
            index = 0  # Reiniciar el índice para cada registro
            conversion = f''
            for data in record[1:]:  # Excluimos el id
                field_name = matching_fields_list[index][0]  # El nombre del campo

                if data is not None:
                    if isinstance(data, int) or isinstance(data, float):
                        # Si field_name es id, no se debe actualizar
                        if field_name == 'id':
                            print("")
                        else:
                            joinSqlScriptAndmatchingUpdate_fields_list.append(f"{field_name} = %s")
                            joinSqlScriptAndmatchingInsert_fields_list.append(data)
                            conversion = conversion + ',%s'
                    else:
                        joinSqlScriptAndmatchingUpdate_fields_list.append(f"{field_name} = %s")
                        joinSqlScriptAndmatchingInsert_fields_list.append(f"{data}")
                        conversion = conversion + ',%s'
                else:
                    # Tratar como NULL para campos que no son enteros
                    joinSqlScriptAndmatchingUpdate_fields_list.append(f"{field_name} = %s")
                    joinSqlScriptAndmatchingInsert_fields_list.append(None)
                    conversion = conversion + ',%s'

                index += 1
                # Verificar si el índice excede la longitud de matching_fields_list
                if index >= len(matching_fields_list):
                    break

            # Verificamos si existe el registro en la tabla de destino
            dest_cursor.execute(f"SELECT id FROM {table_name} WHERE id = {id};")
            exist = dest_cursor.fetchone()

            #Usando %s para evitar SQL Injection
            valores = conversion.split(',')
            valores = [valor for valor in valores if valor]

            if exist:
                tupleUpdateValues = tuple(joinSqlScriptAndmatchingInsert_fields_list)  # Añadimos el valor del ID al final de la lista de valores
                sqlUpdate = f"""UPDATE {table_name} SET {', '.join(joinSqlScriptAndmatchingUpdate_fields_list)} WHERE id = {id};"""
                print(sqlUpdate)
                dest_cursor.execute(sqlUpdate, tupleUpdateValues)
            else:

                #Comparar si el nombre de la tabla es resource_resource
                if self.table_name == 'resource_resource':
                    joinSqlScriptAndmatchingInsert_fields_list.append("America/Guayaquil")

                joinSqlScriptAndmatchingInsert_fields_list.append(id)

                # Si no existe el registro, insertamos
                tupleInsertValues = tuple(joinSqlScriptAndmatchingInsert_fields_list)
                new_string = matching_fields_str.replace(' id,', '')

                # new_string = self.table_name if self.table_name != 'resource_resource' else f"{new_string},tz"

                #Agreggar una %s al inicio de la cadena
                conversion = conversion + ',%s'
                if self.table_name == 'resource_resource':
                    conversion = conversion + ',%s'

                if self.table_name == 'resource_resource':
                    new_string = f"{new_string},tz"
                #Agregregar el id al final de new_string
                new_string = new_string + ',id'
                # Si es resource_resource quiero que agregue siempre el valor de tupleInsertValues de America/Guayaquil
                #
                #Agregar el id al final de la cadena
                # tupleInsertValues = tupleInsertValues + (id,)
                sqlInsert = '''INSERT INTO {table_name} ({new_string}) VALUES ({conversion[1:]});'''
                print(sqlInsert)
                print(tupleInsertValues)
                new_string = ''
                dest_cursor.execute(sqlInsert, tupleInsertValues)

    def convert_parent_path(self, parent_id, src_cursor):

        # Array para almacenar los ids de las categorías padres
        parent_path = []

        while parent_id:
            # Fetch the parent category information
            src_cursor.execute(f'''SELECT id, parent_id, name FROM product_category WHERE id = {parent_id}''')
            parent_category = src_cursor.fetchone()

            if parent_category:
                # Insert the parent category id into the list
                parent_path.insert(0, str(parent_category['id']))

                # Update parent_id to continue the loop
                parent_id = parent_category['parent_id']
            else:
                # Break the loop if the parent category is not found
                break

        return '/'.join(parent_path)











