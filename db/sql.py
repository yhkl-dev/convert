oracle_get_user_tables_sql_fmt = """
    SELECT TABLE_NAME FROM dba_tables where owner={}
"""
