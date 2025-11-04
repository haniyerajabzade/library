from datetime import datetime, timedelta, date
import random
import json
import os

def check_json(file):
    filename= file + '.json'
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f, indent=4)
    else:
        with open(filename) as ff:
            db = ff.read()
        if db.strip() == '':
            with open(filename, 'w') as fff:
                json.dump([], fff, indent=4)

def load_json(file):
    check_json(file)
    with open(f'{file}.json','r')as f:
        db=json.load(f)
    return db

def write_2_json(file,data):
    db=load_json(file)
    db.append(data)
    with open(f'{file}.json','w')as f:
        json.dump(db,f,indent=4)

def edit_json(file,data):
    with open(f'{file}.json','w')as f:
        json.dump(data,f,indent=4)

def check_username(file,input_username):
    db=load_json(file)
    i=0
    while i<len(db):
        if input_username.strip()=='':
            return None
        if db[i]['username']==input_username:
            return False
        i+=1
    return True

def check_user(file, username):
    db = load_json(file)
    for user in db:
        if username.strip() == '':
            return None
        if user['username'] == username:
            return True
    return False

def check_password(input_password):
    errors=[]
    up=False
    lo=False
    di=False
    for i in input_password:
        if i.isupper():
            up=True
        if i.islower():
            lo=True
        if i.isdigit():
            di=True
    if not up:
        errors.append('PASSWORD MUST BE HAVE A_Z')
    if not lo:
        errors.append('PASSWORD MUST HAVE a-z')
    if not di:
        errors.append('PASSWORD MUST HAVE BE 0_9')
    if len(input_password)<8:
        errors.append('PASSWORD MUST BE BIGGER THAN 8')
    if len(errors)==0:
        return True,input_password
    else:
        return False,errors

def check_email(input_email):
    email_address = input_email.strip().lower()
    if email_address.endswith('@gmail.com') or email_address.endswith('@yahoo.com'):
        if len(email_address) > 10:
            return True
        else:
            print("Email is incorrect. Please try again.")
            return False
    else:
        print("Email must end with @gmail.com or @yahoo.com. Please try again.")
        return False

def check_security_answer(file, answer):
    db = load_json(file)
    i = 0
    while i < len(db):
        if answer.strip() == '':
            return None
        if db[i]["answer"] ==answer:
            return True
        i += 1
    return False

#
def check_book_id(file, input_book_id):
    db = load_json(file)
    i = 0
    while i < len(db):
        if input_book_id.strip() == "":
            return None
        if db[i]["book's ID"] == input_book_id:
            return False
        i += 1
    return True

def add_new_book(file):
    book_name = input("Enter book's name: ").strip()
    while book_name == "":
        print("Please complete this field.")
        book_name = input("Enter book's name: ").strip()

    book_author = input("Enter author's name: ").strip()
    while book_author == "":
        print("Please complete this field.")
        book_author = input("Enter author's name: ").strip()

    while True:
        publication_year = input("Enter book's publication year: ").replace(" ", "")
        if publication_year.strip() == "":
            print("Please complete this field.")
            continue
        if not publication_year.isdigit() :
            print("Please enter a valid number.")
            continue
        break


    while True:
        book_id = str(random.randint(100000, 999999))
        result = check_book_id(file, book_id)
        if result:
            break
        elif result == False:
            continue
    books_info = {"name": book_name,
                    "author": book_author,
                    "publication year": int(publication_year),
                    "book's ID": int(book_id),
                    "borrowers": []
                    }
    write_2_json(file, books_info)
    print("Book added successfully.")

# --------------------------------------------------

def check_book(file, input_book):
    db = load_json(file)
    i = 0
    while i < len(db):
        if db[i]["book's ID"] == int(input_book):
            return True
        i += 1
    return False

def delete_book(file):
    db = load_json(file)
    while True:
        book_id = input("Enter book's ID: ").replace(" ", "")
        if book_id == "":
            print("Please complete this field.")
            continue
        if not book_id.isdigit():
            print("Please enter a valid book ID.")
            continue
        break
    i = 0
    while i < 3:
        if check_book(file, book_id):
            for book in db:
                if book["book's ID"] == int(book_id):
                    db.remove(book)
                    edit_json(file, db)
                    print("Book deleted successfully.")
                    return
        else:
            print("Book's ID not found. Please try again.")
            book_id = input("Enter book's ID: ").replace(" ", "")
            i += 1

    print("Failed to delete book after 3 attempts.")

#

def search_book(file):
    title_input=input('Enter the name of the book: (optional)').strip()
    if title_input=='':
        title_input=None

    author_input=input('Enter the authors name: (optional)').strip()
    if author_input=='':
        author_input=None

    year_input = input('Enter the year of publication: (optional)').strip()
    if year_input=='':
        year_input=None
    else:
        while True:
            if year_input.isdigit():
                break
            else:
                print("Please enter a valid number.")
                year_input = input('Enter the year of publication: (optional)').strip()

    db=load_json(file)
    results = []
    for book in db:
        if title_input is not None and title_input.lower()  not in book["name"].lower():
            continue
        if author_input is not None and author_input.lower() not in book["author"].lower():
            continue
        if year_input is not None and year_input != book["publication year"]:
            continue
        results.append(book)
    if title_input is None and author_input is None and year_input is None:
        results=db[:]

    if results:
        print(f"{len(results)} book's found:")
        for book in results:
            print(f'''{book["name"]} | {book["author"]} | {book["publication year"]}''')
    else:
        print("No books were found with the entered specifications.")

