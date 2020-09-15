import cx_Oracle
import csv
import sys

INSERT_SQL_FMT = """
    insert into "{table_name}" values ({fileds})
    
"""

TABLE_META_DATA_SQL = """
    SELECT * FROM USER_TAB_COLUMNS WHERE TABLE_NAME='{}'
"""

class NUMBER2(object):

    def __init__(self, length, precision):
        self._length = length
        self._precision = precision

    def __call__(self, value):
        try:
            if not self._length or self._precision == 0:
                return int(value)
            return round(float(value), self._precision)
        except ValueError:
            # return Exception("Value type error got {} want {}".format(value, 'int or float'))
            return 0


class VARCHAR2(object):

    def __init__(self, length):
        self._length = length

    def __call__(self, value):
        if isinstance(value, str):
            if len(value) > self._length:
                raise Exception("The length of {} is too long".format(value))
            return repr((value))
        if isinstance(value, (int, float)):
            return repr((value))


class TEXT(object):

    def __call__(self, value):
        return repr(value)


class Oracle(object):
    def __init__(self, **kwargs):
        self.conn_string = "{user}/{password}@{host}:{port}/{sid}".format(
            **kwargs)
        self.user = kwargs.get("user")
        try:
            self._db = cx_Oracle.connect(self.conn_string)
        except Exception as e:
            raise Exception("Connect Oracle Error, error is: ", e)

    def insert_row_to_table(self, table_name, row):
        table_header = self._fetch_table_meta_data(table_name)

        table_row = []
        for i, item in enumerate(row):
            print('item', item)
            table_row.append(eval(table_header[i][1])(item))
        sql = INSERT_SQL_FMT.format(user=self.user,
                                    table_name=table_name,
                                    fileds=",".join(
                                        [repr(item) for item in row]))
        with self._db.cursor() as cursor:
            print(sql)
            cursor.execute(sql)

    def _fetch_table_meta_data(self, table_name: str) -> list:
        sql = TABLE_META_DATA_SQL.format(table_name)
        with self._db.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
            return [(column[1], column[2]) for column in res]

    def generate_row_from_file(self, csv_file_name):
        with open(csv_file_name, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                yield row

    def insert_to_table(self, table_name, csv_file_name):
        generator = self.generate_row_from_file(csv_file_name)
        for row in generator:
            self.insert_row_to_table(table_name, row)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("no table and csv file")
        sys.exit(1)
    table_name = sys.argv[1]
    csv_file_name = sys.argv[2]
    conn_dict = {
        "user": 'test',
        'password': "test",
        'host': '192.168.31.128',
        'port': 1521,
        'sid': 'helowin'
    }
    o = Oracle(**conn_dict)
    o.insert_to_table(table_name, csv_file_name)
