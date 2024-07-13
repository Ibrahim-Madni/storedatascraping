import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("new_and_improved_asos.csv")

# Define the list of valid subcategory titles
SubcatTitles = [
   'Cargo Trousers',
   'Jorts',
   'Tracksuits & Joggers',
   'Blouses',
   'Blazers',
   'Waistcoats',
   'Jumpers & Cardigans',
   'Hoodies & Sweatshirts',
   'Coats & Jackets',
   'Trousers & Leggings',
   'Suits & Tailoring',
   'Shirts',
   'Jumpsuits & Playsuits',
   'Jeans',
   'T-Shirts & Vests',
   'Loungewear',
   'Co-ords',
   'Shorts',
   'Tops',
   'Dresses',
   'Skirts',
   'Polo shirts',
   'Joggers',
   'Tracksuits',
   'Jackets & Coats'


   
#    'SHORTS | SKORTS',
#    'SKIRTS',
#    'KNITWEAR',
#    'WAISTCOATS',
#    'DRESSES',
#    'TOPS | BODYSUITS',
#    'CO-ORD SETS',
#    'Sweaters',
#    'BLAZERS',
   ''
]

# Define the function to filter rows based on the SubcatTitles list
def headerremoval(dataframe, column_name):
    # Filter the DataFrame to exclude rows where the column's value is not in the SubcatTitles list
    filtered_df = dataframe[dataframe[column_name].isin(SubcatTitles)]
    return filtered_df

# Specify the column name to check against the SubcatTitles list
column_name_to_check = "SubcategoryName"  # Replace with the actual column name in your CSV

# Apply the headerremoval function to the DataFrame
filtered_df = headerremoval(df, column_name_to_check)

# Save the filtered DataFrame back to a new CSV file
filtered_df.to_csv("asos_filtered.csv", index=False)

print("Filtered DataFrame saved to 'asos_filtered.csv'.")