#
def show_all_books(file):
    db=load_json(file)
    for book in db:
        print(f'''{book["name"]} | {book["author"]} | {book["publication year"]}''')

#
def check_user_has_book(book, username):
    for borrower in book["borrowers"]:
        if borrower["username"] == username:
            return True
    return False
#

def checkout_book(file, username):
    db = load_json(file)
    while True:
        book_id = input("Enter book's ID: ").replace(" ", "")
        if book_id == "":
            print("Please complete this field.")
            continue
        if not book_id.isdigit():
            print("Please enter a valid book ID.")
            continue
        break

    i = 0
    while i < 3:
        for book in db:
            if book["book's ID"] == int(book_id):
                if check_user_has_book(book, username):
                    print("You have this book checked out.")
                    return

                checkout_time = date.today()
                return_time = checkout_time + timedelta(days=14)
                borrowers_info = {
                    "username": username,
                    "checkout time": checkout_time.strftime("%Y-%m-%d"),
                    "return time": return_time.strftime("%Y-%m-%d")
                }
                book["borrowers"].append(borrowers_info)
                edit_json(file, db)
                print("Checkout successful.")
                return

        print("Book's ID not found. Please try again.")
        book_id = input("Enter book's ID: ").replace(" ", "")
        i += 1

    print("Failed to checkout book after 3 attempts.")
# --------------------------------------------------

def return_book(file, username):
    db = load_json(file)
    while True:
        book_id = input("Enter book's ID: ").replace(" ", "")
        if book_id == "":
            print("Please complete this field.")
            continue
        if not book_id.isdigit():
            print("Please enter a valid book ID.")
            continue
        break
    i = 0
    while i < 3:
        if check_book(file, book_id):
            for book in db:
                if book["book's ID"] == int(book_id):
                    if not check_user_has_book(book, username):
                        print("You hadn't checked out this book.")
                        return
                    new_borrowers = []
                    for k in book["borrowers"]:
                        if k["username"] != username:
                            new_borrowers.append(k)
                    book["borrowers"] = new_borrowers
                    edit_json(file, db)
                    print("Return successful.")
                    return
        else:
            print("Book's ID not found. Please try again.")
            book_id = input("Enter book's ID: ").replace(" ", "")
            i += 1

    print("Failed to return book after 3 attempts.")

#

def extend_deposit(file, username):
    today = datetime.today()
    db = load_json(file)
    updated = False
    has_deposit = False

    for book in db:
        if check_user_has_book(book, username):
            has_deposit = True
            for borrower in book["borrowers"]:
                if borrower["username"] == username:
                    return_time = datetime.strptime(borrower["return time"], '%Y-%m-%d')
                    remaining_days = (return_time - today).days

                    if remaining_days < 3:
                        new_deadline = return_time + timedelta(days=7)
                        borrower["return time"] = new_deadline.strftime('%Y-%m-%d')
                        print(f"{book['name']} extended until: {new_deadline.strftime('%Y-%m-%d')}")
                        updated = True
                    else:
                        print(f"{book['name']} still has {remaining_days} days left.")

    if not has_deposit:
        print("You have no active book deposits.")
    if updated:
        edit_json(file, db)

#
def suggest_random_book(file):
    db=load_json(file)
    if not db:
        print("The book list is empty!")
        return
    selected_book= random.choice(db)
    print(f'Suggestion: «{selected_book["name"]}» written by {selected_book["author"]}')
    return

#
def show_user_list(file):
    db=load_json(file)
    if not db:
        print("No users have registered.")
        return
    print("List of registered users:")
    for u in db:
        print(f"name:{u['username']} | email address:{u['email address']} | role:{u['role']}")

#

def admin_menu():
    return('\nWhat do you want to do?\n'
            '1.Add new book\n'+
            '2.Delete book\n'+
            '3.Search book\n'+
            '4.Show all books\n'+
            '5.Check out book\n'+
            '6.Return book\n'+
            '7.Extend deposit\n'+
            '8.Random book suggestion\n'+
            '9.Show user list\n'+
            '10.Logout')
def user_menu():
    return('\nWhat do you want to do?\n'+'1.Search book\n' +
           '2.Show all books\n' +
           '3.Check out book\n' +
           '4.Return book\n' +
           '5.Extend deposit\n' +
           '6.Random book suggestion\n'+
           '7.Logout')
def admin_panel(username):
    print(f"Welcome {username}!")
    print("You have admin access.")
    while True:
        print(admin_menu())
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            add_new_book("books_info")
        elif choice == '2':
            delete_book("books_info")
        elif choice == '3':
            search_book("books_info")
        elif choice == '4':
            show_all_books("books_info")
        elif choice == '5':
            checkout_book("books_info", username)
        elif choice == '6':
            return_book("books_info", username)
        elif choice== '7':
            extend_deposit("books_info",username)
        elif choice== '8':
            suggest_random_book("books_info")
        elif choice== '9':
            show_user_list('users')
        elif choice == '10':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 10.")
