from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import joblib
import random
import json

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
CORS(app)

# Load ML model
model = joblib.load("expense_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# ---------- DATABASE ----------
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            merchant TEXT,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict_category():
    merchant = request.json.get("merchant", "").lower()
    X = vectorizer.transform([merchant])
    category = model.predict(X)[0]
    return jsonify({"category": category})

@app.route("/add-expense", methods=["POST"])
def add_expense():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO expenses (amount, merchant, category) VALUES (?, ?, ?)",
        (data["amount"], data["merchant"], data["category"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "Expense added successfully"})

# ✅ MEME ROUTE (MUST BE HERE)
@app.route("/meme/<category>")
def get_meme(category):
    try:
        with open(f"../frontend/static/memes/{category.lower()}.json", "r", encoding="utf-8") as f:
            memes = json.load(f)
    except:
        with open("../frontend/static/memes/default.json", "r", encoding="utf-8") as f:
            memes = json.load(f)

    return jsonify({"meme": random.choice(memes)})

# ---------- RUN APP ----------
@app.route("/summary")
def spending_summary():
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT category, SUM(amount) as total FROM expenses GROUP BY category"
    ).fetchall()
    conn.close()

    if not rows:
        return jsonify({"summary": "Abhi koi expense data nahi hai 🤷‍♂️"})

    totals = {row["category"]: row["total"] for row in rows}
    overall = sum(totals.values())
    top_category = max(totals, key=totals.get)

    summary = (
        f"Is month tumne sabse zyada kharcha "
        f"{top_category} pe kiya 😅. "
        f"Total expense ₹{int(overall)} raha. "
        f"Agar thoda control kar lo, next month savings possible hai 👍"
    )

    return jsonify({"summary": summary})

@app.route("/chart-data")
def chart_data():
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT category, SUM(amount) as total FROM expenses GROUP BY category"
    ).fetchall()
    conn.close()

    labels = [row["category"] for row in rows]
    values = [row["total"] for row in rows]

    return jsonify({
        "labels": labels,
        "values": values
    })
@app.route("/reset", methods=["POST"])
def reset_data():
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()
    return jsonify({"status": "All data cleared"})

if __name__ == "__main__":
    app.run()