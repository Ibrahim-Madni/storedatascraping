import os
import json
import magic
from PIL import Image
from urllib.parse import urlparse

def convert_to_jpg_if_needed(image_path):
    try:
        img = Image.open(image_path)
        new_image_path = os.path.splitext(image_path)[0] + '.jpg'
        img.save(new_image_path, "JPEG")
        os.remove(image_path)
        return new_image_path
        
        
    except Exception as e:
        print(f"Error converting image to JPG: {e} image path {image_path}")
    
    return image_path

def update_json_data():
    #add path of the json data and images folder here
    json_file_path = "C:/Users/Hassan Ajmal/Desktop/Veeve data scraping/store-data-scraping/danubeData.json"
    images_directory = "C:/Users/Hassan Ajmal/Desktop/Veeve data scraping/store-data-scraping/Images"
    

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create a dictionary to map the image section of the URL to local file paths
    common_path_prefix = os.path.commonpath([images_directory])
    url_section_to_path_mapping = {}
    
    # Traverse the images_directory and build the mapping
    file_count = 0  # Initialize a counter outside the loop
    dict_count = 0
    
    for root, _, files in os.walk(images_directory):
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_count += 1  # Increment the counter for each image file
                print(f"Processing file {file_count}: {file_name}")
                
                local_path = os.path.join(root, file_name)
               
                
                
                # Extract the relative path from the images_directory
                relative_path = os.path.relpath(local_path, start=images_directory)
                
                # Use the relative path as the URL section
                # Convert the relative path to use forward slashes (for Windows)
                url_section = relative_path.replace(os.path.sep, '/')
                

                url_section_to_path_mapping[file_name] = url_section
                print(f"Key in Dictionary: {url_section_to_path_mapping[file_name]}")
            else: 
                file_count += 1
                print(f"Processing file {file_count}: {file_name}")
                local_path = os.path.join(root, file_name)
                local_path = convert_to_jpg_if_needed(local_path)
                print(f"localPath : {local_path}")
                
                # Extract the relative path from the images_directory
                relative_path = os.path.relpath(local_path, start=images_directory)
                # Convert the relative path to use forward slashes (for Windows)
                url_section = relative_path.replace(os.path.sep, '/')
                url_section_to_path_mapping[file_name] = url_section

    # Iterate through the data and add a new key-value pair to each entry
    for entry in data:
        if 'Subcategories' in entry:
            # might need this is future
            # category_title = entry['CategoryTitle']
            subcategories = entry['Subcategories']

            for subcategory in subcategories:
                # might need this in future
                # subcategory_title = subcategory['subcategoryTitle']
                product_items = subcategory.get('productItems', [])

                for item_object in product_items:
                    if 'image_urls' in item_object:
                        
                        # for index, url in enumerate(item_object['image_urls']):
                        url_endpoint = urlparse(item_object['image_urls']).path.split('/')[-1]
                        url_endpoint = url_endpoint.replace("\\", "/")

                        if url_endpoint in url_section_to_path_mapping:
                            local_image_path = url_section_to_path_mapping[url_endpoint]
                            local_image_path = local_image_path.replace('\\', '/')
                            item_object['local_image_path'] = local_image_path

    # Save the modified data back to the JSON file
    print("Successfully done adding new key-value pairs.")
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Call the function to update JSON data with new key-value pairs and convert images to jpg if needed
update_json_data()
