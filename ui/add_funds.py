import customtkinter as ctk 
from models.card import get_cards
from models.transaction import add_transaction

class AddFundsWindow(ctk.CTkToplevel):
    def __init__(self, root, user_id):
        super().__init__(root)
        self.root = root
        self.user_id = user_id
        self.title("💳 Add Funds")
        self.geometry("500x500")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#2c2f3a")  
        self.cards = self.load_user_cards()

        self.title_label = ctk.CTkLabel(self, text="Add Funds to Card", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=(20, 10))

        if not self.cards:
            ctk.CTkLabel(self, text="You have no cards to add funds", text_color="red").pack(pady=20)
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

        self.add_button = ctk.CTkButton(
            self,
            text="Add Funds",
            command=self.add_funds,
            width=150,
            height=40,
            corner_radius=10,
            fg_color="#4a90e2",
            hover_color="#357ABD"
        )
        self.add_button.pack(pady=(10, 5))

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

    def add_funds(self):
        amount = self.amount_entry.get()
        if not amount.isdigit() or int(amount) <= 0:
            self.message_label.configure(text="❌ Invalid amount", text_color="red")
            return

        selected_card_display = self.cards_combobox.get()
        card_index = None
        for card in self.cards:
            display = f"{card[1][:4]} **** **** {card[1][-4:]}"
            if display == selected_card_display:
                card_index = card[0]
                break

        if card_index is None:
            self.message_label.configure(text="❌ Please select a card", text_color="red")
            return

        add_transaction(card_index, int(amount), "add")
        self.message_label.configure(text=f"✅ ${amount} added to your card", text_color="green")

    def go_back(self):
        self.destroy()
        from ui.dashboard import DashboardWindow
        DashboardWindow(self.root, self.user_id)
