import pandas as pd
import json

# Load the CSV into a DataFrame
df = pd.read_csv('asos_filtered.csv')

# Function to update the path in the JSON string based on conditions
def update_paths(json_str):
    # print(json_str)
    if isinstance(json_str, str):
        print("I am here")
        json_str = json_str.replace("'", '"')
        json_data = json.loads(json_str)
        # print(json_data)
        
        for item in json_data:
            item['path'] = item['path'].replace('\\', '/')
            
            item['path'] += '.png'
        
    #     # Convert back to JSON string
        updated_json_str = json.dumps(json_data)
        return updated_json_str
    else:
        print("Non-string value encountered:", json_str)
        return None

column_name = "images"

df[column_name] = df[column_name].apply(update_paths)

# Save the modified DataFrame to a new CSV file
df.to_csv('pngextensionadded_asos.csv', index=False)
# Ensure the DataFrame looks like the desired format
# print(df[column_name].tolist())