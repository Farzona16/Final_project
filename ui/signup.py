import customtkinter as ctk
from models.user import create_user, verify_user
from ui.dashboard import DashboardWindow

class SignUpWindow:
    def __init__(self, root):
        self.root = root
        self.bg_frame = ctk.CTkFrame(self.root, fg_color="#1f1f2e") 
        self.bg_frame.pack(fill="both", expand=True)
        self.frame = ctk.CTkFrame(self.bg_frame, corner_radius=15, fg_color="#2c2c3c")
        self.frame.pack(pady=100, padx=40, fill="both", expand=True)
        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Username", height=40)
        self.username_entry.pack(pady=(30,10), padx=20, fill="x")
        self.title_label = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(0, 5))
        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*", height=40)
        self.password_entry.pack(pady=(5,10), padx=20, fill="x")
        self.message_label = ctk.CTkLabel(self.frame, text="")
        self.message_label.pack(pady=5)

        self.signup_button = ctk.CTkButton(self.frame, text="Register", command=self.signup)
        self.signup_button.pack(pady=15)

    def signup(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            self.message_label.configure(text="Fill all fields", text_color="orange")
            return

        if len(password) < 8:
            self.message_label.configure(text="Password must be at least 8 characters", text_color="red")
            return
        success = create_user(username, password)
        if success:
            user = verify_user(username, password)
            self.bg_frame.destroy() 
            DashboardWindow(self.root, user[0])
        else:
            self.message_label.configure(text="Username already exists", text_color="red")