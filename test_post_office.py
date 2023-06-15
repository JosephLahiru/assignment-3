import unittest
import csv
import os
import post_office_management as pom

class TestPostOfficeManagement(unittest.TestCase):

    def setUp(self):
        self.data = pom.read_csv_file("post_office.csv")
        self.test_file = "test_post_office.csv"
        
        with open(self.test_file, 'w', newline='') as file:
            fieldnames = self.data[0].keys()
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(self.data)

    def test_find_record_existing_record(self):
        record = pom.find_record(self.data, 1)
        self.assertIsNotNone(record)
        self.assertEqual(record['name'], 'William')

    def test_find_record_non_existing_record(self):
        record = pom.find_record(self.data, 9999)
        self.assertIsNone(record)

    def test_add_record(self):
        new_record = {
            'id': len(self.data) + 1,
            'name': 'John',
            'age': '19',
            'street': 'Sigapor',
            'city': 'Sigapor',
            'postal_code': '3453',
            'country': 'Sn',
            'phone': '12345',
            'email': 'ss@gmail.com'
        }
        pom.add_record(self.data, self.test_file, new_record)
        added_record = pom.find_record(self.data, new_record['id'])
        self.assertIsNotNone(added_record)
        self.assertEqual(added_record['name'], new_record['name'])

    def test_amend_record(self):
        record_id = 4
        new_name = "Jane Smith"
        new_age = 20
        new_street = "New Street"
        new_city = "New City"
        new_postal_code = 9999
        new_country = "New Country"
        new_phone = 98765
        new_email = "jane@example.com"
        pom.amend_record(self.data, self.test_file, record_id, new_name, new_age, new_street, new_city, new_postal_code, new_country, new_phone, new_email)
        amended_record = pom.find_record(self.data, record_id)
        self.assertIsNotNone(amended_record)
        self.assertEqual(amended_record['name'], new_name)
        self.assertEqual(amended_record['age'], new_age)
        self.assertEqual(amended_record['street'], new_street)
        self.assertEqual(amended_record['city'], new_city)
        self.assertEqual(amended_record['postal_code'], new_postal_code)
        self.assertEqual(amended_record['country'], new_country)
        self.assertEqual(amended_record['phone'], new_phone)
        self.assertEqual(amended_record['email'], new_email)

    def test_delete_record(self):
        record_id = 1
        pom.delete_record(self.data, self.test_file, record_id)
        deleted_record = pom.find_record(self.data, record_id)
        self.assertIsNone(deleted_record)

    def tearDown(self):
        os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()
