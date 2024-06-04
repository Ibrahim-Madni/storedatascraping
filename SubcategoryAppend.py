import json

def combine_data(data):
    combined = {}
    
    for entry in data:
        category_title = entry['CategoryTitle']
        subcategories = entry['Subcategories']
        
        if category_title not in combined:
            combined[category_title] = {"CategoryTitle": category_title, "Subcategories": []}
        
        for subcategory in subcategories:
            subcategory_title = subcategory['subcategoryTitle']
            product_items = subcategory['productItems']
            
            # Check if the subcategory already exists within the category
            existing_subcategory = None
            for sc in combined[category_title]["Subcategories"]:
                if sc['subcategoryTitle'] == subcategory_title:
                    existing_subcategory = sc
                    break
            
            # If it exists, append the product items; if not, create a new subcategory
            if existing_subcategory:
                existing_subcategory['productItems'].extend(product_items)
            else:
                combined[category_title]["Subcategories"].append(subcategory)
    
    # Transforming combined data back to list format
    return list(combined.values())

def main():
    input_file_path = 'C:/Users/Hassan Ajmal/Desktop/Veeve data scraping/store-data-scraping/formattedData.json'  # Provide your input file path here
    output_file_path = 'combined_data.json'
    
    try:
        # Load data
        with open(input_file_path, 'r') as infile:
            data = json.load(infile)
        
        # Combine data
        new_data = combine_data(data)
        
        # Write combined data to new JSON file
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            json.dump(new_data, outfile, ensure_ascii=False, indent=4)
        print(f"Combined data written to: {output_file_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()