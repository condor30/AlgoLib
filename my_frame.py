import os
import json
import customtkinter as ctk

class MyFrame(ctk.CTkScrollableFrame):
    """Classe représentant le cadre contenant les algorithmes."""

    def __init__(self, master, textbox, **kwargs):
        """Constructeur de la classe MyFrame."""
        super().__init__(master, **kwargs)
        self.textbox = textbox 
        
        # Get the directory of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the full path to 'algorithms.json'
        algorithms_file_path = os.path.join(current_directory, "algorithms.json")

        # Ajouter des widgets dans le cadre...
        with open(algorithms_file_path, "r") as file:
            self.all_algorithms = json.load(file).get("algorithms", [])
        
        self.filtered_algorithms = self.all_algorithms  # Initialisez avec tous les algorithmes

        self.create_buttons()

        self.grid_columnconfigure(0, weight=1)

    def create_buttons(self):
        """Crée les boutons en fonction des algorithmes filtrés."""
        for row, algorithm in enumerate(self.filtered_algorithms, start=1):
            algorithm_name = algorithm.get("name", "")
            algorithm_button = ctk.CTkButton(self, text=algorithm_name)
            algorithm_button.grid(row=row, column=0, pady=5, sticky="ew")

            algorithm_button.configure(command=lambda algo=algorithm: self.show_algorithm(algo))

    def update_filtered_algorithms(self, search_text):
        """Met à jour la liste des algorithmes filtrés en fonction de la chaîne de recherche."""
        if search_text:
            self.filtered_algorithms = [algo for algo in self.all_algorithms if search_text.lower() in algo.get("name", "").lower()]
        else:
            self.filtered_algorithms = self.all_algorithms

        # Supprimez tous les boutons actuels
        for widget in self.winfo_children():
            widget.destroy()

        # Recréez les boutons avec les algorithmes filtrés
        self.create_buttons()

    def show_algorithm(self, algorithm):
        """Mettez à jour le CTkTextbox avec le contenu de l'algorithme sélectionné."""
        algorithm_content = algorithm.get("content", "")
        self.textbox.configure(state="normal")  # Activez le mode lecture/écriture
        self.textbox.delete("1.0", "end")  # Effacer le contenu existant
        self.textbox.insert("1.0", algorithm_content)
        self.textbox.configure(state="disabled")  # Désactivez le mode écriture après l'affichage
