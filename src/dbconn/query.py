from src.dbconn import connection
from src.utils import logger
import inspect

DATA = 'data'
ERROR = 'error'
MESSAGE = 'message'


def _execute_select_all(sql, data=None) -> (dict, bool):
    success = False
    sql_string = None
    try:
        with connection.get_db_cursor() as cursor:
            sql_string = cursor.mogrify(sql, data).decode("utf-8")
            logger.debug(inspect.stack()[0][3] + " --> " + sql_string)

            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)
            rows = cursor.fetchall()
            result = {DATA: rows}
            success = True

    except Exception as e:
        err_msg = inspect.stack()[0][3] + " --> \n" + sql_string + "\n" + str(e)
        logger.error(err_msg)

        result = {ERROR: err_msg}

    return result, success


def _iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row


def _execute_select_many(sql, data=None, limit=10):
    sql_string = None
    try:
        with connection.get_db_cursor() as cursor:
            sql_string = cursor.mogrify(sql, data).decode("utf-8")
            logger.debug(inspect.stack()[0][3] + " --> " + sql_string)

            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)

            yield from _iter_row(cursor, limit)

    except Exception as e:
        err_msg = inspect.stack()[0][3] + " --> \n" + sql_string + "\n" + str(e)
        logger.error(err_msg)

        result = {ERROR: err_msg}

        return result, False


def _execute_iud(sql, data, commit=False, **kwargs) -> (dict, bool):
    success = False
    result = ''
    sql_string = None
    try:
        with connection.get_db_cursor(commit) as cursor:
            sql_string = cursor.mogrify(sql, data).decode("utf-8")
            logger.info(inspect.stack()[0][3] + " --> " + sql_string)

            cursor.execute(sql, data)
            rows = cursor.fetchall()
            result = {DATA: rows}
            success = True

    except Exception as e:
        err_msg = inspect.stack()[0][3] + " --> \n" + sql_string + "\n" + str(e)

        # To ignore some exception
        ignore = kwargs.get('ignore_exception')
        if not ignore or not (ignore in err_msg):
            logger.error(err_msg)

        result = {ERROR: err_msg}

    return result, success


def get_records(table_name=None, group=False, offset=0, limit='ALL', field_name=None, qparam=False):
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

    return _execute_select_all(sql, data)


def get_records_partly(table_name=None, group=False, offset=0, limit=10, field_name=None, qparam=False):
    data = None
    if group:
        sql = """SELECT * from {0} OFFSET {1}""".format(table_name, offset)
    elif qparam:
        tmp = """SELECT * from {0} WHERE {1} = %s"""
        for i in range(1, len(field_name)):
            tmp += """ and {""" + str(i+1) + """} = %s"""

        sql = tmp.format(table_name, *field_name)
        data = offset
    elif field_name:
        sql = """SELECT * from {0} WHERE {1} = %s""".format(table_name, field_name)
        data = (offset,)
    else:
        sql = """SELECT * from {0}""".format(table_name)

    return _execute_select_many(sql, data, limit)


def get_count(table_name=None):
    sql = """SELECT COUNT(*) FROM {0}""".format(table_name)

    return _execute_select_all(sql)


def create_record(table_name=None, record=None, return_field=None, production=True, **kwargs):
    str_keys, values, str_format = record.get_key_value_format()
    sql = """INSERT INTO {0} ({1}) VALUES ({2}) RETURNING {3}""" \
        .format(table_name, str_keys, str_format, return_field)

    return _execute_iud(sql, values, commit=production, **kwargs)


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