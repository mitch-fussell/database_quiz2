import pandas as pd
import sqlite3
import re

def split_name(name):
    # Handles names like "Jean KLEYN", "Pieter-Steph DU TOIT", "Ben-Jason DIXON"
    parts = name.strip().split()
    if len(parts) == 1:
        return parts[0], ''
    # If last part is all uppercase, treat as last name
    if parts[-1].isupper():
        return ' '.join(parts[:-1]), parts[-1]
    # Otherwise, last word is last name
    return ' '.join(parts[:-1]), parts[-1]

def update_bio():
    df = pd.read_csv('bio.csv')
    df[['FirstName', 'LastName']] = df['Name'].apply(lambda x: pd.Series(split_name(x)))
    cols = ['FirstName', 'LastName'] + [c for c in df.columns if c not in ['Name', 'FirstName', 'LastName']]
    df = df[cols]
    df.to_csv('bio.csv', index=False)
    # Update DB
    conn = sqlite3.connect('springboks.db')
    df.to_sql('bio', conn, if_exists='replace', index=False)
    conn.close()

def update_stats():
    df = pd.read_csv('stats.csv')
    if 'Player' in df.columns:
        df[['FirstName', 'LastName']] = df['Player'].apply(lambda x: pd.Series(split_name(x)))
        cols = ['FirstName', 'LastName'] + [c for c in df.columns if c not in ['Player', 'FirstName', 'LastName']]
        df = df[cols]
        df.to_csv('stats.csv', index=False)
        # Update DB
        conn = sqlite3.connect('springboks.db')
        df.to_sql('stats', conn, if_exists='replace', index=False)
        conn.close()

def main():
    update_bio()
    update_stats()

if __name__ == "__main__":
    main()
