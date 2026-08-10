import os

import psycopg2

connection = psycopg2.connect(
    database=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host="localhost",
    port=5432,
)
cursor = connection.cursor()
with open("dictionary_entries_formated_cleaned.txt") as f:
    for line in f:
        a, b, c = "'a'", "'b'", "'c'"
        query = f"INSERT INTO dictionary_entry (header, reading, content) VALUES ({a}, {b}, {c});"  # nosec
        cursor.execute(query)

connection.commit()
connection.close()
