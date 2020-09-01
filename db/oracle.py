import cx_Oracle
from pprint import pprint
from dbbase import Database
from exception import ConnectDataBaseError


class Oracle(Database):
    '''
    Oracle source class
    '''

    def __init__(self, conn: dict):
        super(Oracle, self).__init__(conn)
        try:
            self._db = cx_Oracle.connect("test", "test", "192.168.31.128:1521/helowin")
        except Exception as e:
            raise ConnectDataBaseError("Cannot connect to oracle", e)
        self.cursor = self._db.cursor()
        self.tables = self._fetch_tables(conn.get("USER"))

    def _fetch_tables(self, schema_name):
        print('schema name', schema_name)
        sql = """SELECT TABLE_NAME FROM dba_tables where owner='TEST'"""
        self.cursor.execute(sql)
        rest = self.cursor.fetchall()
        pprint(rest)


if __name__ == '__main__':
    o = Oracle("x")

    pprint(o.tables)
