from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Get MongoDB connection details from .env
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME")

# Connect to MongoDB Atlas
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]


# ------------------- API ROUTE -------------------
@app.route("/api")
def api_route():
    """Reads data from data.json and returns JSON response"""
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------- FRONTEND FORM -------------------
@app.route("/")
def index():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form["name"]
        email = request.form["email"]

        # Insert into MongoDB
        collection.insert_one({"name": name, "email": email})

        # Redirect to success page
        return redirect(url_for("success"))
    except Exception as e:
        # Stay on form page with error
        return render_template("form.html", error=str(e))


@app.route("/success")
def success():
    return "Data submitted successfully"


if __name__ == "__main__":
    app.run(debug=True)
