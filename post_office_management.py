import csv
import os
import logging
from tabulate import tabulate

# Function to read the CSV file and store unique records in the data list
def read_csv_file(file_name):
    data = []
    unique_ids = set()

    # Read the CSV file and check for duplicate IDs and corrupt data
    with open(file_name, 'r') as file:
        csv_reader = csv.DictReader(file)
        row_number = 1
        for row in csv_reader:
            if row['id'] in unique_ids:
                log_error(f"Duplicate ID found for row {row_number}: {row}")
            else:
                if (is_valid_age(row['age']) and
                    is_valid_email(row['email']) and
                    is_valid_phone(row['phone'])):
                    data.append(row)
                    unique_ids.add(row['id'])
                else:
                    log_error(f"Corrupt data found for row {row_number}: {row}")
            row_number += 1
    return data

# Function to display the main menu
def display_menu():
    print("\nPost Office Database Menu\n")
    print("1. Browse records")
    print("2. Add record")
    print("3. Amend record")
    print("4. Delete record")
    print("5. Display record")
    print("6. Exit\n")

# Function to log errors to a log file
def log_error(error_msg):
    logging.basicConfig(filename='post_office.log', level=logging.ERROR)
    logging.error(error_msg)

# Function to find a record by ID in the data list
def find_record(data, id):
    for record in data:
        if int(record['id']) == id:
            return record
    return None

# Function to browse and display all records in a table format
def browse_records(data):
    headers = data[0].keys()
    table_data = [row.values() for row in data]
    print(tabulate(table_data, headers=headers))

# Function to display a specific record by ID
def display_record(data, record_id=None):
    if(record_id==None):
        id = int(input("Enter the record ID to display: "))
    else:
        id = record_id

    record = find_record(data, id)
    if record:
        headers = record.keys()
        table_data = [record.values()]
        print(tabulate(table_data, headers=headers))
    else:
        print("\nRecord not found.\n")
        log_error(f"Record not found for ID: {id}")

# Function to validate age
def is_valid_age(age):
    return age.isdigit() and (0 < int(age) <= 120)

# Function to validate email
def is_valid_email(email):
    return '@' in email and '.' in email

# Function to validate phone number
def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10

# Function to input data with validation
def input_with_validation(prompt, validation_func, error_msg):
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        print(error_msg)

# Function to add a new record to the data list and CSV file
def add_record(data, file_name, new_record=None):
    # If new_record is not provided, ask for input
    if(new_record==None):
        new_id = int(data[-1]['id']) + 1
        new_name = input("Enter new name: ")
        new_age = input_with_validation("Enter new age: ", is_valid_age, "Age must be a positive integer between 1 and 120.")
        new_street = input("Enter new street: ")
        new_city = input("Enter new city: ")
        new_postal_code = input("Enter new postal code: ")
        new_country = input("Enter new country: ")
        new_phone = input_with_validation("Enter new phone: ", is_valid_phone, "Phone number must be all digits and contain at least 10 digits.")
        new_email = input_with_validation("Enter new email: ", is_valid_email, "Email must be in a valid format (e.g., user@example.com).")

        new_record = {
            'id': new_id,
            'name': new_name,
            'age': new_age,
            'street': new_street,
            'city': new_city,
            'postal_code': new_postal_code,
            'country': new_country,
            'phone': new_phone,
            'email': new_email
        }

    # Add the new_record to the data list and update the CSV file
    data.append(new_record)
    with open(file_name, 'w', newline='') as file:
        fieldnames = data[0].keys()
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)

    print("\nRecord added successfully.\n")

# Function to amend a specific record in the data list and CSV file
def amend_record(data, file_name, record_id=None, _new_name=None, _new_age=None, _new_street=None, _new_city=None, _new_postal_code=None, _new_country=None, _new_phone=None, _new_email=None):
    if(record_id==None):
        id = int(input("Enter the record ID to amend: "))
    else:
        id = record_id

    record = find_record(data, id)
    if record:
        # If new values are not provided, ask for input
        if(_new_name==None or _new_age==None or _new_street==None or _new_city==None or _new_postal_code==None or _new_country==None or _new_phone==None or _new_email==None):
            new_name = input(f"Enter new name ({record['name']}): ")
            new_age = input_with_validation(f"Enter new age ({record['age']}): ", is_valid_age, "Age must be a positive integer between 1 and 120.")
            new_street = input(f"Enter new street ({record['street']}): ")
            new_city = input(f"Enter new city ({record['city']}): ")
            new_postal_code = input(f"Enter new postal code ({record['postal_code']}): ")
            new_country = input(f"Enter new country ({record['country']}): ")
            new_phone = input_with_validation(f"Enter new phone ({record['phone']}): ", is_valid_phone, "Phone number must be all digits and contain at least 10 digits.")
            new_email = input_with_validation(f"Enter new email ({record['email']}): ", is_valid_email, "Email must be in a valid format (e.g., user@example.com).")
            
        else:
            new_name = _new_name
            new_age = _new_age
            new_street = _new_street
            new_city = _new_city
            new_postal_code = _new_postal_code
            new_country = _new_country
            new_phone = _new_phone
            new_email = _new_email

        # Update the record with new values
        record['name'] = new_name or record['name']
        record['age'] = new_age or record['age']
        record['street'] = new_street or record['street']
        record['city'] = new_city or record['city']
        record['postal_code'] = new_postal_code or record['postal_code']
        record['country'] = new_country or record['country']
        record['phone'] = new_phone or record['phone']
        record['email'] = new_email or record['email']

        # Update the CSV file with the amended record
        with open(file_name, 'w', newline='') as file:
            fieldnames = data[0].keys()
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(data)

        print("\nRecord amended successfully.\n")
    else:
        print("\nRecord not found.\n")
        log_error(f"Record not found for ID: {id}")

# Function to delete a specific record from the data list and CSV file
def delete_record(data, file_name, record_id=None):
    if(record_id==None):
        id = int(input("Enter the record ID to delete: "))
    else:
        id = record_id

    record = find_record(data, id)
    if record:
        data.remove(record)

        # Update the CSV file after deleting the record
        with open(file_name, 'w', newline='') as file:
            fieldnames = data[0].keys()
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(data)

        print("\nRecord deleted successfully.\n")
    else:
        print("\nRecord not found.\n")
        log_error(f"Record not found for ID: {id}")

# Main program loop
def main():
    file_name = 'post_office.csv'
    data = read_csv_file(file_name)

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            browse_records(data)
        elif choice == '2':
            add_record(data, file_name)
        elif choice == '3':
            amend_record(data, file_name)
        elif choice == '4':
            delete_record(data, file_name)
        elif choice == '5':
            display_record(data)
        elif choice == '6':
            search_records(data)
        elif choice == '7':
            print("\nExiting the program...\n")
            break
        else:
            print("\nInvalid choice. Please try again.\n")
            log_error(f"Invalid menu choice: {choice}")

# Function to search records based on a keyword
def search_records(data, keyword=None):
    if(keyword==None):
        keyword = input("Enter the keyword to search: ").lower()
    else:
        keyword = keyword.lower()

    found_records = []

    for record in data:
        for key, value in record.items():
            if keyword in str(value).lower():
                found_records.append(record)
                break

    if found_records:
        print("\nFound records:\n")
        display_records(found_records)
    else:
        print("\nNo records found with the given keyword.\n")
        log_error(f"No records found with keyword: {keyword}")

if __name__ == '__main__':
    main()
