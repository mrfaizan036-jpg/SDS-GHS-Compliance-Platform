import sqlite3

DATABASE_PATH = "sds_ghs.db"

new_columns = {
    "hazard_class": "TEXT",
    "hazard_category": "TEXT",
    "signal_word": "TEXT",
    "pictograms": "TEXT",
    "hazard_statements": "TEXT",
    "precautionary_statements": "TEXT",
}


connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

cursor.execute("PRAGMA table_info(chemicals)")
existing_columns = {
    column[1]
    for column in cursor.fetchall()
}


for column_name, column_type in new_columns.items():

    if column_name not in existing_columns:
        cursor.execute(
            f"ALTER TABLE chemicals ADD COLUMN {column_name} {column_type}"
        )

        print(f"Added column: {column_name}")

    else:
        print(f"Column already exists: {column_name}")


connection.commit()
connection.close()

print("\nDatabase update completed successfully.")