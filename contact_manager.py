import sqlite3
from datetime import datetime
import os

class ContactManager:
    def __init__(self, db_path="contacts.db"):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Create the database and contacts table if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company TEXT,
                role TEXT,
                email TEXT,
                linkedin_url TEXT,
                relevance_score INTEGER CHECK (relevance_score BETWEEN 1 AND 10),
                notes TEXT,
                last_contact_date TEXT,
                follow_up_date TEXT,
                status TEXT DEFAULT 'New',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                action_type TEXT,
                action_date TEXT DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (contact_id) REFERENCES contacts (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def add_contact(self, name, company, role, email="", linkedin_url="", 
                   relevance_score=1, notes="", status="New"):
        """Add a new contact to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contacts (name, company, role, email, linkedin_url, 
                                relevance_score, notes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, company, role, email, linkedin_url, relevance_score, 
              notes, status))
        
        contact_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        self.log_history(contact_id, "Created", "Initial contact created")
        return contact_id

    def update_contact(self, contact_id, **kwargs):
        """Update an existing contact's information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        update_fields = []
        values = []
        for key, value in kwargs.items():
            update_fields.append(f"{key} = ?")
            values.append(value)
        
        values.append(contact_id)
        query = f"UPDATE contacts SET {', '.join(update_fields)} WHERE id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        self.log_history(contact_id, "Updated", f"Updated fields: {', '.join(kwargs.keys())}")

    def get_all_contacts(self):
        """Retrieve all contacts from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM contacts ORDER BY relevance_score DESC")
        contacts = cursor.fetchall()
        
        conn.close()
        return contacts

    def search_contacts(self, search_term):
        """Search contacts by name, company, or notes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM contacts 
            WHERE name LIKE ? OR company LIKE ? OR notes LIKE ?
            ORDER BY relevance_score DESC
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        contacts = cursor.fetchall()
        conn.close()
        return contacts

    def delete_contact(self, contact_id):
        """Delete a contact from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        
        conn.commit()
        conn.close()
        
        self.log_history(contact_id, "Deleted", "Contact deleted")

    def log_history(self, contact_id, action_type, notes=""):
        """Log an action in the contact history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contact_history (contact_id, action_type, notes)
            VALUES (?, ?, ?)
        ''', (contact_id, action_type, notes))
        
        conn.commit()
        conn.close()

    def get_contact_history(self, contact_id):
        """Get history for a specific contact"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT action_type, action_date, notes 
            FROM contact_history 
            WHERE contact_id = ?
            ORDER BY action_date DESC
        ''', (contact_id,))
        
        history = cursor.fetchall()
        conn.close()
        return history 