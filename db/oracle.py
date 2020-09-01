import cx_Oracle
from pprint import pprint
from dbbase import Database
from exception import ConnectDataBaseError
from config import Config
from sql import oracle_get_user_tables_sql_fmt


class Oracle(Database):
    '''
    Oracle source class
    '''

    def __init__(self, **kwargs):
        super(Oracle, self).__init__(**kwargs)
        try:
            # self._db = cx_Oracle.connect("test", "test", "192.168.31.128:1521/helowin")
            self._db = cx_Oracle.connect(kwargs.get("USER"), kwargs.get("PASSWORD"),
                                         "{}:{}/{}".format(kwargs.get("HOST"), kwargs.get("PORT"), kwargs.get("SID")))
        except Exception as e:
            raise ConnectDataBaseError("Cannot connect to oracle", e)
        self.cursor = self._db.cursor()
        self.tables = self._fetch_tables(kwargs.get("USER"))

    def _fetch_tables(self, user_name):
        print('user/schema name', user_name)
        sql = oracle_get_user_tables_sql_fmt.format(user_name.upper())
        self.cursor.execute(sql)
        rest = self.cursor.fetchall()
        pprint(rest)


if __name__ == '__main__':
    # o = Oracle(Config().source_conn)
    conf = Config()
    o = Oracle(**conf.SOURCE_CONN)
