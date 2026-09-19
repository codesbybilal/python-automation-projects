print(" -------------------------------------")
print("|         Contact Book CLI            |")
print(" -------------------------------------")
#Operations on Contact Book 
print("Contact Book Contents:")
print("1. Show all contacts")
print("2. Add a contact")
print("3. Delete a contact")
print("4. Search by name")
option = int(input("Enter an option (1, 2, 3 or 4): "))


def showContacts():
    with open("contact.txt", "r") as f:
        data = f.read()
    print(data)

def addContact():
    name = input("Enter the name of the contact: ")
    number = input("Enter the number of the contact: ")
    newContact = f"\n{name} | {number}" 
    with open("contact.txt", "a") as f:
        f.write(newContact)
def deleteContact():
    delContactName = input("Enter the name of the contact you want to be deleted: ")
    with open("contact.txt", "r+") as f:
        allContacts = f.read()
    if delContactName in allContacts:
        allContacts.replace(delContactName, "Deleted Contact")
    else:
        print(f"{delContactName} does not exist in the contact list.")

def searchContact():
    searchContact = input("Enter the contact name to search: ")

    with open("contact.txt", "r") as f:
        for line in f:
            name, number = line.strip().split(" | ")

            if searchContact == name:
                print(f"Name: {name}\nContact: {number}")
                return

    print("Contact not found.")
match option:
    case 1:
        showContacts()
    case 2:
        addContact()
    case 3:
        deleteContact()
    case 4:
        searchContact()
    case _:
        print("Invalid option entered. Enter either 1, 2, 3 or 4.")


