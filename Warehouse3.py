import ast
import os

class Manager:
    def __init__(self):
        # Initialize state
        self.balance = 0.0
        self.warehouse = {}
        self.operations = []

        self.tasks = {
            "balance": self.balance_task,
            "sale": self.sale_task,
            "purchase": self.purchase_task,
            "account": self.account_task,
            "list": self.list_task,
            "warehouse": self.warehouse_task,
            "review": self.review_task,
            "end": self.end_task
        }

        self.running = True

    def record_operation(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if result:
                self.operations.append(result)
            return result
        return wrapper

    def require_funds(func):
        def wrapper(self, *args, **kwargs):
            total = kwargs.get('total', 0)
            if total > self.balance:
                print("Insufficient funds for this purchase.")
                return None
            return func(self, *args, **kwargs)
        return wrapper

    @record_operation
    def balance_task(self):
        try:
            amount = float(input("Enter amount to add/subtract: "))
            self.balance += amount
            return f"Balance changed by {amount}, new balance: {self.balance}"
        except ValueError:
            print("Invalid amount! Please enter a valid number.")

    @record_operation
    def sale_task(self):
        product = input("Enter product name: ").strip()
        try:
            price = float(input("Enter price per unit: "))
            quantity = int(input("Enter quantity: "))
            if product not in self.warehouse or self.warehouse[product]['quantity'] < quantity:
                print("Not enough stock for this sale.")
                return None
            total = price * quantity
            self.balance += total
            self.warehouse[product]['quantity'] -= quantity
            return f"Sold {quantity} of {product} at {price} each. Total: {total}"
        except ValueError:
            print("Invalid input!")

    @record_operation
    @require_funds
    def purchase_task(self, total=0):
        product = input("Enter product name: ").strip()
        try:
            price = float(input("Enter price per unit: "))
            quantity = int(input("Enter quantity: "))
            total = price * quantity
            kwargs = {'total': total}
            if total > self.balance:
                print("Insufficient funds for this purchase.")
                return None
            self.balance -= total
            if product not in self.warehouse:
                self.warehouse[product] = {'price': price, 'quantity': quantity}
            else:
                self.warehouse[product]['quantity'] += quantity
                self.warehouse[product]['price'] = price
            return f"Purchased {quantity} of {product} at {price} each. Total: {total}"
        except ValueError:
            print("Invalid input! Price and quantity must be numbers.")

    def account_task(self):
        print(f"Current account balance: {self.balance}")

    def list_task(self):
        if not self.warehouse:
            print("Warehouse is empty.")
        else:
            print("Warehouse Inventory:")
            for product, details in self.warehouse.items():
                print(f"{product}: {details['quantity']} units, Price: {details['price']}")

    def warehouse_task(self):
        product = input("Enter product name: ").strip()
        if product in self.warehouse:
            details = self.warehouse[product]
            print(f"{product}: {details['quantity']} units, Price: {details['price']}")
        else:
            print(f"{product} not found in warehouse.")

    def review_task(self):
        try:
            from_idx = input("Enter start index: ")
            to_idx = input("Enter end index: ")
            start = int(from_idx) if from_idx else 0
            end = int(to_idx) if to_idx else len(self.operations)
            if start < 0 or end > len(self.operations) or start > end:
                print("Invalid index range.")
            else:
                for op in self.operations[start:end]:
                    print(op)
        except ValueError:
            print("Invalid index. Please enter valid integers.")

    def end_task(self):
        print("Exiting program...")
        self.running = False

    def assign(self, task_name):
        task = self.tasks.get(task_name)
        if task:
            task()
        else:
            print("Invalid command!")

def main():
    manager = Manager()

    while manager.running:
        print("\nCommands: balance, sale, purchase, account, list, warehouse, review, end")
        cmd = input("Enter command: ").strip().lower()
        manager.assign(cmd)

if __name__ == "__main__":
    main()