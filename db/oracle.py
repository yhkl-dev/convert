import cx_Oracle
from db.dbbase import Database
from db.exception import ConnectDataBaseError
from config import Config
from db.sql import oracle_get_user_tables_sql_fmt, oracle_check_table_struct_sql_fmt, \
    oracle_query_table_data_sql_fmt
import sys
import typing


class Oracle(Database):
    '''
    Oracle source class
    '''

    def __init__(self, **kwargs):
        super(Oracle, self).__init__(**kwargs)
        try:
            conn_string = "{user}/{password}@{host}:{port}/{sid}".format(user=kwargs.get("USER"),
                                                                         password=kwargs.get("PASSWORD"),
                                                                         host=kwargs.get("HOST"),
                                                                         port=kwargs.get("PORT"),
                                                                         sid=kwargs.get("SID"))

            self._db = cx_Oracle.connect(conn_string)

        except Exception as e:
            raise ConnectDataBaseError("Cannot connect to oracle", e)

        self.cursor = self._db.cursor()
        self.tables = self._fetch_tables(kwargs.get("USER"))
        if len(self.tables) == 0:
            print('no tables to convert')
            sys.exit(0)

    def _fetch_tables(self, user_name: str) -> list:
        print('user/schema name', user_name)

        sql = oracle_get_user_tables_sql_fmt.format(user_name.upper())

        self.cursor.execute(sql)

        res = self.cursor.fetchall()
        return [table_tuple[0] for table_tuple in res] if len(res) != 0 else []

    def _fetch_table_meta_data(self, table_name: str) -> list:
        sql = oracle_check_table_struct_sql_fmt.format(table_name)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return [(column[1], column[2]) for column in res]

    def generate_data(self, table_name: str) -> typing.Sequence:
        table_columns_and_type = self._fetch_table_meta_data(table_name)
        table_columns = [table_column[0] for table_column in table_columns_and_type]
        sql = oracle_query_table_data_sql_fmt.format(table_columns=','.join(table_columns),
                                                     table_name=table_name)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        for row in res:
            yield row

    def generate_all_table_data(self):
        for table_name in self.tables:
            rows_generator = self.generate_data(table_name)
            for row in rows_generator:
                yield row


if __name__ == '__main__':
    # o = Oracle(Config().source_conn)
    conf = Config()
    o = Oracle(**conf.SOURCE_CONN)

    o.generate_all_table_data()
