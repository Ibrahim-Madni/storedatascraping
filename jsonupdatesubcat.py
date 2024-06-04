# add image urls in subcategories
import os
import json
def update():
    storeData = "C:/Users/Hassan Ajmal/Downloads/FinalAlmeeraCatalogue.json"
    subcatJson = "C:/Users/Hassan Ajmal/Desktop/Veeve data scraping/store-data-scraping/subcategory.json"
    with open(storeData, 'r', encoding='utf-8') as file:
        json_data1 = json.load(file)
    with open(subcatJson, 'r', encoding='utf-8') as file:
        json_data2 = json.load(file)
    
    for category1 in json_data1:
        for subcategory1 in category1["Subcategories"]:
            subcategoryTitle1 = subcategory1["subcategoryTitle"]
            
            # Iterate through the second JSON data
            for subcategory2 in json_data2:
               
                subcategorybannerTitle2 = subcategory2["subcategorybannerTitle"]
                
                # If the subcategory titles match, add the image to the first JSON
                if subcategoryTitle1 == subcategorybannerTitle2:
                   
                    subcategory1["subcategorybannerImage"] = subcategory2["subcategorybannerImage"]
                
                    break
   
    output_file_path = 'sub_Cat.json'

        # Serialize the combined data list and write it to the JSON file
    with open(output_file_path, 'w') as file:
        json.dump(json_data1, file, indent=4)               

update()