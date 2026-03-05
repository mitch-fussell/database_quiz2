import pandas as pd
import sqlite3

def csv_to_sqlite(csv_file, db_file, table_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_file)
    # Write the data to the specified table
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    csv_to_sqlite("bio.csv", "springboks.db", "bio")
    csv_to_sqlite("stats.csv", "springboks.db", "stats")
