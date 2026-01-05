import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1. Load dataset
data = pd.read_csv("../data/expenses.csv")

X = data["merchant"].str.lower()
y = data["category"]

# 2. Convert text to numbers
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# 3. Train model
model = LogisticRegression()
model.fit(X_vectorized, y)

# 4. Save model & vectorizer
joblib.dump(model, "expense_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model trained and saved successfully")
