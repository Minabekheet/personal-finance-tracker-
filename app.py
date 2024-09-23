from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('finance.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS transactions 
                        (id INTEGER PRIMARY KEY, type TEXT, amount REAL)''')

@app.route('/')
def index():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['POST'])
def add_transaction():
    transaction_type = request.form['type']
    amount = request.form['amount']
    with sqlite3.connect('finance.db') as conn:
        conn.execute('INSERT INTO transactions (type, amount) VALUES (?, ?)', (transaction_type, amount))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

