from db.exception import UnSupportDatabaseTypeError


class Database(object):
    SUPPORT_DATABASE_TYPE = ('oracle', 'postgresql', 'mysql')

    def __init__(self, **kwargs):
        self.db_type = kwargs.get("TYPE")
        if self.db_type not in self.SUPPORT_DATABASE_TYPE:
            raise UnSupportDatabaseTypeError
        self.conn_dict = kwargs
        self.conn = None
        self.cursor = self.conn.cursor()

    def _fetch_table_meta_data(self, table_name):
        return NotImplemented

    def generate_data(self, table_name):
        return NotImplemented

    def close(self):
        self.cursor.close()
