import sqlite3

try:
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE accounts_user (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      password VARCHAR(128) NOT NULL,
      last_login DATETIME NULL,
      is_superuser BOOLEAN NOT NULL,
      username VARCHAR(150) NOT NULL UNIQUE,
      first_name VARCHAR(150) NOT NULL,
      last_name VARCHAR(150) NOT NULL,
      email VARCHAR(254) NOT NULL,
      is_staff BOOLEAN NOT NULL,
      is_active BOOLEAN NOT NULL,
      date_joined DATETIME NOT NULL
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("Table 'accounts_user' created successfully.")

except sqlite3.OperationalError as e:
    print(f"Error creating table: {e}. It might already exist.")

finally:
    if conn:
        conn.close()