from customer import Customer  # Adjust this import based on your actual file structure

class TestCustomer:
    def test_customer_creation(self):
        print('Test Case 1: Can create a new Customer instance')
        customer = Customer(id='999999999', name='John Doe', dob='01-01-1980', pin='1234', pay_method='Visa', days_purchased=12)
        assert (customer.id, customer.name, customer.dob, customer.pin, customer.pay_method, customer.days_purchased) == \
               ('999999999', 'John Doe', '01-01-1980', '1234', 'Visa', 12)

    def test_customer_default_id(self):
        print('Test Case 2: Customer ID defaults to a random value if not provided')
        customer = Customer(name='Jane Doe', dob='02-02-1980', pin='5678', pay_method='MasterCard', days_purchased=5)
        assert customer.id is not None, "Customer ID should be automatically generated"

    def test_invalid_dob(self):
        print('Test Case 3: Test invalid date of birth format')
        customer = Customer(name='Jane Doe', dob='1980-02-02', pin='5678', pay_method='MasterCard', days_purchased=5)
        assert customer.dob == '1980-02-02', "Customer DOB should match the input, even if format is incorrect"

    def test_customer_without_payment_method(self):
        print('Test Case 4: Test customer creation without specifying a payment method')
        customer = Customer(name='Alice', dob='03-03-1980', pin='4321', days_purchased=3)
        assert customer.pay_method == 'Unknown', "Default payment method should be 'Unknown'"

if __name__ == "__main__":
    test_customer = TestCustomer()
    test_customer.test_customer_creation()
    test_customer.test_customer_default_id()
    test_customer.test_invalid_dob()
    test_customer.test_customer_without_payment_method()