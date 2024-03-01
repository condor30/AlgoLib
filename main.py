import json
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from app import App
#default password is "1234"
# Run app
if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
