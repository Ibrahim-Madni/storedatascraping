import os
import csv
import pandas as pd
from supabase import create_client, Client
from datetime import datetime
import re


url: str = "https://bdaapulxwuqtaiddgwca.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJkYWFwdWx4d3VxdGFpZGRnd2NhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY4NzkzMjEsImV4cCI6MjAzMjQ1NTMyMX0.x7aob_dQrJ2tbnVwDW1dbxgrlsUShpmxSMyfAoFcNcc"
supabase: Client = create_client(url, key)
user = supabase.auth.sign_in_with_password({ "email":"ibrahim.madni@hotmail.com" ,   "password": "123456"})

if not user.user:
    raise Exception("Authentication failed")

user_id = user.user.id

def insert_data():
    currenttime = datetime.now().isoformat()
    # print(currenttime)
    insert_response = supabase.table("storedata").insert({"name": "Germany", "created_at":currenttime, "updated_at":currenttime}).execute()
    # # insert_response = supabase.table("todos").insert({"name": "Germany", "created_at":currenttime, "updated_at":currenttime}).execute()
    # # if insert_response.status_code == 201:
    print("Insert successful:", insert_response.data)
    # else:
    #     print("Insert operation failed:", insert_response.error_message)

# Function to select data from the 'todos' table
def select_data():
    select_response = supabase.table("storedata").select("*").execute()
    # if select_response.status_code == 200:
    print("Select successful:", select_response.data)
    # else:
    #     print("Select operation failed:", select_response.error_message)


def clean_price(price):
    # Remove unwanted characters like Â
    return price.replace('Â', '')

def update_data(file_path):
    data = []
    # select_response = supabase.table("storedata").select("*").execute()
    # data = select_response.data
    # Item_price = None
    
    # for item in data:
    #     item_price = item['ItemPrice']
    #     item_title = item['ItemTitle']
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            item_title = row['ItemTitle'] 
            item_price = re.sub(r'\s+', '', clean_price(row['ItemPrice']))
            select_response = supabase.table('storedata').select('*').eq('ItemTitle', item_title).execute()
            existing_items = select_response.data
            # print(existing_items[0])
            if existing_items:
                existing_item = existing_items[0]  # Assume there's only one matching item
                # print(existing_item)
                # print(existing_item['ItemPrice'])
                # item_id = existing_item['id']
                # print(item_id)
                # print(item_price)
                # print(f'database_title: {existing_item['ItemTitle']},  csv item title: {item_title}')
                # print(item_title)
                database_price = re.sub(r'\s+', '', existing_item['ItemPrice'])
                print(f'database price : {database_price}, csv item price : {item_price} ')
                if(existing_item['ItemTitle'] == item_title):
                    if database_price != item_price:
                          # Update the item price if it's different
                        try:
                            update_response= supabase.table('storedata').update({'ItemPrice': item_price}).eq('ItemTitle', item_title).execute()
                            print("Update successful:", update_response.data)
                            if update_response.data:
                                print("Update successful:", update_response.data)
                            else:
                                print("Update failed. No data returned:", update_response)
                        except Exception as e:
                            # Log the error details
                            print("Error updating the database:", e)
                    else:
                        print(f"'{item_title}' does not need price update")
                else:
                    print(f'Itemcsv title:{item_title} and databasetitle {existing_item['ItemTitle']} do not match')
            # if (row['ItemTitle'] == item_title):
            #     if(row['ItemPrice'] == item_price):
            #         break
            #     else:
            #         update_data= supabase.table('storedata').update({'ItemPrice': item_price}).eq('ItemTitle', item_title).execute()
            #         print("Select successful:", update_data.data)


    #     :
    #         print(row['ItemBrand'])
    #         print(row['ItemTitle'])


def main():
    csv_file_path = 'C:/Users/Ibrahim Madni/Desktop/data/StoreData/asosstore2_trimmed.csv'
    # data = pd.read_csv(csv_file_path)
    # print(data)
# Toggle between insert and select
    while True:
        operation = input("Enter 'insert' to insert data or 'select' to fetch data: ").strip().lower()

        if operation == "insert":
            insert_data()
        elif operation == "update":
            update_data(csv_file_path)
            data = pd.read_csv(csv_file_path)
        elif operation == "select":
            select_data()
        elif operation == "exit":
            print("exiting")
            break
        else:
            print("Invalid operation. Please enter either 'insert' or 'select'.")

        
if __name__ == "__main__":
    main()