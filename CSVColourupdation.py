import pandas as pd
import re
import json

# Load the CSV into a DataFrame
df = pd.read_csv('loropianadata.csv')

# Function to update the path in the JSON string based on conditions
def update_paths(json_str):
    samecolours = []
    if isinstance(json_str, str):
        original_str = json_str
        if re.search(r'Nougat', json_str) and json_str == "Natural Light Camel":
            json_str = "Cream"
            # print(f"replaced the item colour {json_str}")
        elif re.search(r'Mountain Rock', json_str):
            json_str = "Grey"
        elif re.search(r'Micro Stripes', json_str):
            if(json_str=="Micro Stripes Pale Sky"):
                json_str = "Blue"
            elif(json_str=="Azure Micro Stripes"):
                json_str = "Light Blue"
            elif(json_str=="Aqua Micro Stripes"):
                json_str = "light blue"
            else:
                json_str= "White"
        elif re.search(r'Melonpan', json_str):            
            if(json_str=="Melonpan+golden Joinery"):
                json_str = "Beige"
            else:
                json_str = "Champagne"    
        elif re.search(r'Green Tea Mochi', json_str):
            if(json_str=="Green Tea Mochi/turquoise Stone"):
                json_str = "Olive Green"
            elif(json_str=="Green Tea Mochi"):
                json_str = "light green"    
        elif re.search(r"Ginseng", json_str):
            if(json_str=="Ginseng"):
                json_str = "Beige"
            elif(json_str == "Ginseng+white"):
                json_str = "White"
            
            elif(json_str == "Ginseng/optical White"):
                json_str = "Champaigne"
            
            # specificcolour = len(json_str)
            # print(f"replaced the item colour {specificcolour}")
        elif(json_str == "Kokuto Sugar+ginseng"):
                json_str = "Beige"
        elif(json_str == "Golden Joinery"):
                json_str = "Beige"    
        elif json_str == "Rice Milk" :
            json_str = "White"
            # print(f"replaced the item colour {json_str}")
        elif json_str == "Black": 
            json_str
            
        elif json_str == "Caviar" or json_str == "Black/gray Melange" :
            json_str = "Black"
            print(f"replaced the item colour {json_str}")
        elif json_str == "Navy Blue":
            json_str= original_str
        elif json_str == "Navy Blue/gray Melange" :
            json_str = "Navy Blue"
            print(f"replaced the item colour {json_str}")
        elif json_str == "Rinse Wash":
            json_str = "Dark Blue"
            print(f"replaced the item colour {json_str}")
        elif json_str == "Optical White" :
            json_str = "White"
            print(f"replaced the item colour {json_str}")
        elif json_str == "kale" :
            json_str = "Olive Green"
            print(f"replaced the item colour {json_str}")
        elif json_str == "Kokuto Sugar" or json_str == "Manioc Root":
            json_str = "Red"
            # print(f"replaced the item colour {json_str}")
        elif json_str == "Plum Flower" or json_str == "Light Petal":
            json_str = "Light Pink"
            print(f"replaced the item colour {json_str}")
        elif json_str == "Landscape Green":
            json_str = "Dark Green"
            print(f"replaced the item colour {json_str}")
        elif json_str == "Rice Milk" or json_str == "White":
            json_str = "White"
        elif json_str == "Cocoa Truffle Melange":
            json_str = "Brown"
        if original_str != json_str:
            return json_str

    # Return None if no color was altered
    return None

            

    # return samecolours
        # elif re.search(r'Black', json_str):

            
        # if nougat_match:
        #     re.sub( json_str, "cream")
        # if match:
        #     value = match.group(1)
        #     print(value)
        # print("I am here")
        
    #     json_str = json_str.replace("'", '"')
    #     json_data = json.loads(json_str)
    #     print(json_data)
        
    #     for item in json_data:
    #         item['path'] = item['path'].replace('\\', '/')
            
    #         if 'WOMEN' in item['path']:
    #             item['path'] = item['path'].replace('WOMEN', 'women_clothing_items')
    #         elif item['path'].startswith('MEN'):
    #             item['path'] = item['path'].replace('MEN', 'men_clothing_items')
        
    # #     # Convert back to JSON string
    #     updated_json_str = json.dumps(json_data)
    #     return updated_json_str
    # else:
    #     print("Non-string value encountered:", json_str)
    #     return None

column_name = "ItemColour"

df[column_name] = df[column_name].apply(update_paths)
df.to_csv('new_and_improved_loropiana.csv', index=False)



def headerremoval(dataframe, column_name):
    # Filter the DataFrame to exclude rows where the column's value is not in the SubcatTitles list
    filtered_df = dataframe[dataframe[column_name].notna() & (dataframe[column_name] != '')]
    return filtered_df

additional_column_name = "ItemColour"

filtered_df = headerremoval(df, additional_column_name)
# Save the modified DataFrame to a new CSV file
df.to_csv('final_improved_loropiana.csv', index=False)
# Ensure the DataFrame looks like the desired format
# print(df[column_na
# me].tolist())