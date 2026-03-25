import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime

# Pathing for Vercel: looking one folder up for templates
app = Flask(__name__, template_folder='../templates')

# MongoDB Connection with a 5-second timeout
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client.vibe_db
collection = db.updates

@app.route('/')
def index():
    try:
        # If DB connection fails, this will jump to 'except' after 5 seconds
        posts = list(collection.find().sort("_id", -1))
    except Exception as e:
        print(f"DB Error: {e}")
        posts = []
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add():
    skill = request.form.get('skill')
    notes = request.form.get('notes')
    if skill:
        try:
            collection.insert_one({
                "skill": skill,
                "notes": notes,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        except:
            pass
    return redirect('/')