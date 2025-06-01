import customtkinter as ctk
from ui.login import LoginWindow

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")   
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    app.geometry("500x500")
    app.title("Banking App")
    LoginWindow(app)
    app.mainloop()

