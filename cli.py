from contact_manager import ContactManager
import sys

def print_menu():
    print("\nContact Manager Menu:")
    print("1. Add new contact")
    print("2. List all contacts")
    print("3. Search contacts")
    print("4. Update contact")
    print("5. Delete contact")
    print("6. Exit")

def get_contact_info():
    name = input("Name: ")
    company = input("Company/Organization: ")
    role = input("Role/Title: ")
    email = input("Email (optional): ")
    linkedin = input("LinkedIn profile URL (optional): ")
    
    while True:
        try:
            relevance = int(input("Relevance score (1-10): "))
            if 1 <= relevance <= 10:
                break
            print("Please enter a number between 1 and 10")
        except ValueError:
            print("Please enter a valid number")
    
    notes = input("Notes: ")
    return name, company, role, email, linkedin, relevance, notes

def main():
    cm = ContactManager()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            # Add new contact
            contact_info = get_contact_info()
            cm.add_contact(*contact_info)
            print("Contact added successfully!")

        elif choice == "2":
            # List all contacts
            contacts = cm.get_all_contacts()
            if not contacts:
                print("No contacts found.")
                continue
                
            print("\nAll Contacts:")
            for contact in contacts:
                print(f"\nID: {contact[0]}")
                print(f"Name: {contact[1]}")
                print(f"Company: {contact[2]}")
                print(f"Role: {contact[3]}")
                print(f"Email: {contact[4]}")
                print(f"LinkedIn: {contact[5]}")
                print(f"Relevance: {contact[6]}")
                print(f"Notes: {contact[7]}")
                print("-" * 40)

        elif choice == "3":
            # Search contacts
            search_term = input("Enter search term: ")
            contacts = cm.search_contacts(search_term)
            
            if not contacts:
                print("No matching contacts found.")
                continue
                
            print("\nMatching Contacts:")
            for contact in contacts:
                print(f"\nID: {contact[0]}")
                print(f"Name: {contact[1]}")
                print(f"Company: {contact[2]}")
                print(f"Relevance: {contact[6]}")
                print("-" * 40)

        elif choice == "4":
            # Update contact
            contact_id = input("Enter contact ID to update: ")
            print("Enter new values (or press Enter to skip):")
            
            updates = {}
            name = input("Name: ")
            if name: updates['name'] = name
            
            company = input("Company: ")
            if company: updates['company'] = company
            
            role = input("Role: ")
            if role: updates['role'] = role
            
            email = input("Email: ")
            if email: updates['email'] = email
            
            linkedin = input("LinkedIn URL: ")
            if linkedin: updates['linkedin_url'] = linkedin
            
            relevance = input("Relevance score (1-10): ")
            if relevance: updates['relevance_score'] = int(relevance)
            
            notes = input("Notes: ")
            if notes: updates['notes'] = notes
            
            if updates:
                cm.update_contact(contact_id, **updates)
                print("Contact updated successfully!")

        elif choice == "5":
            # Delete contact
            contact_id = input("Enter contact ID to delete: ")
            cm.delete_contact(contact_id)
            print("Contact deleted successfully!")

        elif choice == "6":
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 