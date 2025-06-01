import customtkinter as ctk
from models.user import verify_user
from ui.dashboard import DashboardWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.configure(fg_color="#1f1f2e")  
        self.frame = ctk.CTkFrame(root, fg_color="#2c2c3c", corner_radius=15)
        self.frame.pack(pady=50, padx=50, fill="both", expand=True)
        self.title_label = ctk.CTkLabel(self.frame, text="🔐 Login", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=(20, 30))
        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Username",width=300, height=35, corner_radius=10)
        self.username_entry.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*", width=300, height=35, corner_radius=10)
        self.password_entry.pack(pady=10)
        self.login_button = ctk.CTkButton(self.frame, text="Login", command=self.login,width=300, height=40, corner_radius=10)
        self.login_button.pack(pady=20)
        self.message_label = ctk.CTkLabel(self.frame, text="")
        self.message_label.pack(pady=2)
        self.signup_button = ctk.CTkButton(self.frame, text="Sign Up", command=self.open_signup, width=300, height=40, corner_radius=10, fg_color="#3a3a5a", hover_color="#505080")
        self.signup_button.pack(pady=5)
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = verify_user(username, password)
        if user:
            self.frame.destroy()
            DashboardWindow(self.root, user[0]) 
        else:
            self.message_label.configure(text="Invalid username or password", text_color="red")
            return
    def open_signup(self):
        from ui.signup import SignUpWindow
        self.frame.destroy()
        SignUpWindow(self.root)

