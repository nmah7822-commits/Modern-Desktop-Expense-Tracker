import sqlite3
import os
from datetime import datetime

# Cloud par sahi path dhoondhne ke liye
DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.create_budget_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                amount REAL,
                description TEXT
            )
        ''')
        self.conn.commit()

    def create_budget_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget (
                id INTEGER PRIMARY KEY,
                monthly_limit REAL
            )
        ''')
        self.conn.commit()
        self.cursor.execute('SELECT COUNT(*) FROM budget')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('INSERT INTO budget (monthly_limit) VALUES (0)')
            self.conn.commit()

    def add_expense(self, date, category, amount, description):
        self.cursor.execute(
            'INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)',
            (date, category, amount, description)
        )
        self.conn.commit()

    def get_filtered_expenses(self, category="All", search_text=""):
        query = 'SELECT * FROM expenses WHERE 1=1'
        params = []
        if category != "All":
            query += ' AND category = ?'
            params.append(category)
        if search_text:
            query += ' AND description LIKE ?'
            params.append(f'%{search_text}%')
        query += ' ORDER BY date DESC'
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_current_month_expenses(self):
        current_month = datetime.now().strftime("%Y-%m")
        self.cursor.execute('SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC', (f'{current_month}%',))
        return self.cursor.fetchall()

    def get_monthly_budget(self):
        self.cursor.execute('SELECT monthly_limit FROM budget WHERE id = 1')
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def set_monthly_budget(self, amount):
        self.cursor.execute('UPDATE budget SET monthly_limit = ? WHERE id = 1', (amount,))
        self.conn.commit()

    def delete_expense(self, expense_id):
        self.cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        self.conn.commit()
        
    def get_all_expenses(self):
        self.cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        return self.cursor.fetchall()