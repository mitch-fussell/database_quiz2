import pandas as pd
import sqlite3

def csv_to_sqlite(csv_file, db_file, table_name):
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    csv_to_sqlite("stats_aggregated.csv", "springboks.db", "stats_aggregated")
