from src.dbconn import connection

DATA = 'data'
ERROR = 'error'
MESSAGE = 'message'


def _execute_select(sql, data=None):
    success = False
    try:
        with connection.get_db_cursor() as cursor:
            # print("[INFO: _execute_select]", cursor.mogrify(sql, data))
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)
            rows = cursor.fetchall()
            result = {DATA: rows}
            success = True
    except Exception as e:
        print(e)
        result = {ERROR: str(e)}

    return result, success


def _execute_iud(sql, data, commit=False):
    success = False
    result = ''
    try:
        with connection.get_db_cursor(commit) as cursor:
            # print("[INFO: _execute_iud]", cursor.mogrify(sql, data))
            cursor.execute(sql, data)
            rows = cursor.fetchall()
            result = {DATA: rows}
            success = True
    except Exception as e:
        print("[ERROR: _execute_iud]",e)
        # print(e.__dict__)
        # print(e.pgcode)
        # print(errorcodes.lookup(e.pgcode[:2]))
        # print(errorcodes.lookup(e.pgcode))
        result = {ERROR: e}

    return result, success


# def _execute_transection(sqls):
#     success = False
#     result = ''
#     try:
#         with connection.get_db_cursor(True) as cursor:
#             for sql in sqls:
#                 print(cursor.mogrify(sql, data))
#                 cursor.execute(sql, data)
#                 rows = cursor.fetchall()
#                 result = {DATA: rows}
#             success = True
#     except Exception as e:
#         print(e)
#         # print(e.__dict__)
#         # print(e.pgcode)
#         # print(errorcodes.lookup(e.pgcode[:2]))
#         # print(errorcodes.lookup(e.pgcode))
#         result = {ERROR: str(e)}
#
#     return result, success


def get_record(table_name=None, group=False, offset=0, limit='ALL', field_name=None, qparam=False):
    data = None
    if group:
        sql = """SELECT * from {0} LIMIT {1} OFFSET {2}""".format(table_name, limit, offset)
    elif qparam:
        tmp = """SELECT * from {0} WHERE {1} = %s"""
        for i in range(1, len(field_name)):
            tmp += """ and {""" + str(i+1) + """} = %s"""

        sql = tmp.format(table_name, *field_name)
        data = offset
    else:
        sql = """SELECT * from {0} WHERE {1} = %s""".format(table_name, field_name)
        data = (offset,)

    print(sql)
    return _execute_select(sql, data)


def get_count(table_name=None):
    sql = """SELECT COUNT(*) FROM {0}""".format(table_name)

    return _execute_select(sql)


def create_record(table_name=None, record=None, field_name=None, production=True):
    str_keys, values, str_format = record.get_key_value_format()
    sql = """INSERT INTO {0} ({1}) VALUES ({2}) RETURNING {3}""" \
        .format(table_name, str_keys, str_format, field_name)
    print(sql)

    return _execute_iud(sql, values, commit=production)


def update_record(table_name=None, record=None, field_name=None, field_value=None, production=True):
    str_keys, values, str_format = record.get_key_value_format()
    if len(values) > 1:
        sql = """UPDATE {0} SET ({1}) = ({2}) WHERE {3} = %s RETURNING {4}""" \
            .format(table_name, str_keys, str_format, field_name, field_name)
    else:
        sql = """UPDATE {0} SET {1} = {2} WHERE {3} = %s RETURNING {4}""" \
            .format(table_name, str_keys, str_format, field_name, field_name)
    values.append(field_value)
    return _execute_iud(sql, values, commit=production)


def create_or_update_record(table_name=None, record=None, conflict_field=None, return_field=None, production=True):
    str_keys, values, str_format = record.get_key_value_format()
    insert_sql = """INSERT INTO {0} ({1}) VALUES ({2})""" \
        .format(table_name, str_keys, str_format)

    if len(values) > 1:
        update_sql = """UPDATE SET ({0}) = ({1})""" \
            .format(str_keys, str_format)
    else:
        update_sql = """UPDATE SET {0} = {1}""" \
            .format(str_keys, str_format)

    returning_sql = """ RETURNING {0}""".format(return_field)

    sql = insert_sql + """ ON CONFLICT ({0}) DO """.format(conflict_field) + update_sql + returning_sql
    values = values + values

    return _execute_iud(sql, values, commit=production)
