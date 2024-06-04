import os
import json



def updateJsonDataFormat():
    combinedData = {}
    # change the file path 
    json_file_path = "C:/Users/Hassan Ajmal/Desktop/Veeve data scraping/store-data-scraping/danubeData.json"
    try:
        # open the json file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for entry in data:
            category_title = entry["CategoryTitle"]
            subcategories = entry["Subcategories"]

            if category_title in combinedData:
                # Category already exists, append subcategories
                combinedData[category_title]["Subcategories"].extend(subcategories)
            else:
                # Category doesn't exist, create a new entry
                combinedData[category_title] = {
                    "CategoryTitle": category_title,
                    "Subcategories": subcategories
                }
        print(combinedData)
        combined_data_list = list(combinedData.values())
        # change the name of coverted output file if required
        output_file_path = 'formatedDanubeData.json'

# Serialize the combined data list and write it to the JSON file
        with open(output_file_path, 'w') as json_file:
            json.dump(combined_data_list, json_file, indent=4)
    except Exception as e:
        print("there was an error converting in json format")

updateJsonDataFormat()