oracle_get_user_tables_sql_fmt = """
    SELECT TABLE_NAME FROM dba_tables where owner='{}'
"""

oracle_check_table_struct_sql_fmt = """
    SELECT * FROM USER_TAB_COLUMNS WHERE TABLE_NAME='{}'
"""

oracle_query_table_data_sql_fmt = """
    select {table_columns} from {table_name}
"""
