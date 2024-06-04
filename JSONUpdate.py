import json
import os
from urllib.parse import urlparse

def update_json_data():
    # Load the JSON data
    json_file_path = "C:/Users/Cowlar/Desktop/Veeve Data Scraping/StoreData/CorrectEdekaData.json"
    images_directory = "C:/Users/Cowlar/Desktop/Veeve Data Scraping/StoreData/Images"
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create a dictionary to map the image section of the URL to local file paths
    common_path_prefix = os.path.commonpath([images_directory])
    url_section_to_path_mapping = {}
    # print(url_section_to_path_mapping)
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
                
                # Remove file extension to get the URL section
                url_section = url_section.replace(common_path_prefix, '', 1).lstrip('/')

                # Remove file extension to get the URL section
                url_section = os.path.splitext(url_section)[0]

                url_section_to_path_mapping[file_name] = url_section
                print(f"Jey in DIck: {url_section_to_path_mapping[file_name]}")
                # print(f"Number of items in dictionary: {len(url_section_to_path_mapping)}")
                # print(url_section_to_path_mapping)
                # print(local_path)
                # print(url_section_to_path_mapping)
                # if url_section in url_section_to_path_mapping:
                #     url_section_to_path_mapping[url_section] = local_path
                #     dict_count += 1  # Increment the counter for each new dictionary entry
                #     print(f"Added entry {dict_count} to dictionary: {url_section}")
    # print(f"Total files processed: {file_count}")
                # print(f"Total dictionary entries: {dict_count}")
    # print(url_section_to_path_mapping)
                # print(url_section_to_path_mapping)
    # Iterate through the data and add a new key-value pair to each entry
     
    # print(url_section_to_path_mapping)
    for entry in data:
        # Check if the current entry contains 'Subcategories'
        # print(entry)
        if 'Subcategories' in entry:
            category_title = entry['CategoryTitle']
            subcategories = entry['Subcategories']

            # Iterate through subcategories
            for subcategory in subcategories:
                subcategory_title = subcategory['subcategoryTitle']
                product_items = subcategory.get('productItems', [])

                # Iterate through product items
                for item_object in product_items:
                    # print(item_object)
                    if 'image_urls' in item_object:
                        
                        # print("Processing item object:", item_object.get('ItemTitle', 'Unknown Item'))

                        # Iterate through the 'image_urls' of the current item object
                        for index, url in enumerate(item_object['image_urls']):
                            # print(url)
                            # Extract the endpoint of the URL (the part after the last '/')
                            url_endpoint = urlparse(url).path.split('/')[-1]
                            url_endpoint = url_endpoint.replace("\\", "/")
                            
                            # print(url_endpoint)
                        # print(url_section_to_path_mapping)

                        if url_endpoint in url_section_to_path_mapping:
                        # Use the URL endpoint as the key to retrieve the local path
                            # print(url_endpoint)
                            local_image_path = url_section_to_path_mapping[url_endpoint]
                            local_image_path = local_image_path.replace('\\', '/')
                            item_object['local_image_path'] = local_image_path
                            # print(f"Added new key-value pair: 'local_image_path': {item_object['local_image_path']}")

                            # else:
                            #     print(f"url_endpoint '{url_endpoint}' not found in url_section_to_path_mapping")
                            # print(url_endpoint)

                            # Extract the section from the URL (e.g., "bacardi-cartablanca")
                #             url_section = os.path.splitext(url_endpoint)[0]
                #             # print(url_section)
                #             relevant_part = url_section.split('_')[0]

                #             # print(f"Relevant part: {relevant_part}")
                #             # print(f"URL section: {*-on}")
                #             # print(f"its a me:{url_section_to_path_mapping}")
                # keys = url_section_to_path_mapping.keys()
                # for keys in keys:
                #     print(keys)
                            # Check if the URL section exists in the mapping
                            # local_image_path = os.path.basename(url_section_to_path_mapping[url_section])
                            # print(local_image_path)
                #             # print*
                #             if relevant_part in url_section_to_path_mapping:
                # # If a match is found, use the matching key to retrieve the local path
                #                 print("am I here")
                #                 matched_key = relevant_part
                #                 entry['local_image_path'] = url_section_to_path_mapping[matched_key]
                #                 print(f"Added new key-value pair: 'local_image_path': {entry['local_image_path']}")
                            # if url_section in url_section_to_path_mapping:
                            #     entry['local_image_path'] = url_section_to_path_mapping[url_section]
                            #     print(f"Added new key-value pair: 'local_image_path': {entry['local_image_path']}")
    # Save the modified data back to the JSON file
        print("Successfully done adding new key-value pairs.")
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            # print("Really done tho?.")


# Call the function to update JSON data with new key-value pairs
update_json_data()
