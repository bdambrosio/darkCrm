import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from contact_manager import ContactManager
from datetime import datetime
import tkinter.font as tkfont

class ContactManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.cm = ContactManager()
        
        # Setup dark theme
        self.setup_dark_theme()
        
        # Create main container
        self.main_container = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Contact list
        self.left_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.left_frame)
        
        # Search frame
        search_frame = ttk.Frame(self.left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style='Dark.TEntry')
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Contact list
        self.contact_tree = ttk.Treeview(self.left_frame, columns=('ID', 'Name', 'Company', 'Relevance'),
                                       show='headings')
        self.contact_tree.heading('ID', text='ID')
        self.contact_tree.heading('Name', text='Name')
        self.contact_tree.heading('Company', text='Company')
        self.contact_tree.heading('Relevance', text='Relevance')
        self.contact_tree.column('ID', width=50)
        self.contact_tree.column('Relevance', width=70)
        self.contact_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        self.contact_tree.bind('<<TreeviewSelect>>', self.on_select_contact)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=10)
        ttk.Button(btn_frame, text="New Contact", 
                  command=self.new_contact,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete",
                  command=self.delete_contact,
                  style='Warning.TButton').pack(side=tk.LEFT, padx=2)
        
        # Right panel - Contact details
        self.right_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.right_frame)
        
        # Contact details form
        self.setup_contact_form()
        
        self.refresh_contacts()

    def setup_dark_theme(self):
        """Configure dark theme colors and styles"""
        self.root.configure(bg='#2b2b2b')
        
        style = ttk.Style()
        
        # Configure colors
        self.colors = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'input_bg': '#3b3b3b',
            'input_fg': '#ffffff',
            'accent': '#4a90e2',
            'warning': '#e25555'
        }
        
        # Configure general styles
        style.configure('.',
            background=self.colors['bg'],
            foreground=self.colors['fg'],
            fieldbackground=self.colors['input_bg'],
            troughcolor=self.colors['bg'],
            selectbackground=self.colors['accent'],
            selectforeground=self.colors['fg']
        )
        
        # Configure specific widget styles
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabelframe', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TLabelframe.Label', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TButton',
            background=self.colors['accent'],
            foreground=self.colors['fg'],
            padding=5
        )
        
        # Configure Treeview colors
        style.configure('Treeview',
            background=self.colors['input_bg'],
            foreground=self.colors['fg'],
            fieldbackground=self.colors['input_bg'],
            rowheight=30
        )
        style.configure('Treeview.Heading',
            background=self.colors['bg'],
            foreground=self.colors['fg']
        )
        
        # Map dynamic states
        style.map('Treeview',
            background=[('selected', self.colors['accent'])],
            foreground=[('selected', self.colors['fg'])]
        )
        style.map('TButton',
            background=[('active', self.colors['accent'])],
            foreground=[('active', self.colors['fg'])]
        )
        
        # Add custom button styles
        style.configure('Accent.TButton',
            background=self.colors['accent'],
            foreground=self.colors['fg']
        )
        style.configure('Warning.TButton',
            background=self.colors['warning'],
            foreground=self.colors['fg']
        )
        
        # Map button states
        style.map('Accent.TButton',
            background=[('active', self.colors['accent'])],
            foreground=[('active', self.colors['fg'])]
        )
        style.map('Warning.TButton',
            background=[('active', self.colors['warning'])],
            foreground=[('active', self.colors['fg'])]
        )
        
        # Add this after the other style configurations:
        style.configure('Dark.TEntry',
            fieldbackground=self.colors['input_bg'],
            foreground=self.colors['fg'],
            insertcolor=self.colors['fg']
        )
        
        # And add this to the style.map section:
        style.map('Dark.TEntry',
            fieldbackground=[('readonly', self.colors['input_bg'])],
            foreground=[('readonly', self.colors['fg'])]
        )

    def setup_contact_form(self):
        form_frame = ttk.LabelFrame(self.right_frame, text="Contact Details")
        form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create form fields
        self.fields = {}
        field_names = ['name', 'company', 'role', 'email', 'linkedin_url', 'relevance_score', 'notes']
        field_labels = ['Name:', 'Company:', 'Role:', 'Email:', 'LinkedIn:', 'Relevance (1-10):', 'Notes:']
        
        for i, (name, label) in enumerate(zip(field_names, field_labels)):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
            if name == 'notes':
                self.fields[name] = scrolledtext.ScrolledText(form_frame, height=3)
            else:
                self.fields[name] = ttk.Entry(form_frame, style='Dark.TEntry')
            self.fields[name].grid(row=i, column=1, padx=5, pady=2, sticky=tk.EW)
        
        ttk.Button(form_frame, text="Save Changes", command=self.save_contact).grid(row=len(field_names), 
                                                                                  column=0, 
                                                                                  columnspan=2, 
                                                                                  pady=10)
        form_frame.columnconfigure(1, weight=1)
        
        # Modify the fields to use dark theme
        for name in self.fields:
            if isinstance(self.fields[name], scrolledtext.ScrolledText):
                self.fields[name].configure(
                    bg=self.colors['input_bg'],
                    fg=self.colors['fg'],
                    insertbackground=self.colors['fg'],  # Cursor color
                    selectbackground=self.colors['accent']
                )
            else:
                self.fields[name].configure(
                    style='Dark.TEntry'
                )

        # Create and configure history section
        ttk.Label(self.right_frame, text="Contact History:").pack(fill=tk.X, padx=5, pady=(10,0))
        self.history_text = scrolledtext.ScrolledText(self.right_frame, height=10)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure the history text widget
        self.history_text.configure(
            bg=self.colors['input_bg'],
            fg=self.colors['fg'],
            insertbackground=self.colors['fg'],
            selectbackground=self.colors['accent']
        )

    def refresh_contacts(self):
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)
        
        contacts = self.cm.get_all_contacts()
        for contact in contacts:
            self.contact_tree.insert('', 'end', values=(contact[0], contact[1], contact[2], contact[6]))

    def on_search(self, *args):
        search_term = self.search_var.get()
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)
        
        if search_term:
            contacts = self.cm.search_contacts(search_term)
        else:
            contacts = self.cm.get_all_contacts()
            
        for contact in contacts:
            self.contact_tree.insert('', 'end', values=(contact[0], contact[1], contact[2], contact[6]))

    def on_select_contact(self, event):
        selection = self.contact_tree.selection()
        if not selection:
            return
        
        contact_id = self.contact_tree.item(selection[0])['values'][0]
        contacts = self.cm.get_all_contacts()
        contact = next((c for c in contacts if c[0] == contact_id), None)
        
        if contact:
            self.fields['name'].delete(0, tk.END)
            self.fields['name'].insert(0, contact[1])
            self.fields['company'].delete(0, tk.END)
            self.fields['company'].insert(0, contact[2] or '')
            self.fields['role'].delete(0, tk.END)
            self.fields['role'].insert(0, contact[3] or '')
            self.fields['email'].delete(0, tk.END)
            self.fields['email'].insert(0, contact[4] or '')
            self.fields['linkedin_url'].delete(0, tk.END)
            self.fields['linkedin_url'].insert(0, contact[5] or '')
            self.fields['relevance_score'].delete(0, tk.END)
            self.fields['relevance_score'].insert(0, str(contact[6]))
            self.fields['notes'].delete('1.0', tk.END)
            self.fields['notes'].insert('1.0', contact[7] or '')
            
            # Update history
            self.history_text.delete('1.0', tk.END)
            history = self.cm.get_contact_history(contact_id)
            for action in history:
                self.history_text.insert(tk.END, 
                                       f"{action[1]} - {action[0]}\n{action[2]}\n{'='*40}\n")

    def new_contact(self):
        # Clear all fields
        for field in self.fields.values():
            if isinstance(field, scrolledtext.ScrolledText):
                field.delete('1.0', tk.END)
            else:
                field.delete(0, tk.END)
        self.history_text.delete('1.0', tk.END)

    def save_contact(self):
        try:
            selection = self.contact_tree.selection()
            data = {
                'name': self.fields['name'].get(),
                'company': self.fields['company'].get(),
                'role': self.fields['role'].get(),
                'email': self.fields['email'].get(),
                'linkedin_url': self.fields['linkedin_url'].get(),
                'relevance_score': int(self.fields['relevance_score'].get()),
                'notes': self.fields['notes'].get('1.0', tk.END).strip()
            }
            
            if selection:  # Update existing contact
                contact_id = self.contact_tree.item(selection[0])['values'][0]
                self.cm.update_contact(contact_id, **data)
            else:  # New contact
                self.cm.add_contact(**data)
            
            self.refresh_contacts()
            messagebox.showinfo("Success", "Contact saved successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", "Please ensure all fields are filled correctly.")

    def delete_contact(self):
        selection = self.contact_tree.selection()
        if not selection:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?"):
            contact_id = self.contact_tree.item(selection[0])['values'][0]
            self.cm.delete_contact(contact_id)
            self.refresh_contacts()
            self.new_contact()  # Clear the form

    def create_custom_entry_style(self):
        """Create custom style for Entry widgets"""
        style = ttk.Style()
        
        # Configure dark entry style
        style.configure('Dark.TEntry',
            fieldbackground=self.colors['input_bg'],
            foreground=self.colors['fg'],
            insertcolor=self.colors['fg']
        )
        
        # Map states
        style.map('Dark.TEntry',
            fieldbackground=[('readonly', self.colors['input_bg'])],
            foreground=[('readonly', self.colors['fg'])]
        )

def main():
    root = tk.Tk()
    root.geometry("1000x600")
    
    # Set window background
    root.configure(bg='#2b2b2b')
    
    app = ContactManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 