def user_panel(username):
    print(f"Welcome {username}!")
    print("You have user access.")
    while True:
        print(user_menu())
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            search_book("books_info")
        elif choice == '2':
            show_all_books("books_info")
        elif choice == '3':
            checkout_book("books_info", username)
        elif choice == '4':
            return_book("books_info", username)
        elif choice == '5':
            extend_deposit("books_info",username)
        elif choice == '6':
            suggest_random_book("books_info")
        elif choice == '7':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
#

def register(file):
    while True:
        username = input("Enter your username: ").replace(" ", "").lower()
        result = check_username(file, username)
        if result:
            if username == "amir" or username == "haniye":
                print("Username is invalid. Please try again.")
            else:
                break
        elif result == False:
            if username == "amir" or username == "haniye":
                print("Username is invalid. Please try again.")
                continue
            else:
                print("Username must be unique. Please try again.")
                continue
        elif result is None:
            print("Please complete this field.")
            continue

    while True:
        password = input("Enter your password: ")
        while password.strip() == "":
            print("Please complete this field.")
            password = input("Enter your password: ").replace(" ", "")
        valid, messages = check_password(password)
        if valid:
            break
        else:
            for i in messages:
                print(i)
    while True:
        confirm= input("Enter your password again: ")
        while password.strip() == "":
            print("Please complete this field.")
            password = input("Enter your password: ").replace(" ", "")
        if confirm == password:
            break
        else:
            print("Password confirmation must match the password.")
    while True:
        email = input("Enter your email: ").replace(" ", "")
        while email.strip() == "":
            print("Please complete this field.")
            email = input("Enter your email: ").replace(" ", "")
        if not check_email(email):
            print("The email must end with @gmail.com or @yahoo.com.")
            continue
        break
    while True:
        security_question= input('Enter your Security question: ')
        while security_question.strip() == "":
            print("Please complete this field.")
            security_question= input('Enter your Security question: ')
        answer=input(f'Enter the answer of {security_question}? ').replace(" ", "")
        while answer.strip() == "":
            print("Please complete this field.")
            answer=input(f'Enter the answer of {security_question}? ').replace(" ", "")
        break
    users_info= {"username": username,
        "password": password,
        "email address": email,
        'security_question':security_question,
        "answer":answer,
        "role":'user'
    }
    write_2_json(file,users_info)
    print("Register succesfully.")
#
def login(file):
    while True:
        username = input("Enter username: ").strip()
        db = load_json(file)
        result=check_user(file,username)
        if result == False:
            print("Username not found. Please try again.")
        if result:
            i = 0
            valid=False
            while i < 3:
                password = input("Enter Password: ")
                for j in db:
                    if j['username'] == username and j['password'] == password:
                        if j['role'] == 'admin':
                            admin_panel(username)
                        else:
                            user_panel(username)
                        valid=True
                        break
                if valid:
                    break
                elif password.strip() == "":
                    print("Please complete this field.")
                else:
                    print("Password is incorrect. Please try again.")
                i += 1
            if valid:
                break
            else:
                print(f'Too many incorrect attempts. login {username} failed.')
        elif result is None:
            print("Please complete this field.")


#
def edit_password(file, username):
    db = load_json(file)
    while True:
        new_password = input("Enter new password: ").replace(" ", "")
        while new_password.strip() == "":
            print("Please complete this field.")
            new_password = input("Enter your new password: ").replace(" ", "")
        res, error = check_password(new_password)
        if res:
            for j in db:
                if j["username"] == username:
                    j["password"] = new_password
                    edit_json(file, db)
            break
        else:
            for i in error:
                print(i)
def forgot_password(file):
    while True:
        username = input("Enter your username: ").strip().replace(" ", "")
        result=check_user(file,username)
        if result is None :
            print("Please complete this field.")
            continue
        if not result:
            print("Username not found. Please try again.")
            continue
        db = load_json(file)
        user = next((j for j in db if j["username"] == username), None)
        if not user:
            print("User data not found.")
            return

        i = 0
        while i < 3:
            answer = input(f"{user['security_question']}? ").strip().lower().replace(" ", "")
            if not answer:
                print("Please complete this field.")
                i += 1
                continue
            if answer == user["answer"].lower():
                edit_password(file, username)
                print("Password changed successfully.")
                return
            else:
                print("Answer is incorrect. Please try again.")
                i += 1

        print("Too many incorrect attempts. Password recovery failed.")
        return

def main(file):
    while True:
        op = input("1-Register\n2-Login\n3-forgot_password\n4-exit : ")
        if op == '1':
            register(file)
        elif op == '2':
            login(file)
        elif op== "3":
            forgot_password(file)
        elif op == '4':
            print("Have a Good Moment :)")
            break
        else:
            print("INVALID ANSWER, PLEASE TRY AGAIN.")

main('users')