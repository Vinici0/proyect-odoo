from sqlalchemy import create_engine
import psycopg2

class DatabaseComparator:
    def __init__(self, src_db_config, dest_db_config):
        self.src_db_config = src_db_config
        self.dest_db_config = dest_db_config

    def connect_to_database(self, db_config):
        try:
            conn_string = f"host={db_config['host']} dbname={db_config['dbname']} user={db_config['user']} password={db_config['password']}"
            conn = psycopg2.connect(conn_string)
            print(f"Conexión exitosa a la base de datos {db_config['dbname']}")
            return conn
        except Exception as e:
            print(f"Error en la conexión a la base de datos {db_config['dbname']}: {str(e)}")
            return None

    def compare_tables(self, table_name):
        src_conn = self.connect_to_database(self.src_db_config)
        dest_conn = self.connect_to_database(self.dest_db_config)

        if not src_conn or not dest_conn:
            print("No se pueden comparar las tablas debido a problemas de conexión.")
            return

        src_cursor = src_conn.cursor()
        dest_cursor = dest_conn.cursor()

        src_cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';")
        src_fields = src_cursor.fetchall()

        dest_cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';")
        dest_fields = dest_cursor.fetchall()

        matching_fields = []
        non_matching_fields = []

        for src_field, dest_field in zip(src_fields, dest_fields):
            src_column_name, src_data_type = src_field
            dest_column_name, dest_data_type = dest_field

            if src_column_name == dest_column_name and (src_data_type == dest_data_type or ('numeric' in src_data_type and 'numeric' in dest_data_type) or ('character' in src_data_type and 'character' in dest_data_type)):
                matching_fields.append(src_field)
            else:
                non_matching_fields.append((src_field, dest_field))

        # Imprimir o manejar los resultados como desees
        print("Campos coincidentes:")
        count = 0
        for field in matching_fields:
            count += 1
            print(field)

        print(count)

        print("Campos no coincidentes:")
        for fields in non_matching_fields:
            print(fields)

        # Cerrar conexiones
        src_conn.close()
        dest_conn.close()

# Configuración de la base de datos de origen
src_db_config = {
    'host': 'localhost',
    'dbname': 'gserp14_new',
    'user': 'vborja',
    'password': 'Vborja@2023'
}

# Configuración de la base de datos de destino
dest_db_config = {
    'host': 'localhost',
     'dbname': 'gserp11',
     'user': 'vborja',
     'password': 'Vborja@2023'
}

# Crear una instancia de la clase DatabaseComparator
# db_comparator = DatabaseComparator(src_db_config, dest_db_config)
#
# # Comparar las tablas
# db_comparator.compare_tables('product_product')
