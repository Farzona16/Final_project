import customtkinter as ctk
from models.card import add_card, get_cards, card_exists, delete_card
class DashboardWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.bg_frame = ctk.CTkFrame(self.root, fg_color="#1f1f2e")
        self.bg_frame.pack(fill="both", expand=True)
        self.frame = ctk.CTkFrame(self.bg_frame, corner_radius=15, fg_color="#2c2c3c")
        self.frame.pack(padx=40, pady=40, fill="both", expand=True)
        self.title = ctk.CTkLabel(self.frame, text="🏠 Welcome to Dashboard", font=("Arial", 20, "bold"))
        self.title.pack(pady=15)

        self.card_button = ctk.CTkButton(self.frame, text="➕ Add Card", command=self.add_card_ui)
        self.card_button.pack(pady=5)


        self.transact_button = ctk.CTkButton(self.frame, text="💳 View Cards", command=self.view_cards)
        self.transact_button.pack(pady=5)


        self.add_funds_button = ctk.CTkButton(self.frame, text="💰 Add Funds", command=self.open_add_funds)
        self.add_funds_button.pack(pady=5)


        self.withdraw_funds_button = ctk.CTkButton(self.frame, text="📤 Withdraw Funds", command=self.open_withdraw_funds)
        self.withdraw_funds_button.pack(pady=5)


        self.back_button = ctk.CTkButton(self.frame, text="🔒 Logout", command=self.logout, fg_color="#a00")
        self.back_button.pack(pady=15)

    def logout(self):
        self.bg_frame.destroy() 
        from ui.login import LoginWindow
        LoginWindow(self.root)
    def add_card_ui(self):
        self.clear_frame()
        self.card_number_entry = ctk.CTkEntry(self.frame, placeholder_text="Card Number (16 digits)", width=160)
        self.card_number_entry.pack(pady=(50,10))

        self.pin_entry = ctk.CTkEntry(self.frame, placeholder_text="PIN (4 digits)", show="*", width=160)
        self.pin_entry.pack(pady=(0,20))

        ctk.CTkButton(self.frame, text="Submit",width=160, command=self.save_card).pack(pady=(10,5))
        self.back_button = ctk.CTkButton(self.frame, text="Back", width=160, command=self.refresh_dashboard)
        self.back_button.pack()
    def save_card(self):
        card_number = self.card_number_entry.get()
        pin = self.pin_entry.get()

        if hasattr(self, 'feedback_label'):
            self.feedback_label.destroy()

        if not card_number.isdigit() or len(card_number) != 16:
            self.feedback_label = ctk.CTkLabel(self.frame, text="Invalid card number", text_color="red")
            self.feedback_label.pack()
            return

        if not pin.isdigit() or len(pin) != 4:
            self.feedback_label = ctk.CTkLabel(self.frame, text="Invalid PIN", text_color="red")
            self.feedback_label.pack()
            return

        if card_exists(self.user_id, card_number):
            self.feedback_label = ctk.CTkLabel(self.frame, text="This card already exists!", text_color="red")
            self.feedback_label.pack()
            return

        add_card(self.user_id, card_number, pin)

        self.feedback_label = ctk.CTkLabel(self.frame, text="Card added successfully!", text_color="green")
        self.feedback_label.pack()

    def delete_card_ui(self, card_number):
        delete_card(self.user_id, card_number)

        self.feedback_label = ctk.CTkLabel(self.frame, text="Card deleted successfully!", text_color="green")
        self.feedback_label.pack()

        self.view_cards()
    

    def view_cards(self):
        self.clear_frame()
        cards = get_cards(self.user_id)

        if not cards:
            ctk.CTkLabel(self.frame, text="No cards found.").pack()

        for c in cards:
            card_number = c[1]
            short_number = f"{card_number[:4]} **** **** {card_number[-4:]}"
            card_info = f"Card: {short_number} | Balance: ${c[2]}"

            card_frame = ctk.CTkFrame(self.frame)
            card_frame.pack(pady=5, fill="x", padx=10)

            ctk.CTkLabel(card_frame, text=card_info).pack(side="left", padx=10)
            ctk.CTkButton(card_frame, text="❌ Delete", text_color="red", width=60,
            command=lambda number=card_number: self.delete_card_ui(number)).pack(side="right", padx=10)

        self.back_button = ctk.CTkButton(self.frame, text="Back", command=self.refresh_dashboard)
        self.back_button.pack(pady=10)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def refresh_dashboard(self):
        self.bg_frame.destroy()
        self.__init__(self.root, self.user_id)
    def open_add_funds(self):
        from ui.add_funds import AddFundsWindow
        AddFundsWindow(self.root, self.user_id)

    def open_withdraw_funds(self):
        from ui.withdraw_funds import WithdrawFundsWindow
        WithdrawFundsWindow(self.root, self.user_id)