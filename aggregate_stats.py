import pandas as pd

def aggregate_stats(csv_file, output_file):
    df = pd.read_csv(csv_file)
    # Remove unwanted columns
    df = df.drop(['Team', 'Place', 'Date'], axis=1)

    # Calculate wins and losses
    df['Win'] = df['Result'] == 'W'
    df['Loss'] = df['Result'] == 'L'
    # Group by Player and aggregate
    agg_dict = {
        'Win': 'sum',
        'Loss': 'sum',
        'Tries': 'sum',
        'Drops': 'sum',
        'Penalties': 'sum',
        'Conversions': 'sum',
        'Points': 'sum',
        'Pen_Cards': 'sum',
        'Minutes': 'sum',
    }
    grouped = df.groupby('Player', as_index=False).agg(agg_dict)
    grouped = grouped.rename(columns={'Win': 'Wins', 'Loss': 'Losses'})
    # Save to new CSV
    grouped.to_csv(output_file, index=False)

if __name__ == "__main__":
    aggregate_stats('stats.csv', 'stats_aggregated.csv')
