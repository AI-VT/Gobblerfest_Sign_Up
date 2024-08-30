import os
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.serving import run_simple

app = Flask(__name__)
CORS(app)  # This allows our frontend to make requests to this backend

CSV_FILE = 'aiml_club_signups.csv'

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['email', 'design_team', 'paper_readings', 'education'])

init_csv()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data['email']
    design_team = data['designTeam']
    paper_readings = data['paperReadings']
    education = data['education']

    # Check if email already exists
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        if any(row[0] == email for row in reader):
            return jsonify({"message": "Email already registered"}), 400

    # Add new signup
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, design_team, paper_readings, education])

    return jsonify({"message": "Signup successful!"}), 201

@app.route('/signups', methods=['GET'])
def get_signups():
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        signups = list(reader)
    return jsonify(signups), 200

if __name__ == '__main__':
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True)