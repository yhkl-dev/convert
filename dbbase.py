class Database(object):

    def __init__(self, **kwargs):
        self.conn = kwargs

    def _fetch_tables_name_in_schema(self, schema_name):
        pass

    def _fetch_table_meta_data(self, table_name):
        pass

    def _field_mapping(self, table_name):
        pass

    def generate_data(self, table_name):
        pass

    def insert_target_db(self, db_type, schema_name):
        pass


class Convert(object):

    def __init__(self, conn):
        self.conn = conn

    def insert_row_to_target_data(self, row, db_conn):
        pass
