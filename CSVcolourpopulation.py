import pandas as pd

# Read the CSV file
df = pd.read_csv('asos_filtered.csv')

# Process the dataframe
def split_itemname_and_fill_color(row):
    if pd.isna(row['ItemColour']):
        parts = row['ItemTitle'].split()
        if parts:
            row['ItemColour'] = parts[-1]
    return row

df = df.apply(split_itemname_and_fill_color, axis=1)

# Save the updated dataframe to a new CSV file
df.to_csv('finalasosdata.csv', index=False)

print("CSV file has been processed and saved.")