import csv
import os
import logging
from tabulate import tabulate

# Function to read data from a CSV file
def read_csv_file(file_name):
    data = []  # List to store the read data from the CSV file
    unique_ids = set()  # Set to store unique IDs to check for duplicates

    with open(file_name, 'r') as file:
        csv_reader = csv.DictReader(file)
        row_number = 1
        for row in csv_reader:
            if row['id'] in unique_ids:  # Check if ID already exists in the set
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

# Function to display the menu options
def display_menu():
    print("\nPost Office Database Menu\n")
    print("1. Browse records")
    print("2. Add record")
    print("3. Amend record")
    print("4. Delete record")
    print("5. Display record")
    print("6. Exit\n")

# Function to log an error message
def log_error(error_msg):
    logging.basicConfig(filename='post_office.log', level=logging.ERROR)
    logging.error(error_msg)

# Function to find a record by ID
def find_record(data, id):
    """
    Find a record in the data list based on the provided ID.

    Args:
        data (list): List of record dictionaries.
        id (int): ID of the record to find.

    Returns:
        dict or None: Found record if available, else None.
    """
    for record in data:
        if int(record['id']) == id:
            return record
    return None

# Function to browse and display all records
def browse_records(data):
    """
    Display all records in a tabular format.

    Args:
        data (list): List of record dictionaries.
    """
    headers = data[0].keys()  # Extract the keys (column names) from the first record
    table_data = [row.values() for row in data]  # Extract the values (row data) from each record
    print(tabulate(table_data, headers=headers))

# Function to display a specific record by ID
def display_record(data, record_id=None):
    """
    Display a record based on the provided ID.

    Args:
        data (list): List of record dictionaries.
        record_id (int, optional): ID of the record to display. If not provided, the user is prompted for input.
    """
    if record_id == None:
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

# Function to validate the age field
def is_valid_age(age):
    """
    Validate the age field.

    Args:
        age (str): Age value to validate.

    Returns:
        bool: True if the age is valid, False otherwise.
    """
    return age.isdigit() and (0 < int(age) <= 120)

# Function to validate the email field
def is_valid_email(email):
    """
    Validate the email field.

    Args:
        email (str): Email value to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    return '@' in email and '.' in email

# Function to validate the phone field
def is_valid_phone(phone):
    """
    Validate the phone field.

    Args:
        phone (str): Phone value to validate.

    Returns:
        bool: True if the phone is valid, False otherwise.
    """
    return phone.isdigit() and len(phone) >= 10

# Function to input a value with validation
def input_with_validation(prompt, validation_func, error_msg):
    """
    Prompt the user for input and validate it using the provided validation function.

    Args:
        prompt (str): Prompt message to display.
        validation_func (function): Validation function to check the input.
        error_msg (str): Error message to display when input is invalid.

    Returns:
        str: Valid input value.
    """
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        print(error_msg)

# Function to add a new record
def add_record(data, file_name, new_record=None):
    """
    Add a new record to the data list.

    Args:
        data (list): List of record dictionaries.
        file_name (str): Name of the CSV file to write the updated data.
        new_record (dict, optional): New record to add. If not provided, the user is prompted for input.
    """
    if new_record == None:
        new_id = int(data[-1]['id']) + 1
        new_name = input("Enter new name: ")
        new_age = input_with_validation("Enter new age: ", is_valid_age, "Age must be a positive integer between 1 and 120.")
        new_street = input("Enter new street: ")
        new_city = input("Enter new city: ")
        new_record = {
            'id': str(new_id),
            'name': new_name,
            'age': new_age,
            'street': new_street,
            'city': new_city
        }
    data.append(new_record)
    write_csv_file(file_name, data)

# Function to write data to a CSV file
def write_csv_file(file_name, data):
    """
    Write the data to a CSV file.

    Args:
        file_name (str): Name of the CSV file to write.
        data (list): List of record dictionaries.
    """
    fieldnames = data[0].keys()
    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Main program execution
def main():
    file_name = 'post_office.csv'  # Name of the CSV file
    data = read_csv_file(file_name)  # Read data from the CSV file

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':  # Browse records
            browse_records(data)
        elif choice == '2':  # Add record
            add_record(data, file_name)
        elif choice == '3':  # Amend record
            pass
        elif choice == '4':  # Delete record
            pass
        elif choice == '5':  # Display record
            display_record(data)
        elif choice == '6':  # Exit
            print("\nExiting program.")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == '__main__':
    main()
