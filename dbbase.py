from exception import UnSupportDatabaseTypeError


class Database(object):
    SUPPORT_DATABASE_TYPE = ('oracle', 'postgresql', 'mysql')

    def __init__(self, **kwargs):
        self.db_type = kwargs.get("TYPE")
        if self.db_type not in self.SUPPORT_DATABASE_TYPE:
            raise UnSupportDatabaseTypeError
        self.conn_dict = kwargs

    def _fetch_table_meta_data(self, table_name):
        return NotImplemented

    def generate_data(self, table_name):
        return NotImplemented

    def close(self):
        self.cursor.close()


class Convert(object):
    '''
        data convert class

    '''

    def __init__(self, conn):
        self.conn = conn

    def _field_mapping(self, table_name):
        pass

    def insert_row_to_target_data(self, row, db_conn):
        pass
