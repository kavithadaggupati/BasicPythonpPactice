
#######################
# Bank loan System
#######################
#Features:
#1. Apply For The Loan : Check salary, calculate loan, EMI and Tenure
#2. Pay EMI            : pay monthly EMI and Update balance
#3. clear Loan         : clear loan fully or partially
#4. View History       : see all past payments, balance and salary
#5. Data Saved         : loans stored in loans.json file

import json
from datetime import datetime
import os

FILE = "loans.json"

MIN_SALARY = 20000

def load_data():
    if not os.path.exists(FILE):
        return[]
    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return[]

def safe_date_input(msg):
    while True:
        date_str = input(msg)
        try:
            datetime.strptime(date_str,"%d-%m-%Y")
            return date_str
        except ValueError:
            print("Invalid date format.\n")
def next_due(start_date):
    d = datetime.strptime(start_date,"%d-%m-%Y")
    if d.month == 12:
        next = d.replace(year = d.year + 1, month = 1)
    else:
        nxt = d.replace(month = d.month +1)
    return nxt.strptime("%d-%m-%Y")

def generate_id(data):
    if not data:
        return 
    max_id = max(loan["loan_id"]for loan in data)
    return max_id + 1

def save_data(data):
    with open(FILE ,"w" )as f:
        json.dump(data,f,indent=2)

def find_loan(data,loan_id):
    for loan in data:
        if loan["loan_id"] == loan_id:
            return loan
    return None


def apply_loan(data):
    name = input("Enter your name:")

    try:
        salary = int(input("Enter your monthly salary:"))
    except ValueError:
        print("Invalid Salary Amount.")
        return
    
    if salary <= MIN_SALARY:
        print(f"Salary must be more than {MIN_SALARY} to get a loan.")
        return
    loan_amt = salary * 10
    emi = int(salary * 0.10)
    months = loan_amt // emi
    print(f"congrats {name}! you are eligible.")
    print(f"LoanAmount : {loan_amt}")
    print(f"EMI: {emi}")
    print(f"Tenure: {months}")

    confirm = input("Do you want to Proceed?(yes/no):").lower()
    if confirm != "yes":
        print("Loan cancelled.\n")

    start_date = safe_date_input("Enter loan start date(dd-mm-yyyy):")

    first_due = next_due(start_date)

    loan_id = generate_id(data)

    record = {
            "loan_id" : loan_id ,
            "name"    : name,
            "salary"  : salary,
            "loan_amount" : loan_amt ,
            "emi"     : emi,
            "tenure"  : months,
            "balance" : loan_amt,
            "status"  :  "ongoing",
            "next_due" : first_due,
            "history"  : [] 
              }

    data.append(record)
    save_data(data)
    print(f"loan approved.Your loan_id: {loan_id}")


def pay_emi(data):
    try:
        loan_id = int(input("Enter your loan_id:"))
    except ValueError:
        print("Invalid loan id.\n")
        return
    loan = find_loan(data,loan_id)
    if not loan:
        print("Loan not found.\n")
        return
    if loan["status"] == "cleared":
        print("loan already cleared.\n")
        return
    print(f"Next emi due: {loan["next_due"]}")

    try:
        amt = int(input(f"Enter emi:({loan["emi"]})"))
    except ValueError:
        print("Invalid amount.\n")
        return
    if amt != loan["emi"]:
        print(f"Wrong emi amount, expected({loan["emi"]}),got{amt}")
        return
    loan["balance"] -= amt
    loan["tenure"] -= 1
    loan["history"].append({"date": loan["next_due"],"amount": amt})
    loan["next_due"] = next_due(loan["next_due"])

    if loan["balance"] <= 0:
        loan["status"] = "cleared"
        loan["balance"] = 0
        loan["tenure"] = 0
        print("Loan cleared!")
    else:
        print(f"EMI paid,balance amount:{loan["balance"]}\n remaining tenure:{loan["tenure"]}months.\n")

    save_data(data)
def clear_loan(data):
    try:
        loan_id = int(input("Enter your loan_id:"))
    except ValueError:
        print("Invalid loan id.\n")
        return
    
    loan = find_loan(data,loan_id)

    if not loan:
         print("Loan not found.\n")
         return
    if loan["status"] == "cleared":
         print("loan already cleared.\n")
         return
    print(f"balance left:{loan["balance"]}")

    try:
        amt = int(input("enter amount to clear(full/partial):"))
    except ValueError:
        print("Invalid amount,\n")
        return

    if amt == loan["balance"]:
        pay_date = safe_date_input("Enter payment date(dd-mm-yyyy):")
        loan["history"].append({"date":pay_date, "amount":amt})

        loan["status"] = "cleared"
        loan["balance"] = 0
        loan["tenure"] = 0
        print("Loan cleared!")
    elif amt < loan["balance"] and amt % loan["emi"] == 0:
        months_reduced = amt // loan["emi"]
        pay_date = safe_date_input("enter payment date(dd-mm-yyyy):")
        loan["history"].append({"date": pay_date, "amount": amt})

        loan["balance"] -= amt
        loan['tenure'] -= months_reduced

        print(f"partial clearence done.paid{amt}")
        print(f"remaining balance:{loan["balance"]},New tenure:{loan["tenure"]}months.")

    else:
        print("Invalid amount.must match balance (full) or be multiple of emi(partial)\n")
        return
    save_data(data) 

def view_history(data):
    try:
        loan_id = int(input("Enter your loan id:"))
    except ValueError:
        print("Invalid id")
        return

    loan = find_loan(data,loan_id)

    if not loan:
        print("loan not found.\n")
        return
    print(f"\npayment history for loanid: {loan["loan_id"]} - {loan["name"]}")
    for p in loan["history"]:
        print(f"Date:{p['date']} - amount: {p['amount']}")
    print(f"\nBalance Remaining:{loan['balance']} ")
    print(f"status : {loan["status"]}")

    if loan['status'] == 'ongoing':
        print(f"Next emi due: {loan['next_due']}\n Remaininig Tenure:{loan['tenure']}months")

def main():

    data = load_data()
    
    while True:
        print(".....Bank Loan System....")
        print("1. Apply for Loan")
        print("2. Pay EMI")
        print("3. Clear Loan")
        print("4. View Payment History")
        print("5. Exit")

        choice = input("Enter your choice:")

        if choice == "1":
            apply_loan(data)
        elif choice == "2":
            pay_emi(data)
        elif choice == "3":
            clear_loan(data)
        elif choice == "4":
            view_history(data)
        elif choice == "5":
            print("Bye, Thank you.")
            break
        else:
            print("Invalid choice.")

main()




