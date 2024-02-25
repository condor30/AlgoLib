# app.py
import json
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from my_frame import MyFrame

class App(ctk.CTk):
    """Classe principale représentant l'application ALGOLIB."""

    def __init__(self, root):
        """Constructeur de la classe App."""
        self.root = root
        self.root.title("")
        self.root.geometry("350x150")

        # Set window properties
        self.root.title("ALGOLIB")

        # Set appearance mode to "dark"
        ctk.set_appearance_mode("dark")

        self.root.grid_columnconfigure((0, 1), weight=1)

        # Label for mode selection
        self.label = ctk.CTkLabel(self.root, text="Which Mode?")
        self.label.grid(row=0, column=0, columnspan=2, pady=(20, 1), sticky="n")

        # Button for User mode
        self.button_user = ctk.CTkButton(self.root, text="User", command=self.user_interface)
        self.button_user.grid(row=1, column=0, padx=(0, 0), pady=(0, 0))

        # Button for Admin mode
        self.button_admin = ctk.CTkButton(self.root, text="Admin", command=self.open_admin)
        self.button_admin.grid(row=1, column=1, padx=(0, 0), pady=(0, 0))

        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def open_admin(self):
        """Ouvre l'interface administrateur."""
        password = self.ask_pass()
        if self.check_pass(password):
            self.admin_interface()
        else:
            CTkMessagebox(title="Information", message="Invalid Password")

    def ask_pass(self):
        """Demande le mot de passe à l'utilisateur."""
        password_window = ctk.CTkToplevel(self.root)
        password_window.title("Enter Password")
        password_window.geometry("300x200")

        label = ctk.CTkLabel(password_window, text="Enter Password:")
        label.pack(pady=10)

        entry = ctk.CTkEntry(password_window, show="*")
        entry.pack(pady=10)

        entered_password = ctk.StringVar()

        def submit_password():
            entered_password.set(entry.get())
            password_window.destroy()

        button = ctk.CTkButton(password_window, text="Submit", command=submit_password)
        button.pack()

        password_window.wait_window()
        return entered_password.get()

    def check_pass(self, entered_password):
        """Vérifie si le mot de passe est valide."""
        try:
            with open("passwords.json", "r") as file:
                passwords = json.load(file)
        except FileNotFoundError:
            passwords = {}

        return passwords.get("admin_password") == entered_password

    def user_interface(self):
        """Interface utilisateur."""
        self.root.withdraw()
        user_interface = ctk.CTkToplevel(self.root)
        user_interface.title("ALGOLIB")
        user_interface.geometry("960x500")

         # Barre de recherche en haut
        search_bar = ctk.CTkEntry(user_interface, placeholder_text="search")
        search_bar.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="we")

        # Bouton à côté de la barre de recherche
        self.mode = ctk.CTkButton(user_interface, text="MODE", width=100, command=self.return_to_main_page)  # Ajustez la valeur de width selon vos besoins
        self.mode.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        # Champ de texte à droite, occupant le reste de la page
        self.textbox = ctk.CTkTextbox(user_interface, corner_radius=15)
        self.textbox.grid(row=1, column=1,columnspan=2, padx=10, pady=10, sticky="nsew")

        # Passer le CTkTextbox à la classe MyFrame
        self.scrollable_frame = MyFrame(master=user_interface, textbox=self.textbox, width=200, height=450)
        self.scrollable_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ns")

        user_interface.grid_rowconfigure(1, weight=1)  # Définir le poids à 1 pour la ligne contenant le champ de texte
        user_interface.grid_columnconfigure(1, weight=1)  # Définir le poids à 1 pour la colonne contenant le champ de texte
        user_interface.grid_columnconfigure(0, weight=0)  # Définir le poids à 0 pour la colonne contenant le cadre déroulant

        ctk.set_appearance_mode("dark")

        # Associez la fonction de mise à jour à l'événement de modification de la barre de recherche
        search_bar.bind("<KeyRelease>", lambda event, s=search_bar: self.update_algorithm_list(s.get(), user_interface))

    def return_to_main_page(self):
        """Retourne à la page principale."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.deiconify()
        new_app = App(self.root)

    def update_algorithm_list(self, search_text, user_interface):
        """Met à jour la liste des algorithmes filtrés dans MyFrame."""
        self.scrollable_frame.update_filtered_algorithms(search_text)

        # Réactivez la mise à jour après un court délai (10 ms)
        user_interface.after(10, lambda: setattr(self.scrollable_frame, 'update_needed', True))

    def admin_interface(self):
        """Interface administrateur."""
        self.root.withdraw()
        admin_interface = ctk.CTkToplevel(self.root)
        admin_interface.title("Admin Mode")
        admin_interface.geometry("960x500")

        # Center the buttons vertically and horizontally
        admin_interface.grid_rowconfigure(1, weight=1)
        admin_interface.grid_columnconfigure(0, weight=2)
        admin_interface.grid_columnconfigure(6, weight=1)

        # Change mode button
        self.mode = ctk.CTkButton(admin_interface, text="MODE", width=100, command=self.return_to_main_page)
        self.mode.grid(row=0, column=6, pady=10, padx=10, sticky="ne")  # Place the button in the top-right corner

        # Change password admin
        self.password_change = ctk.CTkButton(admin_interface, text="Change Password", width=100,command=self.change_password )
        self.password_change.grid(row=1, column=2, pady=10, padx=10)

        # Add an algo
        self.add_algo = ctk.CTkButton(admin_interface, text="Add An Algorithm", width=100, command=self.add_algorithm)
        self.add_algo.grid(row=1, column=3, pady=10, padx=10)

        # Modify an algo
        self.modify_algo = ctk.CTkButton(admin_interface, text="Modify an Algorithm", width=100, command=self.modify_algorithm)
        self.modify_algo.grid(row=1, column=4, pady=10, padx=10)

        # Delete an algo
        self.delete_algo = ctk.CTkButton(admin_interface, text="Delete an Algo", width=100, command=self.delete_algorithm)
        self.delete_algo.grid(row=1, column=5, pady=10, padx=10)
        ctk.set_appearance_mode("system")

    def change_password(self):
        """Change le mot de passe."""
        # Create a Toplevel window for changing password
        password_window = ctk.CTkToplevel(self.root)
        password_window.title("Change Password")
        password_window.geometry("200x200")

        # Label and Entry for new password
        label_password = ctk.CTkLabel(password_window, text="Enter new password:")
        label_password.pack(pady=10)

        new_password_entry = ctk.CTkEntry(password_window, show="*")
        new_password_entry.pack(pady=10)

        # Button to confirm password change
        confirm_button = ctk.CTkButton(password_window, text="Change Password", command=lambda: self.confirm_password_change(password_window, new_password_entry.get()))
        confirm_button.pack(pady=10)
        ctk.set_appearance_mode("dark")

    def confirm_password_change(self, password_window, new_password):
        """Confirme le changement de mot de passe."""
        if new_password:
            # Update the password in the JSON file
            self.update_password(new_password)
            CTkMessagebox(title="Success", message="Password changed successfully!")
            password_window.destroy()
        else:
            CTkMessagebox(title="Warning", message="Please enter a new password.")

    def update_password(self, new_password):
        """Met à jour le mot de passe dans le fichier JSON."""
        # Load the existing JSON data
        with open('passwords.json', 'r') as json_file:
            data = json.load(json_file)

        # Update the password
        data['admin_password'] = new_password

        # Write the updated data back to the JSON file
        with open('passwords.json', 'w') as json_file:
            json.dump(data, json_file)

    def add_algorithm(self):
        """Ajoute un algorithme."""
        # Create a new Toplevel window for adding an algorithm
        add_algo_window = ctk.CTkToplevel(self.root)
        add_algo_window.title("Add Algorithm")
        add_algo_window.geometry("200x400")

        # Entry fields for algorithm name and content
        ctk.CTkLabel(add_algo_window, text="Algorithm Name:").pack(pady=5)

        algo_name_entry = ctk.CTkEntry(add_algo_window)
        algo_name_entry.pack(pady=10)

        ctk.CTkLabel(add_algo_window, text="Algorithm Content:").pack(pady=5, padx=10)
        algo_content_entry = ctk.CTkTextbox(add_algo_window, height=200, width=180, wrap="word")  # Adjusted height
        algo_content_entry.pack(pady=10)

        # Button to confirm the addition
        confirm_button = ctk.CTkButton(add_algo_window, text="Add Algorithm", command=lambda: self.confirm_add_algorithm(add_algo_window, algo_name_entry.get(), algo_content_entry.get("1.0", "end-1c")))
        confirm_button.pack(pady=10)
        ctk.set_appearance_mode("dark")

    def confirm_add_algorithm(self, add_algo_window, name, content):
        """Confirme l'ajout de l'algorithme."""
        if name and content:
            # Load existing JSON data
            with open('algorithms.json', 'r') as json_file:
                data = json.load(json_file)

            # Add the new algorithm
            new_algo = {"name": name, "content": content}
            data["algorithms"].append(new_algo)

            # Write the updated data back to the JSON file
            with open('algorithms.json', 'w') as json_file:
                json.dump(data, json_file)

            CTkMessagebox(title="Success", message="Algorithm added successfully!")
            add_algo_window.destroy()
        else:
            CTkMessagebox.showwarning(title="Warning", message="Please enter both algorithm name and content.")

    def modify_algorithm(self):
        """Modifie un algorithme."""
        # Create a new window for algorithm modification
        modify = ctk.CTkToplevel(self.root)
        modify.title("Modify Algorithm")
        modify.geometry("500x500")

        # Load JSON from a file
        with open('algorithms.json', 'r') as file:
            self.all_algorithms = json.load(file)['algorithms']

        self.label2 = ctk.CTkLabel(modify, text="select your algorithm:", fg_color="transparent")
        self.label2.pack(pady=5)
        # Create a combobox to select the algorithm
        self.selected_algo_var = ctk.StringVar(value="")  # Use a StringVar
        self.selected_algo = ctk.CTkComboBox(modify, values=[algo['name'] for algo in self.all_algorithms], variable=self.selected_algo_var)
        self.selected_algo.pack(pady=10)

        # Modifier le contenu label
        self.label1 = ctk.CTkLabel(modify, text="Change the content of your algorithm:", fg_color="transparent")
        self.label1.pack(pady=5)

        # Create a Textbox to display the content of the selected algorithm
        self.content_textbox = ctk.CTkTextbox(modify, height=300, width=400, wrap="word")
        self.content_textbox.pack(pady=10)

        # Create a Submit button
        self.confirm = ctk.CTkButton(modify, text="Submit", command=self.submit_content)
        self.confirm.pack(pady=10)

        # Link content update to the StringVar
        self.selected_algo_var.trace_add("write", self.update_content)
        self.root.withdraw()

    def update_content(self, *args):
        """Update content based on selected algorithm."""
        selected_algo_name = self.selected_algo_var.get()
        selected_algo_content = next((algo["content"] for algo in self.all_algorithms if algo["name"] == selected_algo_name), "")
        self.content_textbox.configure(state="normal")  # Enable read/write mode
        self.content_textbox.delete("1.0", "end")  # Clear existing content
        self.content_textbox.insert("1.0", selected_algo_content)

    def submit_content(self):
        """Submit modified content."""
        selected_algo_name = self.selected_algo_var.get()
        new_content = self.content_textbox.get("1.0", "end-1c")  # Get content from TextBox

        # Update content of the selected algorithm
        for algo in self.all_algorithms:
            if algo["name"] == selected_algo_name:
                algo["content"] = new_content

        # Save changes to the JSON file
        with open('algorithms.json', 'w') as file:
            json.dump({"algorithms": self.all_algorithms}, file)

        # Display a confirmation message or perform other necessary actions
        print("Modification enregistrée avec succès!")
        CTkMessagebox(title="Success", message="Change saved successfully!")

    def delete_algorithm(self):
        """Delete an algorithm."""
        # Create a new window for algorithm deletion
        delete_window = ctk.CTkToplevel(self.root)
        delete_window.title("Delete Algorithm")
        delete_window.geometry("300x150")

        # Load JSON from a file
        with open('algorithms.json', 'r') as file:
            self.all_algorithms = json.load(file)['algorithms']

        self.label1 = ctk.CTkLabel(delete_window, text="Choose the Algorith to delete:", fg_color="transparent")
        self.label1.pack(pady=5)
        # Create a combobox to select the algorithm to delete
        selected_algo_var = ctk.StringVar(value="")
        delete_algo_combobox = ctk.CTkComboBox(delete_window, values=[algo['name'] for algo in self.all_algorithms], variable=selected_algo_var)
        delete_algo_combobox.pack(pady=10)

        # Create a confirmation button to delete the algorithm
        confirm_delete_button = ctk.CTkButton(delete_window, text="Delete", command=lambda: self.confirm_delete(selected_algo_var.get(), delete_window))
        confirm_delete_button.pack(pady=10)

    def confirm_delete(self, selected_algo_name, delete_window):
        """Confirm deletion of the algorithm."""
        if selected_algo_name:
            # Remove the algorithm from the list
            self.all_algorithms = [algo for algo in self.all_algorithms if algo['name'] != selected_algo_name]

            # Save changes to the JSON file
            with open('algorithms.json', 'w') as file:
                json.dump({"algorithms": self.all_algorithms}, file)

            # Display a confirmation message or perform other necessary actions
            print(f"Algorithm '{selected_algo_name}' supprimé avec succès!")

            CTkMessagebox(title="Success", message="Algorithm deleted with success!")
            delete_window.destroy()
        else:
            CTkMessagebox.showwarning(title="Warning", message="Please select an algorithm to delete.")
