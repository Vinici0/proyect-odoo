import psycopg2 # Para conectarse a la base de datos
import logging # Para imprimir mensajes en el log
import time # Para medir el tiempo de ejecución
from odoo import fields, models, api, _ 
from psycopg2.extras import RealDictCursor # Para obtener los resultados de las consultas en formato diccionario
from odoo.tools import config # Para obtener la configuración de la base de datos
import datetime # Para obtener la fecha y hora actual


class SyncCategory(models.Model):
    """
        Comenta: 
    """
    _name = "master_pruebas.sync_category"
    _description = "Módelo para la sincronizacion de usuarios"

    @api.model
    def sync_category(self):
        conn11 = None
        conn14 = None
        
        dest_db_config = {
            'host': 'localhost',
            'dbname': 'gserp14_new',
            'user': 'vborja',
            'password': 'Vborja@2023'
        }

        src_db_config = {
            'host': 'localhost',
            'dbname': 'gserp11',
            'user': 'vborja',
            'password': 'Vborja@2023'
        }

        src_db_connector = DatabaseConnector(src_db_config)
        dest_db_connector = DatabaseConnector(dest_db_config)
        db_comparator = DatabaseComparator(src_db_connector, dest_db_connector)
        db_comparator.update_or_insert_records('product_product')

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

    
    def update_or_insert_records(self, table_name):
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
            self.insert_non_matching_records(dest_cursor, table_name, non_matching_fields)

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

        fields_to_ignore = {'write_uid', 'create_uid'}

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
        sqlSelect = f"SELECT id, {matching_fields_str} FROM {table_name} WHERE id IS NOT NULL;"
        src_cursor.execute(sqlSelect)
        source_records = src_cursor.fetchall()

        # Actualizar o insertar registros en la tabla de destino
        for record in source_records:
            # Limpiar las listas
            joinSqlScriptAndmatchingUpdate_fields_list = []
            joinSqlScriptAndmatchingInsert_fields_list = []
            id = record[0]  # El primer campo es el id
            index = 0  # Reiniciar el índice para cada registro

            for data in record[1:]:
                field_name = matching_fields_list[index][0]  # El nombre del campo

                if data is not None:
                    if isinstance(data, int):
                        joinSqlScriptAndmatchingUpdate_fields_list.append(f"{field_name} = {data}")
                        joinSqlScriptAndmatchingInsert_fields_list.append(str(data))
                    else:
                        joinSqlScriptAndmatchingUpdate_fields_list.append(f"{field_name} = '{data}'")
                        joinSqlScriptAndmatchingInsert_fields_list.append(f"'{data}'")
                else:
                    # Tratar como NULL para campos que no son enteros
                    joinSqlScriptAndmatchingUpdate_fields_list.append(f"{field_name} = NULL")
                    joinSqlScriptAndmatchingInsert_fields_list.append('NULL')

                index += 1
                # Verificar si el índice excede la longitud de matching_fields_list
                if index >= len(matching_fields_list):
                    break

            # Verificamos si existe el registro en la tabla de destino
            dest_cursor.execute(f"SELECT id FROM {table_name} WHERE id = {id};")
            exist = dest_cursor.fetchone()
            if exist:
                # Si existe el registro, actualizamos
                dest_cursor.execute(
                    f"UPDATE {table_name} SET {', '.join(joinSqlScriptAndmatchingUpdate_fields_list)} WHERE id = {id};"
                )
            else:
                # Si no existe el registro, insertamos
                sqlInsert = f"INSERT INTO {table_name} ({matching_fields_str}) VALUES ({', '.join(joinSqlScriptAndmatchingInsert_fields_list)});"
                dest_cursor.execute(sqlInsert)
