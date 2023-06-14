import csv

def display_menu():
    print("1. Browse Records")
    print("2. Add New Record")
    print("3. Amend Record")
    print("4. Delete Record")
    print("5. Display Record Details")
    print("0. Quit")

def read_records():
    records = []
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(row)
    return records

def write_records(records):
    with open('data.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Name', 'Age', 'Email'])
        writer.writeheader()
        writer.writerows(records)

def browse_records():
    records = read_records()
    for record in records:
        print(record)

def add_record():
    name = input("Enter Name: ").strip()
    age = input("Enter Age: ").strip()
    email = input("Enter Email: ").strip()

    if not name or not age or not email:
        print("Invalid input. Please enter all fields.")
        return

    try:
        age = int(age)
    except ValueError:
        print("Invalid input. Age must be a number.")
        return

    record = {'Name': name, 'Age': age, 'Email': email}
    records = read_records()
    records.append(record)
    write_records(records)
    print("Record added successfully!")

def amend_record():
    name = input("Enter Name of the record to amend: ").strip()
    if not name:
        print("Invalid input. Please enter a name.")
        return

    records = read_records()
    record_found = False

    for record in records:
        if record['Name'] == name:
            new_age = input("Enter new Age: ").strip()
            new_email = input("Enter new Email: ").strip()

            if not new_age or not new_email:
                print("Invalid input. Please enter all fields.")
                return

            try:
                new_age = int(new_age)
            except ValueError:
                print("Invalid input. Age must be a number.")
                return

            record['Age'] = new_age
            record['Email'] = new_email
            write_records(records)
            print("Record amended successfully!")
            record_found = True
            break

    if not record_found:
        print("Record not found!")

def delete_record():
    name = input("Enter Name of the record to delete: ").strip()
    if not name:
        print("Invalid input. Please enter a name.")
        return

    records = read_records()
    record_found = False

    for record in records:
        if record['Name'] == name:
            records.remove(record)
            write_records(records)
            print("Record deleted successfully!")
            record_found = True
            break

    if not record_found:
        print("Record not found!")

def display_record_details():
    name = input("Enter Name of the record to display details: ").strip()
    if not name:
        print("Invalid input. Please enter a name.")
        return

    records = read_records()
    record_found = False

    for record in records:
        if record['Name'] == name:
            print(record)
            record_found = True
            break

    if not record_found:
        print("Record not found!")

while True:
    display_menu()
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        browse_records()
    elif choice == '2':
        add_record()
    elif choice == '3':
        amend_record()
    elif choice == '4':
        delete_record()
    elif choice == '5':
        display_record_details()
    elif choice == '0':
        break
    else:
        print("Invalid choice. Please try again.")
