import customtkinter as ctk
from models.card import get_cards
from models.transaction import add_transaction, get_balance

class WithdrawFundsWindow(ctk.CTkToplevel):
    def __init__(self, root, user_id):
        super().__init__(root)
        self.root = root
        self.user_id = user_id
        self.title("💸 Withdraw Funds")
        self.geometry("500x500")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#2c2f3a")  
        self.cards = self.load_user_cards()

        self.title_label = ctk.CTkLabel(self, text="Withdraw From Card", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=(20, 10))

        if not self.cards:
            ctk.CTkLabel(self, text="You have no cards to withdraw from", text_color="red").pack(pady=20)
            ctk.CTkButton(self, text="Back", command=self.destroy, width=120, height=35, corner_radius=8).pack(pady=10)
            return

        self.cards_combobox = ctk.CTkComboBox(
            self,
            values=[f"{card[1][:4]} **** **** {card[1][-4:]}" for card in self.cards],
            width=280,
            height=35,
            corner_radius=10,
            font=("Arial", 14)
        )
        self.cards_combobox.pack(pady=10)

        self.amount_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter amount",
            width=280,
            height=35,
            corner_radius=10
        )
        self.amount_entry.pack(pady=10)

        self.message_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.message_label.pack(pady=5)

        self.withdraw_button = ctk.CTkButton(
            self,
            text="Withdraw Funds",
            command=self.withdraw_funds,
            width=150,
            height=40,
            corner_radius=10,
            fg_color="#ff6363",
            hover_color="#cc4c4c"
        )
        self.withdraw_button.pack(pady=(10, 5))

        self.back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.destroy,
            width=150,
            height=35,
            corner_radius=10,
            fg_color="#444",
            hover_color="#666"
        )
        self.back_button.pack(pady=5)

    def load_user_cards(self):
        return get_cards(self.user_id)

    def withdraw_funds(self):
        selected_card = self.cards_combobox.get()
        amount = self.amount_entry.get()

        if not amount.isdigit() or int(amount) <= 0:
            self.message_label.configure(text="❌ Invalid amount", text_color="red")
            return

        card_id = None
        for card in self.cards:
            display = f"{card[1][:4]} **** **** {card[1][-4:]}"
            if display == selected_card:
                card_id = card[0]
                break

        if card_id is None:
            self.message_label.configure(text="❌ Please select a card", text_color="red")
            return

        balance = get_balance(card_id)
        if balance < int(amount):
            self.message_label.configure(text="❌ Insufficient funds", text_color="red")
            return

        add_transaction(card_id, int(amount), "withdraw")
        self.message_label.configure(text=f"✅ ${amount} withdrawn from your card", text_color="green")

    def go_back(self):
        self.destroy()
        from ui.dashboard import DashboardWindow
        DashboardWindow(self.root, self.user_id)
