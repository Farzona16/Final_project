# ==== models/card.py ====
from database.db_manager import get_connection

def add_card(user_id, number, pin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Cards (user_id, number, pin, balance) VALUES (?, ?, ?, 0)", (user_id, number, pin))
    conn.commit()

def get_cards(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, number, balance FROM Cards WHERE user_id=?", (user_id,))
    return cursor.fetchall()
def card_exists(user_id, card_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Cards WHERE user_id=? AND number=?", (user_id, card_number))
    return cursor.fetchone() is not None
def delete_card(user_id, card_number):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Cards WHERE user_id = ? AND number = ?", (user_id, card_number))
        row = cursor.fetchone()
        if row is None:
            return False 
        card_id = row[0]

        cursor.execute("DELETE FROM Transactions WHERE card_id = ?", (card_id,))
        cursor.execute("DELETE FROM Cards WHERE id = ?", (card_id,))

        conn.commit()
        return True