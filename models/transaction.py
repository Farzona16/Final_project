from database.db_manager import get_connection
def add_transaction(card_id, amount, trans_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Transactions (card_id, amount, type) VALUES (?, ?, ?)", (card_id, amount, trans_type))
    if trans_type == 'add':
        cursor.execute("UPDATE Cards SET balance = balance + ? WHERE id=?", (amount, card_id))
    elif trans_type == 'withdraw':
        cursor.execute("UPDATE Cards SET balance = balance - ? WHERE id=?", (amount, card_id))
    conn.commit()

def get_balance(card_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM Cards WHERE id=?", (card_id,))
    return cursor.fetchone()[0]
    