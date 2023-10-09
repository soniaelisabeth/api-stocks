import sqlite3

MAIN_DB_PATH = "api_service/api_service.sqlite3"

def execute_query(values):
    try:
        db_connection = sqlite3.connect(MAIN_DB_PATH, timeout=15)
        cursor = db_connection.cursor()
        cursor.execute(INSERT_STOCKS_QUERY, values)
        db_connection.commit()
    except Exception as e:
        return e.args
    finally:
        if db_connection:
            db_connection.close()
            return True

def select_query():
    try:
        db_connection = sqlite3.connect(MAIN_DB_PATH, timeout=15)
        cursor = db_connection.cursor()
        cursor.execute(FETCH_ALL_STOCKS_QUERY)
        return cursor.fetchall()
    except Exception as e:
        return e.args
    finally:
        if db_connection:
            db_connection.close()

def is_user_available(user, password):
    try:
        db_connection = sqlite3.connect(MAIN_DB_PATH)
        cursor = db_connection.cursor()
        cursor.execute(FETCH_USER_QUERY, (user,password))
        count = cursor.fetchone()[0]

        return count > 0

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        if db_connection:
            db_connection.close()


FETCH_ALL_STOCKS_QUERY = "SELECT * FROM stocks"
FETCH_USER_QUERY = 'SELECT COUNT(*) FROM user WHERE username = ? AND password = ?'
INSERT_STOCKS_QUERY = 'INSERT OR REPLACE INTO stocks (name, data) VALUES (?,?)'