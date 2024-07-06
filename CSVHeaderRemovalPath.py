import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("new_and_improved.csv")

# Define the list of valid subcategory titles
SubcatTitles = [
   'SUITS',
   'JACKETS | BLAZERS',
   'JEANS',
   'TROUSERS',
   'SHORTS',
   'POLO SHIRTS',
   'CO-ORD SETS',
   'T-SHIRTS',
   'SHIRTS',
   'LINEN',
   'SWIMWEAR',
   'SHORTS | SKORTS',
   'SKIRTS',
   'KNITWEAR',
   'WAISTCOATS',
   'DRESSES',
   'TOPS | BODYSUITS',
   'CO-ORD SETS',
   'Sweaters',
   'BLAZERS',
   ''
]

# Define the function to filter rows based on the SubcatTitles list
def headerremoval(dataframe, column_name):
    # Filter the DataFrame to exclude rows where the column's value is not in the SubcatTitles list
    filtered_df = dataframe[dataframe[column_name].isin(SubcatTitles)]
    return filtered_df

# Specify the column name to check against the SubcatTitles list
column_name_to_check = "subcategoryTitle"  # Replace with the actual column name in your CSV

# Apply the headerremoval function to the DataFrame
filtered_df = headerremoval(df, column_name_to_check)

# Save the filtered DataFrame back to a new CSV file
filtered_df.to_csv("zarastore_filtered.csv", index=False)

print("Filtered DataFrame saved to 'zarastore_filtered.csv'.")