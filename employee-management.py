import json
class Employee:
    def __init__(self, name,emp_id,depart,salary):
        self.name = name
        self.emp_id = emp_id
        self.depart = depart
        self.salary = salary
    def to_dict(self):
        return{
            "type": "Employee",
            "name": self.name,
            "emp_id": self.emp_id,
            "depart": self.depart,
            "salary": self.salary,
            }    
class Manager(Employee):
    def __init__(self, name, emp_id, depart, salary, responsibilities):
        super().__init__(name, emp_id, depart, salary)
        self.responsibilities = responsibilities
    def to_dict(self):
        data= super().to_dict()
        data["type"]="Manager"
        data["responsibilities"]= self.responsibilities
        return data    

class Company:
    def __init__(self, file_name = "employees.json"):
        self.employees=[]
        self.file_name = file_name
        self.load_data()
    def add_employee(self, emp):
        if any(e.emp_id == emp.emp_id for e in self.employees):
            raise ValueError("Employee ID already exists: ")
        else:
            self.employees.append(emp)
            self.save_data()
    def delete_employee(self, emp_id):
        for e in self.employees:
            if e.emp_id == emp_id:
                self.employees.remove(e)
                self.save_data()
                return
        raise ValueError("Employee ID not found: ")
    def show_employees(self):
        if not self.employees:
            print("No employees found. ")
            return
        for e in self.employees:
            print(e.to_dict())
    def update_employee(self, emp_id, **values):
        for e in self.employees:
            if e.emp_id == emp_id:
                e.name = values.get("name", e.name)
                e.depart = values.get("depart", e.depart)
                e.salary = values.get("salary", e.salary)
                if isinstance(e, Manager):
                    e.responsibilities = values.get("responsibilites", e.responsibilities)
                self.save_data()
                return
        raise ValueError("Employee ID not found: ")                



    def save_data(self):
        with open (self.file_name,'w') as f:
            json.dump([e.to_dict() for e in self.employees], f , indent=4)    
    def load_data(self):
        try:
            with open(self.file_name, 'r') as f:
                data=json.load(f)
                for emp in data:
                    if emp["type"]=="Manager":
                        self.employees.append(Manager(emp["name"], emp["emp_id"], emp["depart"], emp["salary"], emp["responsibilities"]))
                    else:
                        self.employees.append(Employee(emp["name"], emp["emp_id"], emp["depart"], emp["salary"]))
        except FileNotFoundError:
            print("File not found.")
            self.employees = []
def menu():
    company = Company()

    while True:
        print("*******Welcome to Virtual Soft*******")
        print("1. Add Employee")
        print("2. Add Manager")
        print("3. Show Employees")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")
        try:
            choice = int(input("Please enter your choice: "))
            if choice == 1:
                name= input("Enter employee name: ")
                emp_id = input("Please enter employee ID: ")
                depart = input("Please enter employee department: ")
                salary = float(input("Please enter employee salary: "))
                emp= Employee(name, emp_id, depart, salary)
                company.add_employee(emp)
                print("Employee added successfully.")
            elif choice == 2:
                name = input("Enter manager name: ")
                emp_id = input("Please enter manager ID: ")
                depart = input("Please enter manager department: ")
                salary = float(input("Please enter manager salary: "))
                responsibilities = input("Please enter manager responsibilities: ")
                mgr = Manager(name, emp_id, depart, salary, responsibilities)
                company.add_employee(mgr)
                print("Manager added successfully.")
            elif choice == 3:
                company.show_employees()
            elif choice == 4:
                emp_id = input("Please enter employee ID to update records: ")
                name = input("Please enter the new name of the employee or to keep the same name press enter: ")
                depart = input("Please enter the new department of the employee or to keep the same department press enter: ")
                salary = input("Please enter the new salary of the employee or to keep the same salary press enter: ")
                responsibilities = input("Please enter the new responsibilities of the manager or to keep the same responsibilities press enter: ")
                company.update_employee(
                    emp_id,
                    name=name or None,
                    depart=depart or None,
                    salary=float(salary) if salary else None,
                    responsibilities=responsibilities or None
                )  
                print("Employee Updated Successfully.")
            elif choice == 5:
                emp_id = input("please enter employee ID to delete: ")
                company.delete_employee(emp_id)
                print("Employee details deleted successfully. ")
            elif choice == 6:
                print("exiting the program. Good bye! ")
                break
            else:
                print("Invalid Choice Please try again. ")
        except ValueError as e:
            print(f"Error: {e}. Please Try Again. ")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again. ")
menu()  
                               