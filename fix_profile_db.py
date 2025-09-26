import sqlite3

try:
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE accounts_profile (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL UNIQUE,
      photo VARCHAR(100) NULL,
      bio TEXT NULL,
      phone VARCHAR(20) NULL,
      dark_mode BOOLEAN NOT NULL,
      email_notifications BOOLEAN NOT NULL,
      FOREIGN KEY (user_id) REFERENCES accounts_user (id) ON DELETE CASCADE
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("Table 'accounts_profile' created successfully.")

except sqlite3.OperationalError as e:
    print(f"Error creating table: {e}. It might already exist.")

finally:
    if conn:
        conn.close()