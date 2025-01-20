from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from yolov4 import detect_cars
from algo import optimize_traffic
import psycopg2
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Ensure the uploads directory exists
os.makedirs('uploads', exist_ok=True)

conn = psycopg2.connect(
    dbname="traffic_management_db",
    user="traffic_user",
    password="Toxic1345",
    host="4000",
    port="5433"
)
cursor = conn.cursor()

# Store traffic data
def store_traffic_data(intersection_id, vehicle_count):
    timestamp = datetime.now()
    cursor.execute(
        "INSERT INTO traffic_data (timestamp, intersection_id, vehicle_count) VALUES (%s, %s, %s)",
        (timestamp, intersection_id, vehicle_count)
    )
    conn.commit()

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('videos')
    if len(files) != 4:
        return jsonify({'error': 'Please upload exactly 4 videos'}), 400

    video_paths = []
    for i, file in enumerate(files):
        video_path = os.path.join('uploads', f'video_{i}.mp4')
        file.save(video_path)
        video_paths.append(video_path)

    num_cars_list = []
    for video_file in video_paths:
        num_cars = detect_cars(video_file)
        num_cars_list.append(num_cars)
        store_traffic_data(intersection_id=1, vehicle_count=num_cars)

    result = optimize_traffic(num_cars_list)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


# filepath: AI-Based-Traffic-Management-System/backend/algo.py
import pandas as pd
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('traffic_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def analyze_historical_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM traffic_data")
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows, columns=['id', 'timestamp', 'intersection_id', 'vehicle_count'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Perform analysis (e.g., calculate average vehicle count per hour)
    df['hour'] = df['timestamp'].dt.hour
    avg_vehicle_count = df.groupby('hour')['vehicle_count'].mean()
    return avg_vehicle_count.to_dict()


