from src.dbconn import connection

if __name__ == '__main__':
    try:
        with connection.get_db_cursor(commit=True) as cursor:
            cursor.execute("DROP TABLE IF EXISTS tutorials")

        with connection.get_db_cursor(commit=True) as cursor:
            cursor.execute("CREATE TABLE tutorials (name char(40));")
            cursor.execute("INSERT INTO tutorials VALUES ('Berkeley');")

        with connection.get_db_cursor() as cursor:
            cursor.execute("SELECT * from tutorials")
            rows = cursor.fetchall()
            print(rows)

        with connection.get_db_cursor(commit=True) as cursor:
            cursor.execute("DROP TABLE IF EXISTS tutorials")

    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
